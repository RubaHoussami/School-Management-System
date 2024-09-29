import sqlite3
import os
from src.utils.data_validator import DataValidator
from src.components.student import Student
from src.utils.db_controllers.general_controllers import get_db_connection

validator = DataValidator()

def register_student(name: str, age: int, email: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if validator.validate_name(name) and validator.validate_email(email) and validator.validate_age(age):
            cursor.execute('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', (name, age, email))
            conn.commit()
            return {"message": f'Student registered successfully', "student_id": cursor.lastrowid}, 200
        return {"message": "Invalid name or email or age"}, 400
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()

def add_student_to_course(student_id: int, course_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
        return {"message": "Student added to course successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Student or course not found"}, 404
    
def remove_student_from_course(student_id: int, course_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registrations WHERE student_id = ? AND course_id = ?', (student_id, course_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Student not registered in course or course/student not found"}, 404
    conn.close()
    return {"message": "Student removed from course successfully"}, 200

def remove_student(student_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Student not found"}, 404
    conn.close()
    return {"message": "Student deleted successfully"}, 200

def get_students() -> tuple[dict[str, dict[int, Student]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students_data = cursor.fetchall()
    conn.close()
    students = {}
    for student in students_data:
        student_courses, _ = get_student_course_ids_by_student_id(student['id'])
        students[student['id']] = Student(student['name'], student['age'], student['email'], student['id'], student_courses['course_ids'])
    return {"students": students}, 200

def get_student_course_ids_by_student_id(student_id: int) -> tuple[dict[str, list[int]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT course_id FROM registrations WHERE student_id = ?', (student_id,))
    course_ids = cursor.fetchall()
    conn.close()
    return {"course_ids": course_ids}, 200

def get_students_by_course(course_id: int) -> tuple[dict[str, dict[int, Student]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE course_id = ?', (course_id,))
    students_data = cursor.fetchall()
    conn.close()
    students = {}
    for student in students_data:
        student_courses, _ = get_student_course_ids_by_student_id(student['id'])['course_ids']
        students[student['id']] = Student(student['name'], student['age'], student['email'], student['id'], student_courses)
    return {"students": students}, 200

def get_student_courses(courses_ids: list) -> tuple[dict[str, list[str]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    courses_list = []
    for course_id in courses_ids:
        cursor.execute('SELECT name FROM courses WHERE id = ?', (course_id,))
        course = cursor.fetchone()
        if course is None:
            continue
        courses_list.append(course['name'])
    conn.close()
    return {"courses": courses_list}, 200

def get_student_id_by_name(student_name: str) -> tuple[dict[str, int], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE name = ?', (student_name,))
    student = cursor.fetchone()
    conn.close()
    return {"student_id": student['id']}, 200

def search_students(search_type: str, search_term: str) -> tuple[dict[str, list[Student]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        if validator.validate_name(search_term):
            cursor.execute('SELECT * FROM students WHERE name LIKE ?', (search_term,))
        else:
            conn.close()
            return {"message": "Invalid name"}, 400
    elif search_type == "email":
        if validator.validate_email(search_term):
            cursor.execute('SELECT * FROM students WHERE email = ?', (search_term,))
        else:
            conn.close()
            return {"message": "Invalid email"}, 400
    elif search_type == "id":
        cursor.execute('SELECT * FROM students WHERE id = ?', (int(search_term),))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    students_data = cursor.fetchall()
    conn.close()
    students = []
    for student in students_data:
        student_courses, _ = get_student_course_ids_by_student_id(student['id'])
        students.append(Student(student['name'], student['age'], student['email'], student['id'], student_courses['course_ids']))
    return {"students": students}, 200

def update_student(student_id: int, name: str, age: int, email: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if validator.validate_name(name) and validator.validate_email(email) and validator.validate_age(age):
            cursor.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?', (name, age, email, student_id))
            conn.commit()
            if cursor.rowcount == 0:
                return {"message": "Student not found"}, 404
            return {"message": "Student updated successfully"}, 200
        else:
            return {"message": "Invalid name or email or age"}, 400
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()