import sys
import argparse
import os
import django
from db_connection import get_db_connection

def setup_django():
    """
    Initializes the Django environment to allow use of the ORM.
    This must be called before importing any Django models.
    """
    # Add the project root to the Python path to allow imports like 'accounts.models'
    # This assumes the script is in the project root.
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jelani_backend.settings')
    try:
        django.setup()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


def fetch_all_users():
    """
    Tests the database connection and queries the accounts_user table.
    """
    print("--- Fetching all users from the database ---")
    conn = get_db_connection()

    if not conn:
        print("\n--- Test Failed: Could not establish database connection. ---")
        sys.exit(1)

    print("\n✅ SUCCESS: Database connection established successfully!")

    # Import specific exceptions to handle them gracefully
    try:
        from MySQLdb import ProgrammingError
    except ImportError:
        # This case is already handled in db_connection.py, but it's good practice for robustness
        print("❌ Error: The 'mysqlclient' library is not installed.")
        sys.exit(1)

    try:
        # Perform a query to fetch users from the 'accounts_user' table.
        print("\n--- Attempting to fetch data from 'accounts_user' table ---")
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM accounts_user;")
            rows = cursor.fetchall()

            # Get column names to safely find and redact the password
            column_names = [desc[0] for desc in cursor.description]
            password_index = -1
            if 'password' in column_names:
                password_index = column_names.index('password')

            if rows:
                print(f"✅ SUCCESS: Found {len(rows)} user(s).")
                print(f"Columns: {', '.join(column_names)}")
                print("-------------------------------------------------")
                for row in rows:
                    row_list = list(row)
                    if password_index != -1:
                        row_list[password_index] = '[REDACTED]'
                    print(tuple(row_list))
            else:
                print("✅ SUCCESS: Query executed, but the 'accounts_user' table is empty.")

    except ProgrammingError as err:
        error_code, error_message = err.args
        print(f"\n❌ FAILED: Could not query the database.")
        print(f"   Error Code: {error_code}")
        print(f"   Error Message: {error_message}")
        if error_code == 1146:
            print("   -> Table 'accounts_user' not found. Please run `python manage.py migrate` to create it.")

    finally:
        if conn:
            conn.close()
            print("\nConnection closed.")

def register_user(username, email, password):
    """
    Registers a user using the Django ORM to ensure password hashing and data integrity.
    """
    print(f"\n--- Attempting to register user '{username}' via Django ORM ---")
    from django.contrib.auth import get_user_model
    from django.db import IntegrityError

    User = get_user_model()
    try:
        # The create_user method handles password hashing automatically.
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"✅ Django User '{user.username}' created successfully!")
    except IntegrityError:
        print(f"❌ Error: A user with username '{username}' or email '{email}' already exists.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jelani Backend Database Utility Script.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # 'test' command
    test_parser = subparsers.add_parser('test', help='Run a connection test and query the user table.')

    # 'register' command
    register_parser = subparsers.add_parser('register', help='Register a new user via the Django ORM.')
    register_parser.add_argument('username', type=str, help='The username for the new user.')
    register_parser.add_argument('email', type=str, help='The email for the new user.')
    register_parser.add_argument('password', type=str, help='The password for the new user.')

    args = parser.parse_args()

    if args.command == 'test':
        fetch_all_users()
    elif args.command == 'register':
        setup_django()  # Initialize Django environment before using the ORM
        register_user(args.username, args.email, args.password)