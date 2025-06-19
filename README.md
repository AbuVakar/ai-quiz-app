<div align="center">
  <h1>AI Quiz Generator</h1>
  <h3>🤖 Generate MCQs from Text, PDFs, and YouTube Videos</h3>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-2.0.3-green.svg)](https://flask.palletsprojects.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
  ![Demo](https://via.placeholder.com/800x400?text=AI+Quiz+Generator+Demo)
</div>

---

## 📌 Overview

AI Quiz Generator is an intelligent web application that automatically generates multiple-choice questions (MCQs) from various content sources using advanced AI and NLP technologies. Perfect for students, teachers, and content creators who need to create quizzes quickly and efficiently.

### 🌟 Key Features

- **Multiple Input Sources**
  - Generate MCQs from plain text
  - Upload and process PDF documents
  - Extract content from YouTube videos
  
- **Smart Question Generation**
  - AI-powered question formulation
  - Multiple difficulty levels
  - Context-aware answer choices
  
- **User Management**
  - Secure authentication system
  - Profile customization
  - Quiz history tracking
  
- **Gamification**
  - Earn XP for quizzes taken
  - Level up and unlock achievements
  - Daily streaks and leaderboards

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.0.3
- **Database**: SQLAlchemy with SQLite
- **AI/NLP**: Transformers, PyTorch, spaCy
- **Authentication**: Flask-Login

### Frontend
- HTML5, CSS3, JavaScript
- Responsive Design
- Interactive UI Components

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-quiz-app.git
   cd ai-quiz-app
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python migrate_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the app**
   Open your browser and visit: [http://localhost:5000](http://localhost:5000)

## 📂 Project Structure

```
ai-quiz-app/
├── backend/           # Backend application
│   ├── app/           # Main application package
│   │   ├── __init__.py
│   │   ├── models.py  # Database models
│   │   ├── routes.py  # Application routes
│   │   └── nlp/       # NLP processing modules
│   ├── migrations/    # Database migrations
│   ├── uploads/       # User uploads storage
│   ├── config.py      # Configuration settings
│   ├── requirements.txt
│   └── run.py         # Application entry point
└── frontend/          # Frontend files
    ├── css/           # Stylesheets
    ├── js/            # JavaScript files
    └── *.html         # HTML templates
```

## 📝 Usage Guide

### Generating MCQs
1. Sign up or log in to your account
2. Choose your input method (Text/PDF/YouTube)
3. Enter the content or upload a file
4. Configure quiz settings
5. Generate and take the quiz

### User Dashboard
- View your quiz history
- Track your progress and achievements
- Manage your profile

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-branch`
6. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- Built with ❤️ using Python and Flask
- Powered by Transformers and PyTorch
- Icons by [Font Awesome](https://fontawesome.com/)

---