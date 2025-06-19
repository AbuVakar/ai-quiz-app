# Database models go here (move your existing code here)

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_photo = db.Column(db.String(256), nullable=True)  # URL or path to profile photo
    bio = db.Column(db.String(512), nullable=True)  # User bio
    histories = db.relationship("History", backref="author", lazy="dynamic")
    # Gamification fields
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    badges = db.Column(db.JSON, default=list)  # List of badge names/IDs
    streak = db.Column(db.Integer, default=0)
    last_quiz_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.username}>"

    def add_xp(self, amount):
        # XP thresholds for each level (simple formula: 100 * level)
        self.xp += amount
        leveled_up = False
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            leveled_up = True
        return leveled_up

    def add_badge(self, badge_name):
        if self.badges is None:
            self.badges = []
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            return True
        return False

    def update_streak(self, today):
        if self.last_quiz_date:
            delta = (today.date() - self.last_quiz_date.date()).days
            if delta == 1:
                self.streak += 1
            elif delta > 1:
                self.streak = 1
        else:
            self.streak = 1
        self.last_quiz_date = today

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(10))  # "text", "pdf", or "youtube"
    input_content = db.Column(db.Text)       # A snippet or filename/URL
    generated_mcqs = db.Column(db.Text)        # Store JSON string of MCQs
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # New fields for quiz attempt
    user_answers = db.Column(db.JSON)  # List of user answers
    score = db.Column(db.Integer)      # User's score
    attempt_time = db.Column(db.Integer)  # Time taken in seconds (optional)

    def __repr__(self):
        return f"<History {self.id} by User {self.user_id}>"
