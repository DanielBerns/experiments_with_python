import sys
import getpass
from app import app, db, User

def show_help():
    """Prints the help message for the script."""
    print("""
Database Initialization and User Management Script

Usage:
  python manage_db.py <command>

Commands:
  --create      Initializes the database and creates the default 'admin' user.
                The default password is 'password'.
  --adduser     Prompts to add a new user to the database.
  --help        Shows this help message.
""")

def get_credentials():
    username = input("Enter username: ")
    if not username:
        print("Username cannot be empty.")
        return None, None
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Error: Passwords do not match.")
        return None, None
    return username, password


def create_database_and_default_user():
    """Creates all database tables and a default admin user."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

        username, password = get_credentials()
        if username != "admin":
            print("wrong username")
            return
        if not User.query.filter_by(username="admin").first():
            print("Creating default user: 'admin'...")
            admin_user = User(username='admin')
            admin_user.set_password(password)
            db.session.add(admin_user)
            db.session.commit()
            print("Default user 'admin' created")
        else:
            print("User 'admin' already exists.")

def add_new_user():
    """Adds a new user to the database via command-line prompts."""
    with app.app_context():
        _username, _password = get_credentials()
        if _username is None:
            return
        if _password is None:
            return
        if User.query.filter_by(username=_username).first():
            print(f"Error: User '{_username}' already exists.")
            return
        new_user = User(username=_username)
        new_user.set_password(_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' created successfully.")

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        show_help()
        return

    command = sys.argv[1]

    if command == '--create':
        create_database_and_default_user()
    elif command == '--adduser':
        add_new_user()
    else:
        print(f"Error: Unknown command '{command}'")
        show_help()

if __name__ == '__main__':
    main()
