import sqlite3
import os

def initialize_database():
    db_file = 'school_management_system.db'
    db_exists = os.path.exists(db_file)
    
    conn = get_db_connection()

    if not db_exists:
        create_tables(conn)
        return {"message": "Database created and initialized successfully"}, 200
    else:
        return {"message": "Database already exists"}, 200

def get_db_connection():
    conn = sqlite3.connect('school_management_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (student_id, course_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_instructors (
        instructor_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (instructor_id) REFERENCES instructors (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (instructor_id, course_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def backup_database(backup_path: str):
    conn = get_db_connection()
    backup_conn = sqlite3.connect(os.path.join(backup_path, "school_management_system_backup.db"))
    conn.backup(backup_conn)
    backup_conn.close()
    conn.close()
    return {"message": "Database backup created successfully"}, 200

