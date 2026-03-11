import os
from app import create_app

# Create Flask app
app = create_app()

# Gunicorn entry point
application = app

if __name__ == "__main__":
    # Local development
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)