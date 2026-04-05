# DEVELOPMENT PURPOSE ONLY - FOR PRODUCTION USE GUNICORN AND EXPOSE THE WSGI APP IN THE APP DIRECTORY

from app import app

if __name__ == "__main__":
    app.run(debug=True)
