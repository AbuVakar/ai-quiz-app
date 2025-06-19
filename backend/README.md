# Backend (Flask)

This folder contains the Flask backend for the AI Quiz Generator project.

## How to Run

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```

## Structure
- `app/`: All backend Python code (routes, models, NLP, utils)
- `static/` and `templates/`: For serving files if needed
- `requirements.txt`: Python dependencies
- `run.py`: Entry point for Flask app

---

## Notes
- Make sure to update `config.py` as needed.
- NLP and AI logic is inside `app/nlp/`.
