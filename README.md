# SISTEM UNDIGITAL KELAB KKQ SMKDD1

A PHP ported web app built using Python (Flask)

## Project Requirements
- Python (refer to pyproject.toml)
- UV (install with pip)
  ```bash
  pip install uv
  ```
  Refer https://docs.astral.sh/uv/getting-started/installation/ for more installation guides

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
6. Run the project:
   ```bash
   python 'run.py'
   ```
7. Visit http://localhost:5000 on your browser
