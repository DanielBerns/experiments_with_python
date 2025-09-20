# Project: Task Configuration & Reporting Website

This web application provides a user interface to configure parameters, run long-running tasks, and monitor their status, all driven by a central YAML file.

## Features

- **Dynamic Page Generation**: Site structure, forms, and buttons are defined in `config.yaml`.
- [cite_start]**User Authentication**: Secure login/logout system using Flask-Login. [cite: 4]
- [cite_start]**Configuration Auditing**: All parameter changes are logged to a database. [cite: 22]
- [cite_start]**Asynchronous Task Execution**: Shell scripts are run in the background without blocking the UI. [cite: 8]
- [cite_start]**Configuration Export**: Export current settings to a local YAML file. [cite: 2]

## Setup and Installation

### Prerequisites

- Python 3.8+
- `pip` for package installation

### Installation Steps

1.  **Clone the repository or create the project files:**
    Ensure all files (`app.py`, `config.yaml`, `requirements.txt`, etc.) are in a single project directory as specified in the file structure.

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Make the shell scripts executable (on Linux/macOS):**
    ```bash
    chmod +x scripts/processing/start.sh
    chmod +x scripts/backup/start.sh
    ```

## How to Run the Application

1.  **Initialize the Database:**
    From your terminal, run the following commands to set up the database and create the first user.

    ```bash
    # Open the Flask shell
    flask shell

    # In the Python interpreter, run:
    >>> from app import db, User
    >>> db.create_all()
    >>> User.create_default_user()
    >>> exit()
    ```
    This will create a user with the username `admin` and password `password`.

2.  **Run the Flask Development Server:**
    ```bash
    flask run
    ```

3.  **Access the Application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`. You will be redirected to the login page. Use the credentials created above to log in.
