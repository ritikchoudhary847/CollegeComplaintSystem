import sqlite3

def create_database():

    connection = sqlite3.connect(
        "college_complaints.db"
    )
    cursor = connection.cursor()

    # Complaints table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            roll_no TEXT,
            complaint TEXT,
            category TEXT,
            priority TEXT,
            status TEXT
        )
    """)

    # Add date and time column

    try:
        cursor.execute(
            "ALTER TABLE complaints "
            "ADD COLUMN created_at TEXT"
        )
    except sqlite3.OperationalError:

        pass

    # Students table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll_no TEXT UNIQUE,
            email TEXT,
            password TEXT,
            department TEXT,
            semester TEXT
        )
    """)
    connection.commit()
    connection.close()
create_database()