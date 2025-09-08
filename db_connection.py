import os
import sys

try:
    import MySQLdb
    from MySQLdb import OperationalError
except ImportError:
    print("❌ Error: The 'mysqlclient' library is not installed.")
    print("   Please ensure it's installed by running: pip install mysqlclient")
    sys.exit(1)

def get_db_connection():
    """
    Establishes and returns a database connection using credentials from the .env file.

    Returns:
        A MySQLdb connection object or None if the connection fails.
    """
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'passwd': os.getenv('DB_PASSWORD'),
        'db': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

    # Check if all required variables are present
    required_vars = ['host', 'user', 'db']
    missing_vars = [f"DB_{key.upper()}" for key in required_vars if not db_config[key]]
    if 'DB_PASSWORD' not in os.environ:
        missing_vars.append('DB_PASSWORD')

    if missing_vars:
        print(f"❌ Error: Missing required database environment variables in .env: {', '.join(missing_vars)}")
        return None

    try:
        conn = MySQLdb.connect(**db_config)
        return conn
    except OperationalError as err:
        error_code, error_message = err.args
        print(f"\n❌ FAILED: Could not connect to the database.")
        print(f"   Error Code: {error_code}")
        print(f"   Error Message: {error_message}")
        if error_code == 1045:
            print("   -> This is an 'Access Denied' error. Please check your DB_USER and DB_PASSWORD in the .env file.")
        elif error_code == 1049:
            print("   -> This is an 'Unknown Database' error. Please check your DB_NAME in the .env file.")
        elif error_code == 2003:
            print(f"   -> Can't connect to MySQL server on '{db_config['host']}'. Is the server running and the host/port correct?")
        return None