import pickle
import os
import json
import csv

from src.components.instructor import Instructor
from src.components.student import Student
from src.components.course import Course

class DataManager:
    def __init__(self, path: str):
        assert os.path.isdir(path), 'The path specified is not a folder.'
        self.path = path

    def pickle_data(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function pickles the data to the specified path into 'data.pkl' file.
        """
        cvs_path = os.path.join(self.path, 'data.cvs')
        json_path = os.path.join(self.path, 'data.json')
        
        if os.path.isfile(cvs_path):
            os.remove(cvs_path)
        
        if os.path.isfile(json_path):
            os.remove(json_path)

        with open(os.path.join(self.path, 'data.pkl'), 'wb') as file:
            pickle.dump(students, file)
            pickle.dump(instructors, file)
            pickle.dump(courses, file)

    def unpickle_data(self) -> tuple:
        """
        This function unpickles the data from the specified path from 'data.pkl' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.pkl')), 'The path specified does not contain a file named data.pkl.'
        with open(os.path.join(self.path, 'data.pkl'), 'rb') as file:
            students = pickle.load(file)
            instructors = pickle.load(file)
            courses = pickle.load(file)
        return students, instructors, courses

    def save_to_csv(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function saves the data to the specified path into 'data.csv' file.
        """
        pkl_path = os.path.join(self.path, 'data.pkl')
        json_path = os.path.join(self.path, 'data.json')
        
        if os.path.isfile(pkl_path):
            os.remove(pkl_path)
        
        if os.path.isfile(json_path):
            os.remove(json_path)

        with open(os.path.join(self.path, 'data.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'ID', 'Name', 'Age', 'Email', 'Courses/Description', 'Students', 'Instructors'])
            
            for course in courses.values():
                course_students = json.dumps({str(s_id): s.__dict__ for s_id, s in course.students.items()})
                course_instructors = json.dumps({str(i_id): i.__dict__ for i_id, i in course.instructors.items()})
                writer.writerow(['Course', course.course_id, course.name, '', '', course.description, course_students, course_instructors])
            
            for student in students.values():
                writer.writerow(['Student', student.student_id, student.name, student.age, student._email, ','.join(map(str, student.registered_courses)), '', ''])
            
            for instructor in instructors.values():
                writer.writerow(['Instructor', instructor.instructor_id, instructor.name, instructor.age, instructor._email, ','.join(map(str, instructor.registered_courses)), '', ''])

    def load_from_csv(self) -> tuple:
        """
        This function loads the data from the specified path from 'data.csv' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.csv')), 'The path specified does not contain a file named data.csv.'
        students = {}
        instructors = {}
        courses = {}
        
        with open(os.path.join(self.path, 'data.csv'), 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == 'Course':
                    course_id = int(row[1])
                    course_students = json.loads(row[6]) if row[6] else {}
                    course_instructors = json.loads(row[7]) if row[7] else {}
                    courses[course_id] = Course(row[2], row[5], course_id, 
                                                {int(s_id): Student(**s_data) for s_id, s_data in course_students.items()},
                                                {int(i_id): Instructor(**i_data) for i_id, i_data in course_instructors.items()})
                elif row[0] == 'Student':
                    student_id = int(row[1])
                    registered_courses = list(map(int, row[5].split(','))) if row[5] else []
                    students[student_id] = Student(row[2], int(row[3]), row[4], student_id, registered_courses)
                elif row[0] == 'Instructor':
                    instructor_id = int(row[1])
                    registered_courses = list(map(int, row[5].split(','))) if row[5] else []
                    instructors[instructor_id] = Instructor(row[2], int(row[3]), row[4], instructor_id, registered_courses)

        return students, instructors, courses

    def save_to_json(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function saves the data to the specified path into 'data.json' file.
        """
        
        pkl_path = os.path.join(self.path, 'data.pkl')
        csv_path = os.path.join(self.path, 'data.csv')
        
        if os.path.isfile(pkl_path):
            os.remove(pkl_path)
        
        if os.path.isfile(csv_path):
            os.remove(csv_path)

        with open(os.path.join(self.path, 'data.json'), 'w') as file:
            json.dump(students, file, default=lambda x: x.__dict__)
            file.write('\n')
            json.dump(instructors, file, default=lambda x: x.__dict__)
            file.write('\n')
            json.dump(courses, file, default=lambda x: x.__dict__)

    def load_from_json(self) -> tuple:
        """
        This function loads the data from the specified path from 'data.json' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.json')), 'The path specified does not contain a file named data.json.'
        with open(os.path.join(self.path, 'data.json'), 'r') as file:
            data = file.read().split('\n')

            students_data = json.loads(data[0])
            students = {}
            for student_id in students_data:
                student = students_data[student_id]
                students[int(student_id)] = Student(student['name'], int(student['age']), student['_email'], int(student['student_id']), student['registered_courses'])
            
            instructors_data = json.loads(data[1])
            instructors = {}
            for instructor_id in instructors_data:
                instructor = instructors_data[instructor_id]
                instructors[int(instructor_id)] = Instructor(instructor['name'], int(instructor['age']), instructor['_email'], int(instructor['instructor_id']), instructor['registered_courses'])
            
            courses_data = json.loads(data[2])
            courses = {}
            for course_id in courses_data:
                course = courses_data[course_id]

                course_students = {}
                for student_id in course['students']:
                    student = course['students'][student_id]
                    course_students[int(student_id)] = Student(student['name'], int(student['age']), student['_email'], int(student['student_id']), student['registered_courses'])
                course_instructors = {}
                for instructor_id in course['instructors']:
                    instructor = course['instructors'][instructor_id]
                    course_instructors[int(instructor_id)] = Instructor(instructor['name'], int(instructor['age']), instructor['_email'], int(instructor['instructor_id']), instructor['registered_courses'])
                courses[int(course_id)] = Course(course['name'], course['description'], int(course['course_id']), course_students, course_instructors)

        return students, instructors, courses

    def boot(self) -> tuple:
        """
        This function boots the data from the specified path.
        """
        if os.path.isfile(os.path.join(self.path, 'data.pkl')):
            return self.unpickle_data()
        elif os.path.isfile(os.path.join(self.path, 'data.csv')):
            return self.load_from_csv()
        elif os.path.isfile(os.path.join(self.path, 'data.json')):
            return self.load_from_json()
        return {}, {}, {}
