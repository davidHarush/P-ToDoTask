import sqlite3
import pandas as pd


def check_db(db_path):
    """
    Function to check the content of the tasks table in the given SQLite database.
    Args:
    - db_path: Path to the SQLite database file.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Fetch content of the tasks table
        tasks_df = pd.read_sql_query("SELECT * FROM tasks", conn)

        # Display the content of the tasks table
        print("Tasks Table Content:")
        print(tasks_df)

        conn.close()

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # Path to your SQLite database file
    db_path = 'tasks.db'

    # Check the content of the database
    check_db(db_path)
