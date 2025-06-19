from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, History  # Added History import
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.nlp.mcq_generation import generate_mcqs
from app.utils.pdf_extraction import extract_text_from_pdf
from app.utils.youtube_extraction import extract_transcript_from_youtube
import os
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import requests
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.context_processor
def utility_processor():
    return {'now': datetime.now()}

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists.")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Reset Link")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")

@bp.route('/')
@bp.route('/index')
def index():
    login_form = LoginForm()
    signup_form = RegistrationForm()
    show_login_modal = request.args.get('show_login_modal', False)
    show_signup_modal = request.args.get('show_signup_modal', False)
    return render_template('index.html', title='Home', login_form=login_form, signup_form=signup_form, show_login_modal=show_login_modal, show_signup_modal=show_signup_modal)

@bp.route('/mcq')
@login_required
def mcq():
    return render_template('mcq.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/show')
@login_required
def show():
    return render_template('show.html')

@bp.route('/pdf', methods=['GET'])
@login_required
def pdf_page():
    return render_template('pdf.html')

@bp.route('/youtube', methods=['GET'])
@login_required
def youtube_page():
    return render_template('youtube.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.index', show_signup_modal=1))
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.index', show_signup_modal=1))
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.index', show_login_modal=1))
    elif form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
        return redirect(url_for('main.index', show_signup_modal=1))
    return render_template('signup.html', title='Sign Up', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.username.data) | (User.username == form.username.data)).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('main.index'))
        flash('Invalid username/email or password.', 'danger')
        return redirect(url_for('main.index', show_login_modal=1))
    elif form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
        return redirect(url_for('main.index', show_login_modal=1))
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    return send_from_directory(uploads_dir, filename)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username', current_user.username)
        bio = request.form.get('bio', current_user.bio)
        file = request.files.get('profile_photo')
        # Handle file upload
        if file and file.filename:
            uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            ext = os.path.splitext(file.filename)[1]
            filename = f'user_{current_user.id}_profile{ext}'
            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)
            # Save just the filename, not the path
            current_user.profile_photo = filename
        current_user.username = username
        current_user.bio = bio
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('profile.html')

@bp.route('/history')
@login_required
def history():
    import json
    histories = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).all()
    for h in histories:
        try:
            h.mcqs = json.loads(h.generated_mcqs)
        except Exception:
            h.mcqs = []
    return render_template('history.html', histories=histories)

@bp.route('/generate_mcqs', methods=['POST'])
def generate_mcqs_route():
    data = request.get_json()
    input_text = data.get('text', '')
    if not input_text.strip():
        return jsonify({'mcqs': [], 'error': 'No input text provided.'}), 400
    try:
        mcqs = generate_mcqs(input_text)
        # Save to history if user is logged in
        if current_user.is_authenticated:
            import json
            history = History(
                source_type='text',
                input_content=input_text[:2000],  # limit size
                generated_mcqs=json.dumps(mcqs),
                user_id=current_user.id
            )
            db.session.add(history)
            db.session.commit()
        return jsonify({'mcqs': mcqs})
    except Exception as e:
        return jsonify({'mcqs': [], 'error': str(e)}), 500

@bp.route('/generate_mcqs_from_pdf', methods=['POST'])
def generate_mcqs_from_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No PDF file provided.'}), 400
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)
    text = extract_text_from_pdf(file_path)
    mcqs = generate_mcqs(text)
    # Save to history if user is logged in
    if current_user.is_authenticated:
        import json
        history = History(
            source_type='pdf',
            input_content=file.filename,
            generated_mcqs=json.dumps(mcqs),
            user_id=current_user.id
        )
        db.session.add(history)
        db.session.commit()
    return jsonify({'mcqs': mcqs})

@bp.route('/generate_mcqs_from_youtube', methods=['POST'])
def generate_mcqs_from_youtube():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    if not youtube_url:
        return jsonify({'error': 'No YouTube URL provided.'}), 400
    text = extract_transcript_from_youtube(youtube_url)
    mcqs = generate_mcqs(text)
    # Save to history if user is logged in
    if current_user.is_authenticated:
        import json
        history = History(
            source_type='youtube',
            input_content=youtube_url,
            generated_mcqs=json.dumps(mcqs),
            user_id=current_user.id
        )
        db.session.add(history)
        db.session.commit()
    return jsonify({'mcqs': mcqs})

@bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    mcqs = None
    input_text = ''
    if request.method == 'POST':
        input_text = request.form.get('quiz_input', '').strip()
        if input_text:
            try:
                # If input is short (likely a topic), fetch Wikipedia summary
                if len(input_text.split()) < 8:
                    summary = fetch_wikipedia_summary(input_text)
                    if summary:
                        input_text = summary
                    else:
                        flash('No summary found for this topic on Wikipedia.', 'danger')
                        return render_template('quiz.html', mcqs=None, input_text=input_text)
                mcqs = generate_mcqs(input_text)
                # Gamification logic
                if current_user.is_authenticated:
                    from datetime import datetime
                    user = current_user
                    # Award XP for quiz completion
                    leveled_up = user.add_xp(20)  # 20 XP per quiz (example)
                    # Update streak
                    user.update_streak(datetime.utcnow())
                    # Badge logic
                    badge_unlocked = None
                    if user.streak == 3:
                        badge_unlocked = user.add_badge('3-Day Streak')
                    if user.level == 2:
                        badge_unlocked = user.add_badge('Level 2 Achiever')
                    db.session.commit()
                    if leveled_up:
                        flash(f'🎉 Level Up! You are now Level {user.level}.', 'success')
                    if badge_unlocked:
                        flash(f'🏅 New Badge Unlocked!', 'info')
            except Exception as e:
                flash(f'Error generating quiz: {str(e)}', 'danger')
    return render_template('quiz.html', mcqs=mcqs, input_text=input_text)

# Helper to generate and verify tokens
def generate_reset_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('main.reset_password', token=token, _external=True)
            # Improved flash message with copy button
            flash(f'''<div class="flex flex-col items-center gap-2">
                <span class="font-bold text-lg text-yellow-200">Password Reset Link</span>
                <a href="{reset_url}" target="_blank" class="break-all text-blue-200 underline font-mono hover:text-yellow-400">{reset_url}</a>
                <button onclick="navigator.clipboard.writeText('{reset_url}'); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy Link', 1500);" class="mt-2 px-3 py-1 bg-yellow-400 text-black font-bold rounded hover:bg-yellow-500 transition-all">Copy Link</button>
            </div>''', 'info')
        else:
            flash('If this email exists, a reset link has been sent.', 'info')
        return redirect(url_for('main.forgot_password'))
    return render_template('forgot_password.html', form=form)

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('main.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            try:
                user.password_hash = generate_password_hash(form.password.data)
                db.session.commit()
                flash('Your password has been reset successfully. Please login.', 'success')
                # Stay on the same page, show message, hide form
                return render_template('reset_password.html', form=None)
            except Exception as e:
                flash('An error occurred while resetting your password. Please try again.', 'danger')
                return render_template('reset_password.html', form=form)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('main.forgot_password'))
    return render_template('reset_password.html', form=form)

@bp.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    History.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Your quiz history has been cleared.', 'success')
    return redirect(url_for('main.history'))

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not name or not email or not message:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('main.contact'))
        # You can add logic here to save the message or send an email
        flash('Thank you for contacting us! We have received your message.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')

# Add more routes as needed

# Remove login_manager initialization from here; handled in __init__.py

@bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account and all associated data."""
    try:
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
            
        password = data.get('password')
        
        # Verify password
        if not check_password_hash(current_user.password_hash, password):
            return jsonify({'error': 'Incorrect password'}), 401
        
        # Delete all user's history
        History.query.filter_by(user_id=current_user.id).delete()
        
        # Delete profile photo if exists
        if current_user.profile_photo:
            try:
                photo_path = os.path.join(os.path.dirname(__file__), '..', 'uploads', current_user.profile_photo)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            except Exception:
                pass  # Continue with account deletion even if photo deletion fails
        
        # Delete user account
        db.session.delete(current_user)
        db.session.commit()
        
        # Logout user
        logout_user()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting account: {str(e)}")  # For debugging
        return jsonify({'error': 'Failed to delete account'}), 500

def fetch_wikipedia_summary(topic):
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(" ", "%20")}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('extract', '')
    return ''
