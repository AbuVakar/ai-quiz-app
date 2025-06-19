import os
import warnings
from app import create_app, db
from flask_migrate import Migrate

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download")

# Create application instance
app = create_app()
migrate = Migrate(app, db)

# For Gunicorn
application = app

if __name__ == "__main__":
    # When running directly, use the PORT environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)