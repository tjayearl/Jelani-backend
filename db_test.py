import os
import sys
import MySQLdb
from dotenv import load_dotenv

def test_db_connection():
    """
    Tests the connection to the MySQL database using credentials from the .env file.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, '.env')

    if not os.path.exists(env_path):
        print(f"❌ Error: .env file not found at {env_path}")
        sys.exit(1)

    load_dotenv(dotenv_path=env_path)

    # Get database credentials from environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    # Check if all required variables are present
    if not all([db_name, db_user, db_password, db_host, db_port]):
        print("❌ Error: One or more database environment variables are missing.")
        print("   Please ensure DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT are in your .env file.")
        sys.exit(1)

    print("--- Attempting to connect to the database ---")
    print(f"  Host:     {db_host}")
    print(f"  Port:     {db_port}")
    print(f"  Database: {db_name}")
    print(f"  User:     {db_user}")

    try:
        # Attempt to connect
        db = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            db=db_name,
            port=int(db_port)
        )
        print("\n✅ SUCCESS: Database connection established successfully!")
        db.close()
        print("   Connection closed.")

    except MySQLdb.OperationalError as e:
        error_code, error_message = e.args
        print(f"\n❌ FAILED: Could not connect to the database.")
        print(f"   Error Code:    {error_code}")
        print(f"   Error Message: {error_message}")
        print("\n   TROUBLESHOOTING: This is likely an 'Access Denied' or 'Unknown Database' error. Please verify the credentials and database name in your .env file and in your MySQL server.")

    except Exception as e:
        print(f"\n❌ FAILED: An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()