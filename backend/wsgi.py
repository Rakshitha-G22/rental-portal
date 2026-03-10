import os
from app import create_app

# Create Flask app
app = create_app()

# Gunicorn entry point
application = app

if __name__ == "__main__":
    # Use PORT environment variable if provided (Railway/Heroku)
    port = int(os.environ.get("PORT", 8080))
    # Only use debug=True for local development
    app.run(host="0.0.0.0", port=port, debug=True)