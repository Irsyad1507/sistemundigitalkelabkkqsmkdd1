# SISTEM UNDIGITAL KELAB KKQ SMKDD1

A PHP ported web app built using Python (Flask)

## Project Requirements
- Python (refer to pyproject.toml)
- UV (install with pip)
  ```bash
  pip install uv
  ```
  Refer [UV installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more installation guides

## Project Setup
1. Clone this repository
2. Install required dependencies (according to pyproject.toml):
   ```bash
   uv sync
   ```
3. Run this command to enter Python shell:
   ```bash
   python
   ```

   Or if you are using Unix-based terminal:
   ```bash
   python3
   ```

   For Git Bash users:
   ```bash
   winpty python
   ```
4. Create all necessary database using the shell:
   ```python
   >>> from app import app, db
   >>> app.app_context().push()
   >>> db.create_all()
   ```
5. Exit the shell using the exit() command
6. Create a .env file in the root directory
7. Add these to your .env file:
   ```.env
   SECRET_KEY="REPLACE-WITH-REAL-SECRET-KEY"
   DATABASE_URI="sqlite:///undi.db"
   ```
   - Generate secret keys at [djecrety website](https://djecrety.ir/)
8. Run the project:
   ```bash
   uv run 'run.py'
   ```
9. Visit http://localhost:5000 on your browser

## Notes
- This isn't intended for production deployment
- Feel free to tweak this based on your needs (do it on your local machine)
- Will add requirements.txt for legacy pip support
