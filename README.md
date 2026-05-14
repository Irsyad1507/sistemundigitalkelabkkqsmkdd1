# SISTEM UNDIGITAL KELAB KKQ SMKDD1

Live deployment at https://sistemundigitalkelabkkqsmkdd1.onrender.com/

A PHP ported web app built using Python (Flask)

## Project Requirements
- Python (refer to pyproject.toml > requires-python)
- UV (install with pip)
  ```bash
  pip install uv
  ```
  Refer [UV installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more installation guides
- Cloudinary free-tier account (register [here](https://cloudinary.com/users/register_free))

## Project Setup
1. Clone this repository
2. Install required dependencies (according to pyproject.toml):
   ```bash
   uv sync
   ```
3. Create a .env file in the root directory
4. Add these to your .env file:
   ```.env
   SECRET_KEY="REPLACE-WITH-REAL-SECRET-KEY"

   DATABASE_URI="sqlite:///undi.db"

   CLOUDINARY_CLOUD_NAME="REPLACE-WITH-YOUR-CLOUDINARY-CLOUD-NAME"

   CLOUDINARY_API_KEY="REPLACE-WITH-YOUR-CLOUDINARY-API-KEY"

   CLOUDINARY_API_SECRET="REPLACE-WITH-YOUR-CLOUDINARY-API-SECRET"
   ```
   - Generate secret keys at [djecrety website](https://djecrety.ir/)
5. Run these commands to initialize database:
   ```bash
   flask db init
   flask db migrate -m "Initial Migration"
   flask db upgrade
   ```
6. Run the project:
   ```bash
   uv run 'run.py'
   ```
7. Visit http://localhost:5000 on your browser

### Additional Notes
If you wanted to try this out with Docker, follow these steps:

1. Create a .dockerignore file and make sure it contains these:
   ```.dockerignore
   # Python-generated files
   __pycache__/
   *.py[oc]
   build/
   dist/
   wheels/
   *.egg-info

   # Virtual environments
   .venv

   # Environment variables
   *.env
   *.env.local
   .env.docker

   # VS Code settings
   .vscode/

   # Database files
   *.db
   *.sqlite
   instance/

   # Test Files
   create_db.py
   data_pengundi.*

   # Git files
   .git
   .gitignore

   .pytest_cache
   .coverage
   ```

2. Create a docker-compose.yml with these configurations:
   ```yml
   version: '3.8'

   services:
   web:
      build: .
      ports:
         - "8000:8000"
      environment:
         - DATABASE_URI=${DATABASE_URI}
         - SECRET_KEY=${SECRET_KEY}
         - FLASK_ENV=production
         - FLASK_DEBUG=0
         - CLOUDINARY_CLOUD_NAME=${CLOUDINARY_CLOUD_NAME}
         - CLOUDINARY_API_KEY=${CLOUDINARY_API_KEY}
         - CLOUDINARY_API_SECRET=${CLOUDINARY_API_SECRET}
      volumes:
         - ./app/static/imej/uploads:/app/app/static/imej/uploads
      depends_on:
         - web_wait
      restart: unless-stopped

   web_wait:
      image: willwill/wait-for-it:latest
      command: -h eu-central-1.db.thenile.dev -p 5432
   ```

3. Build and run the containers:
   ```bash
   docker compose up --build
   ```

- Recommended to use other databases such as PostgreSQL instead of SQLite for persistent storage in Docker containers

## Notes
- This isn't intended for production deployment
- Feel free to tweak this based on your needs (do it on your local machine)
- Will add requirements.txt for legacy pip support

## Known Limitations (of the live deployment above)
- The service might occasionally be inactive
- Expect high latency for database operations

## Contributions
For any suggestion, kindly open a new issue regarding it