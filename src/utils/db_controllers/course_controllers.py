from src.components.course import Course
from src.utils.db_controllers.general_controllers import get_db_connection
from src.utils.db_controllers.instructor_controllers import get_instructors_by_course
from src.utils.db_controllers.student_controllers import get_students_by_course

def add_course(name: str, description: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO courses (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    return {"message": f'Course added successfully', "course_id": course_id}, 200

def remove_course(course_id: int) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"message": "Course deleted successfully"}, 200

def get_courses() -> tuple[dict[str, dict[int, Course]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    courses_list = {}
    for course in courses:
        students, _ = get_students_by_course(course['id'])
        instructors, _ = get_instructors_by_course(course['id'])
        courses_list[course['id']] = Course(course['name'], course['description'], course['id'], students['students'], instructors['instructors'])
    return {"courses": courses_list}, 200

def get_course_id_by_name(course_name: str) -> tuple[dict[str, int], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE name = ?', (course_name,))
    course = cursor.fetchone()
    if course is None:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"course_id": course['id']}, 200

def search_courses(search_type: str, search_term: str) -> tuple[dict[str, list[Course]], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        cursor.execute('SELECT * FROM courses WHERE name LIKE ?', (search_term.lower(),))
    elif search_type == "id":
        cursor.execute('SELECT * FROM courses WHERE id = ?', (int(search_term),))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    courses = cursor.fetchall()
    conn.close()
    courses_list = []
    for course in courses:
        students, _ = get_students_by_course(course['id'])
        instructors, _ = get_instructors_by_course(course['id'])
        courses_list.append(Course(course['name'], course['description'], course['id'], students['students'], instructors['instructors']))
    return {"courses": courses_list}, 200

def update_course(course_id: int, name: str, description: str) -> tuple[dict[str, str], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET name = ?, description = ? WHERE id = ?', (name, description, course_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"message": "Course updated successfully"}, 200
