import sqlite3
import os
from src.utils.data_validator import DataValidator
from src.components.instructor import Instructor
from src.utils.db_controllers.general_controllers import get_db_connection

validator = DataValidator()

def register_instructor(name: str, age: int, email: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if validator.validate_name(name) and validator.validate_email(email) and validator.validate_age(age):
            cursor.execute('INSERT INTO instructors (name, age, email) VALUES (?, ?, ?)', (name, age, email))
            conn.commit()
            return {"message": f'Instructor registered successfully', "instructor_id": cursor.lastrowid}, 200
        return {"message": "Invalid name or email or age"}, 400
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()

def add_instructor_to_course(instructor_id: int, course_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO course_instructors (instructor_id, course_id) VALUES (?, ?)', (instructor_id, course_id))
        conn.commit()
        return {"message": "Instructor added to course successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Instructor or course not found, or instructor already assigned"}, 400
    finally:
        conn.close()

def remove_instructor_from_course(instructor_id: int, course_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM course_instructors WHERE instructor_id = ? AND course_id = ?', (instructor_id, course_id))
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Instructor not assigned to course or course/instructor not found"}, 404
    conn.close()
    return {"message": "Instructor removed from course successfully"}, 200

def remove_instructor(instructor_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM instructors WHERE id = ?', (instructor_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Instructor not found"}, 404
    conn.close()
    return {"message": "Instructor deleted successfully"}, 200

def get_instructors() -> tuple[dict[str, dict[int, Instructor]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = {}
    for instructor in instructors_data:
        instructor_courses, _ = get_instructor_course_ids_by_instructor_id(instructor['id'])
        instructors[instructor['id']] = Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id'], instructor_courses['course_ids'])
    return {"instructors": instructors}, 200

def get_instructor_course_ids_by_instructor_id(instructor_id: int) -> tuple[dict[str, list[int]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT course_id FROM course_instructors WHERE instructor_id = ?', (instructor_id,))
    course_ids = cursor.fetchall()
    conn.close()
    return {"course_ids": course_ids}, 200

def get_instructors_by_course(course_id: int) -> tuple[dict[str, dict[int, Instructor]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.* FROM instructors i
        JOIN course_instructors ci ON i.id = ci.instructor_id
        WHERE ci.course_id = ?
    ''', (course_id,))
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = {}
    for instructor in instructors_data:
        instructor_courses, _ = get_instructor_course_ids_by_instructor_id(instructor['id'])
        instructors[instructor['id']] = Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id'], instructor_courses['course_ids'])
    return {"instructors": instructors}, 200

def search_instructors(search_type: str, search_term: str) -> tuple[dict[str, list[Instructor]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        if validator.validate_name(search_term):
            cursor.execute('SELECT * FROM instructors WHERE name = ?', (search_term,))
        else:
            conn.close()
            return {"message": "Invalid name"}, 400
    elif search_type == "email":
        if validator.validate_email(search_term):
            cursor.execute('SELECT * FROM instructors WHERE email = ?', (search_term,))
        else:
            conn.close()
            return {"message": "Invalid email"}, 400
    elif search_type == "id":
        cursor.execute('SELECT * FROM instructors WHERE id = ?', (int(search_term),))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = []
    for instructor in instructors_data:
        instructor_courses, _ = get_instructor_course_ids_by_instructor_id(instructor['id'])
        instructors.append(Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id'], instructor_courses['course_ids']))
    return {"instructors": instructors}, 200

def get_instructor_id_by_name(instructor_name: str) -> tuple[dict[str, int], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors WHERE name = ?', (instructor_name,))
    instructor = cursor.fetchone()
    if instructor is None:
        conn.close()
        return {"message": "Instructor not found"}, 404
    conn.close()
    return {"instructor_id": instructor['id']}, 200

def get_instructor_courses(courses_ids: list) -> tuple[dict[str, list[str]], int]:
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

def update_instructor(instructor_id: int, name: str, age: int, email: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if validator.validate_name(name) and validator.validate_email(email) and validator.validate_age(age):
            cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE id = ?', (name, age, email, instructor_id))
            conn.commit()
            if cursor.rowcount == 0:
                return {"message": "Instructor not found"}, 404
            return {"message": "Instructor updated successfully"}, 200
        return {"message": "Invalid name or email or age"}, 400
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()
