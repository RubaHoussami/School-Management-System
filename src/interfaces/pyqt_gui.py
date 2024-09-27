import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QComboBox, QFileDialog, 
                             QMessageBox, QDialog, QTabWidget, QListWidget, QTextEdit)
from PyQt5.QtCore import QTimer, Qt
from src.managers.data_manager import DataManager
from src.utils.file_controller import terminate

def boot_pyqt(database):
    if database:
        from src.utils.db_controller import (
            register_student, remove_student_from_course, register_instructor, remove_instructor_from_course, 
            add_course, add_student_to_course, add_instructor_to_course, remove_student, remove_instructor, 
            remove_course, get_students, get_instructors, get_courses, get_instructors_by_course, get_students_by_course,
            search_students, search_instructors, get_student_courses, get_instructor_courses, search_courses, backup_database, 
            initialize_database
        )
        initialize_database()
    else:
        from src.utils.file_controller import (
            register_student, remove_student_from_course, register_instructor, remove_instructor_from_course, 
            add_course, add_student_to_course, add_instructor_to_course, remove_student, remove_instructor, 
            remove_course, get_students, get_instructors, get_courses, get_instructors_by_course, get_students_by_course,
            search_students, search_instructors, get_student_courses, get_instructor_courses, search_courses, terminate
        )

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Student Management System")
            self.setGeometry(100, 100, 800, 600)

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.layout = QVBoxLayout(self.central_widget)

            self.tab_widget = QTabWidget()
            self.layout.addWidget(self.tab_widget)

            self.student_tab = QWidget()
            self.instructor_tab = QWidget()
            self.course_tab = QWidget()

            self.tab_widget.addTab(self.student_tab, "Students")
            self.tab_widget.addTab(self.instructor_tab, "Instructors")
            self.tab_widget.addTab(self.course_tab, "Courses")

            self.setup_student_tab()
            self.setup_instructor_tab()
            self.setup_course_tab()

            self.message_label = QLabel()
            self.layout.addWidget(self.message_label)

            self.timer = QTimer()
            self.timer.timeout.connect(self.clear_message)

            self.update_dropdowns()

            self.terminate_button = QPushButton("Terminate")
            self.terminate_button.clicked.connect(self.on_closing)
            self.layout.addWidget(self.terminate_button)


        def setup_student_tab(self):
            layout = QVBoxLayout(self.student_tab)

            register_layout = QHBoxLayout()
            layout.addLayout(register_layout)

            register_layout.addWidget(QLabel("Name:"))
            self.student_name_entry = QLineEdit()
            self.student_name_entry.textChanged.connect(self.validate_register_student_fields)
            register_layout.addWidget(self.student_name_entry)

            register_layout.addWidget(QLabel("Age:"))
            self.student_age_entry = QLineEdit()
            self.student_age_entry.textChanged.connect(self.validate_register_student_fields)
            register_layout.addWidget(self.student_age_entry)

            register_layout.addWidget(QLabel("Email:"))
            self.student_email_entry = QLineEdit()
            self.student_email_entry.textChanged.connect(self.validate_register_student_fields)
            register_layout.addWidget(self.student_email_entry)

            self.register_student_button = QPushButton("Register Student")
            self.register_student_button.clicked.connect(self.register_student_command)
            self.register_student_button.setEnabled(False)
            register_layout.addWidget(self.register_student_button)

            delete_layout = QHBoxLayout()
            layout.addLayout(delete_layout)

            delete_layout.addWidget(QLabel("Student ID:"))
            self.delete_student_id_entry = QLineEdit()
            self.delete_student_id_entry.textChanged.connect(self.validate_delete_student_fields)
            delete_layout.addWidget(self.delete_student_id_entry)

            self.delete_student_button = QPushButton("Delete Student")
            self.delete_student_button.clicked.connect(self.delete_student_command)
            self.delete_student_button.setEnabled(False)
            delete_layout.addWidget(self.delete_student_button)

            select_delete_layout = QHBoxLayout()
            layout.addLayout(select_delete_layout)

            self.select_delete_student_combo = QComboBox()
            self.select_delete_student_combo.currentTextChanged.connect(self.validate_select_delete_student_fields)
            select_delete_layout.addWidget(self.select_delete_student_combo)

            self.select_delete_student_button = QPushButton("Delete Selected Student")
            self.select_delete_student_button.clicked.connect(self.select_delete_student_command)
            self.select_delete_student_button.setEnabled(False)
            select_delete_layout.addWidget(self.select_delete_student_button)

            add_to_course_layout = QHBoxLayout()
            layout.addLayout(add_to_course_layout)

            self.select_student_combo = QComboBox()
            self.select_student_combo.currentTextChanged.connect(self.validate_select_add_student_to_course_fields)
            add_to_course_layout.addWidget(self.select_student_combo)

            self.select_course_combo = QComboBox()
            self.select_course_combo.currentTextChanged.connect(self.validate_select_add_student_to_course_fields)
            add_to_course_layout.addWidget(self.select_course_combo)

            self.add_student_to_course_button = QPushButton("Add Student to Course")
            self.add_student_to_course_button.clicked.connect(self.select_add_student_to_course_command)
            self.add_student_to_course_button.setEnabled(False)
            add_to_course_layout.addWidget(self.add_student_to_course_button)

            remove_from_course_layout = QHBoxLayout()
            layout.addLayout(remove_from_course_layout)

            self.select_student_remove_combo = QComboBox()
            self.select_student_remove_combo.currentTextChanged.connect(self.validate_select_remove_student_from_course_fields)
            remove_from_course_layout.addWidget(self.select_student_remove_combo)

            self.select_course_remove_combo = QComboBox()
            self.select_course_remove_combo.currentTextChanged.connect(self.validate_select_remove_student_from_course_fields)
            remove_from_course_layout.addWidget(self.select_course_remove_combo)

            self.remove_student_from_course_button = QPushButton("Remove Student from Course")
            self.remove_student_from_course_button.clicked.connect(self.select_remove_student_from_course_command)
            self.remove_student_from_course_button.setEnabled(False)
            remove_from_course_layout.addWidget(self.remove_student_from_course_button)

            search_layout = QHBoxLayout()
            layout.addLayout(search_layout)

            search_layout.addWidget(QLabel("Name:"))
            self.search_student_name_entry = QLineEdit()
            self.search_student_name_entry.textChanged.connect(self.validate_student_search_fields)
            search_layout.addWidget(self.search_student_name_entry)

            search_layout.addWidget(QLabel("ID:"))
            self.search_student_id_entry = QLineEdit()
            self.search_student_id_entry.textChanged.connect(self.validate_student_search_fields)
            search_layout.addWidget(self.search_student_id_entry)

            search_layout.addWidget(QLabel("Email:"))
            self.search_student_email_entry = QLineEdit()
            self.search_student_email_entry.textChanged.connect(self.validate_student_search_fields)
            search_layout.addWidget(self.search_student_email_entry)

            self.search_student_button = QPushButton("Search Students")
            self.search_student_button.clicked.connect(self.search_students_command)
            self.search_student_button.setEnabled(False)
            search_layout.addWidget(self.search_student_button)

            view_layout = QVBoxLayout()
            layout.addLayout(view_layout)

            self.view_students_list = QListWidget()
            view_layout.addWidget(self.view_students_list)

            self.view_students_button = QPushButton("View All Students")
            self.view_students_button.clicked.connect(self.view_students)
            view_layout.addWidget(self.view_students_button)

        def setup_instructor_tab(self):
            layout = QVBoxLayout(self.instructor_tab)

            register_layout = QHBoxLayout()
            layout.addLayout(register_layout)

            register_layout.addWidget(QLabel("Name:"))
            self.instructor_name_entry = QLineEdit()
            self.instructor_name_entry.textChanged.connect(self.validate_register_instructor_fields)
            register_layout.addWidget(self.instructor_name_entry)

            register_layout.addWidget(QLabel("Age:"))
            self.instructor_age_entry = QLineEdit()
            self.instructor_age_entry.textChanged.connect(self.validate_register_instructor_fields)
            register_layout.addWidget(self.instructor_age_entry)

            register_layout.addWidget(QLabel("Email:"))
            self.instructor_email_entry = QLineEdit()
            self.instructor_email_entry.textChanged.connect(self.validate_register_instructor_fields)
            register_layout.addWidget(self.instructor_email_entry)

            self.register_instructor_button = QPushButton("Register Instructor")
            self.register_instructor_button.clicked.connect(self.register_instructor_command)
            self.register_instructor_button.setEnabled(False)
            register_layout.addWidget(self.register_instructor_button)

            delete_layout = QHBoxLayout()
            layout.addLayout(delete_layout)

            delete_layout.addWidget(QLabel("Instructor ID:"))
            self.delete_instructor_id_entry = QLineEdit()
            self.delete_instructor_id_entry.textChanged.connect(self.validate_delete_instructor_fields)
            delete_layout.addWidget(self.delete_instructor_id_entry)

            self.delete_instructor_button = QPushButton("Delete Instructor")
            self.delete_instructor_button.clicked.connect(self.delete_instructor_command)
            self.delete_instructor_button.setEnabled(False)
            delete_layout.addWidget(self.delete_instructor_button)

            select_delete_layout = QHBoxLayout()
            layout.addLayout(select_delete_layout)

            self.select_delete_instructor_combo = QComboBox()
            self.select_delete_instructor_combo.currentTextChanged.connect(self.validate_select_delete_instructor_fields)
            select_delete_layout.addWidget(self.select_delete_instructor_combo)

            self.select_delete_instructor_button = QPushButton("Delete Selected Instructor")
            self.select_delete_instructor_button.clicked.connect(self.select_delete_instructor_command)
            self.select_delete_instructor_button.setEnabled(False)
            select_delete_layout.addWidget(self.select_delete_instructor_button)

            add_to_course_layout = QHBoxLayout()
            layout.addLayout(add_to_course_layout)

            self.select_instructor_combo = QComboBox()
            self.select_instructor_combo.currentTextChanged.connect(self.validate_select_add_instructor_to_course_fields)
            add_to_course_layout.addWidget(self.select_instructor_combo)

            self.select_course_instructor_combo = QComboBox()
            self.select_course_instructor_combo.currentTextChanged.connect(self.validate_select_add_instructor_to_course_fields)
            add_to_course_layout.addWidget(self.select_course_instructor_combo)

            self.add_instructor_to_course_button = QPushButton("Add Instructor to Course")
            self.add_instructor_to_course_button.clicked.connect(self.select_add_instructor_to_course_command)
            self.add_instructor_to_course_button.setEnabled(False)
            add_to_course_layout.addWidget(self.add_instructor_to_course_button)

            remove_from_course_layout = QHBoxLayout()
            layout.addLayout(remove_from_course_layout)

            self.select_instructor_remove_combo = QComboBox()
            self.select_instructor_remove_combo.currentTextChanged.connect(self.validate_select_remove_instructor_from_course_fields)
            remove_from_course_layout.addWidget(self.select_instructor_remove_combo)

            self.select_course_instructor_remove_combo = QComboBox()
            self.select_course_instructor_remove_combo.currentTextChanged.connect(self.validate_select_remove_instructor_from_course_fields)
            remove_from_course_layout.addWidget(self.select_course_instructor_remove_combo)

            self.remove_instructor_from_course_button = QPushButton("Remove Instructor from Course")
            self.remove_instructor_from_course_button.clicked.connect(self.select_remove_instructor_from_course_command)
            self.remove_instructor_from_course_button.setEnabled(False)
            remove_from_course_layout.addWidget(self.remove_instructor_from_course_button)

            search_layout = QHBoxLayout()
            layout.addLayout(search_layout)

            search_layout.addWidget(QLabel("Name:"))
            self.search_instructor_name_entry = QLineEdit()
            self.search_instructor_name_entry.textChanged.connect(self.validate_instructor_search_fields)
            search_layout.addWidget(self.search_instructor_name_entry)

            search_layout.addWidget(QLabel("ID:"))
            self.search_instructor_id_entry = QLineEdit()
            self.search_instructor_id_entry.textChanged.connect(self.validate_instructor_search_fields)
            search_layout.addWidget(self.search_instructor_id_entry)

            search_layout.addWidget(QLabel("Email:"))
            self.search_instructor_email_entry = QLineEdit()
            self.search_instructor_email_entry.textChanged.connect(self.validate_instructor_search_fields)
            search_layout.addWidget(self.search_instructor_email_entry)

            self.search_instructor_button = QPushButton("Search Instructors")
            self.search_instructor_button.clicked.connect(self.search_instructors_command)
            self.search_instructor_button.setEnabled(False)
            search_layout.addWidget(self.search_instructor_button)

            view_layout = QVBoxLayout()
            layout.addLayout(view_layout)

            self.view_instructors_list = QListWidget()
            view_layout.addWidget(self.view_instructors_list)

            self.view_instructors_button = QPushButton("View All Instructors")
            self.view_instructors_button.clicked.connect(self.view_instructors)
            view_layout.addWidget(self.view_instructors_button)

        def setup_course_tab(self):
            layout = QVBoxLayout(self.course_tab)

            add_course_layout = QHBoxLayout()
            layout.addLayout(add_course_layout)

            add_course_layout.addWidget(QLabel("Course Name:"))
            self.add_course_name_entry = QLineEdit()
            self.add_course_name_entry.textChanged.connect(self.validate_add_course_fields)
            add_course_layout.addWidget(self.add_course_name_entry)

            add_course_layout.addWidget(QLabel("Description:"))
            self.add_course_description_entry = QTextEdit()
            self.add_course_description_entry.textChanged.connect(self.validate_add_course_fields)
            add_course_layout.addWidget(self.add_course_description_entry)

            self.add_course_button = QPushButton("Add Course")
            self.add_course_button.clicked.connect(self.add_course_command)
            self.add_course_button.setEnabled(False)
            add_course_layout.addWidget(self.add_course_button)

            delete_course_layout = QHBoxLayout()
            layout.addLayout(delete_course_layout)

            delete_course_layout.addWidget(QLabel("Course ID:"))
            self.remove_course_id_entry = QLineEdit()
            self.remove_course_id_entry.textChanged.connect(self.validate_remove_course_fields)
            delete_course_layout.addWidget(self.remove_course_id_entry)

            self.remove_course_button = QPushButton("Delete Course")
            self.remove_course_button.clicked.connect(self.remove_course_command)
            self.remove_course_button.setEnabled(False)
            delete_course_layout.addWidget(self.remove_course_button)

            select_delete_course_layout = QHBoxLayout()
            layout.addLayout(select_delete_course_layout)

            self.select_delete_course_combo = QComboBox()
            self.select_delete_course_combo.currentTextChanged.connect(self.validate_select_delete_course_fields)
            select_delete_course_layout.addWidget(self.select_delete_course_combo)

            self.select_delete_course_button = QPushButton("Delete Selected Course")
            self.select_delete_course_button.clicked.connect(self.select_delete_course_command)
            self.select_delete_course_button.setEnabled(False)
            select_delete_course_layout.addWidget(self.select_delete_course_button)

            view_course_layout = QVBoxLayout()
            layout.addLayout(view_course_layout)

            self.course_listbox = QListWidget()
            view_course_layout.addWidget(self.course_listbox)

            self.populate_courses_button = QPushButton("View All Courses")
            self.populate_courses_button.clicked.connect(self.populate_courses)
            view_course_layout.addWidget(self.populate_courses_button)

            course_details_layout = QVBoxLayout()
            layout.addLayout(course_details_layout)

            course_details_layout.addWidget(QLabel("Course Details"))

            self.course_details_text = QTextEdit()
            self.course_details_text.setReadOnly(True)
            course_details_layout.addWidget(self.course_details_text)

        def on_closing(self):
            if database:
                backup_window = BackupDatabaseWindow(self)
                result = backup_window.exec_()
                if result == QDialog.Accepted:
                    QApplication.quit()
                else:
                    return
            else:
                save_window = SaveSessionWindow(self)
                result = save_window.exec_()
                if result == QDialog.Accepted:
                    QApplication.quit()
                else:
                    return

        def save_session_as(self, format):
            if not database:
                current_dir = os.getcwd()
                data_manager = DataManager(current_dir)
                students, instructors, courses = terminate()
                if format == "pickle":
                    data_manager.pickle_data(students, instructors, courses)
                elif format == "csv":
                    data_manager.save_to_csv(students, instructors, courses)
                elif format == "json":
                    data_manager.save_to_json(students, instructors, courses)
                QMessageBox.information(self, "Success", f"Session saved as {format}.")
            else:
                save_window = SaveSessionWindow(self)
                result = save_window.exec_()
                if result == QDialog.Accepted:
                    if save_window.should_quit:
                        QApplication.quit()
                else:
                    return

        def clear_message(self):
            self.message_label.clear()

        def update_dropdowns(self):
            student_options = self.get_student_options()
            course_options = self.get_course_options()
            instructor_options = self.get_instructor_options()

            self.select_student_combo.clear()
            self.select_student_combo.addItems(student_options)
            self.select_student_remove_combo.clear()
            self.select_student_remove_combo.addItems(student_options)
            self.select_delete_student_combo.clear()
            self.select_delete_student_combo.addItems(student_options)

            self.select_course_combo.clear()
            self.select_course_combo.addItems(course_options)
            self.select_course_remove_combo.clear()
            self.select_course_remove_combo.addItems(course_options)
            self.select_course_instructor_combo.clear()
            self.select_course_instructor_combo.addItems(course_options)
            self.select_course_instructor_remove_combo.clear()
            self.select_course_instructor_remove_combo.addItems(course_options)
            self.select_delete_course_combo.clear()
            self.select_delete_course_combo.addItems(course_options)

            self.select_instructor_combo.clear()
            self.select_instructor_combo.addItems(instructor_options)
            self.select_instructor_remove_combo.clear()
            self.select_instructor_remove_combo.addItems(instructor_options)
            self.select_delete_instructor_combo.clear()
            self.select_delete_instructor_combo.addItems(instructor_options)

        def get_student_options(self):
            students, _ = get_students()
            return [f"{student.name}: {student.student_id}" for student in students['students'].values()]

        def get_course_options(self):
            courses, _ = get_courses()
            return [f"{course.name}: {course.course_id}" for course in courses['courses'].values()]

        def get_instructor_options(self):
            instructors, _ = get_instructors()
            return [f"{instructor.name}: {instructor.instructor_id}" for instructor in instructors['instructors'].values()]

        def show_message(self, message, color):
            self.message_label.setText(message)
            self.message_label.setStyleSheet(f"color: {color}")
            self.timer.start(4000)

        def validate_register_student_fields(self):
            if self.student_name_entry.text() and self.student_age_entry.text() and self.student_email_entry.text():
                self.register_student_button.setEnabled(True)
            else:
                self.register_student_button.setEnabled(False)

        def validate_delete_student_fields(self):
            if self.delete_student_id_entry.text():
                self.delete_student_button.setEnabled(True)
            else:
                self.delete_student_button.setEnabled(False)

        def validate_select_delete_student_fields(self):
            if self.select_delete_student_combo.currentText():
                self.select_delete_student_button.setEnabled(True)
            else:
                self.select_delete_student_button.setEnabled(False)

        def validate_select_add_student_to_course_fields(self):
            if self.select_student_combo.currentText() and self.select_course_combo.currentText():
                self.add_student_to_course_button.setEnabled(True)
            else:
                self.add_student_to_course_button.setEnabled(False)

        def validate_select_remove_student_from_course_fields(self):
            if self.select_student_remove_combo.currentText() and self.select_course_remove_combo.currentText():
                self.remove_student_from_course_button.setEnabled(True)
            else:
                self.remove_student_from_course_button.setEnabled(False)

        def validate_register_instructor_fields(self):
            if self.instructor_name_entry.text() and self.instructor_age_entry.text() and self.instructor_email_entry.text():
                self.register_instructor_button.setEnabled(True)
            else:
                self.register_instructor_button.setEnabled(False)

        def validate_delete_instructor_fields(self):
            if self.delete_instructor_id_entry.text():
                self.delete_instructor_button.setEnabled(True)
            else:
                self.delete_instructor_button.setEnabled(False)

        def validate_select_delete_instructor_fields(self):
            if self.select_delete_instructor_combo.currentText():
                self.select_delete_instructor_button.setEnabled(True)
            else:
                self.select_delete_instructor_button.setEnabled(False)

        def validate_select_add_instructor_to_course_fields(self):
            if self.select_instructor_combo.currentText() and self.select_course_instructor_combo.currentText():
                self.add_instructor_to_course_button.setEnabled(True)
            else:
                self.add_instructor_to_course_button.setEnabled(False)

        def validate_select_remove_instructor_from_course_fields(self):
            if self.select_instructor_remove_combo.currentText() and self.select_course_instructor_remove_combo.currentText():
                self.remove_instructor_from_course_button.setEnabled(True)
            else:
                self.remove_instructor_from_course_button.setEnabled(False)

        def validate_add_course_fields(self):
            if self.add_course_name_entry.text():
                self.add_course_button.setEnabled(True)
            else:
                self.add_course_button.setEnabled(False)

        def validate_remove_course_fields(self):
            if self.remove_course_id_entry.text():
                self.remove_course_button.setEnabled(True)
            else:
                self.remove_course_button.setEnabled(False)

        def validate_select_delete_course_fields(self):
            if self.select_delete_course_combo.currentText():
                self.select_delete_course_button.setEnabled(True)
            else:
                self.select_delete_course_button.setEnabled(False)

        def validate_student_search_fields(self):
            if self.search_student_name_entry.text() or self.search_student_id_entry.text() or self.search_student_email_entry.text():
                self.search_student_button.setEnabled(True)
            else:
                self.search_student_button.setEnabled(False)

        def validate_instructor_search_fields(self):
            if self.search_instructor_name_entry.text() or self.search_instructor_id_entry.text() or self.search_instructor_email_entry.text():
                self.search_instructor_button.setEnabled(True)
            else:
                self.search_instructor_button.setEnabled(False)

        def register_student_command(self):
            name = self.student_name_entry.text().strip()
            age = self.student_age_entry.text()
            email = self.student_email_entry.text().strip()
            message, status = register_student(name, int(age), email)

            if status == 200:
                self.student_name_entry.clear()
                self.student_age_entry.clear()
                self.student_email_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def delete_student_command(self):
            student_id = self.delete_student_id_entry.text()
            message, status = remove_student(int(student_id))

            if status == 200:
                self.delete_student_id_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def select_delete_student_command(self):
            student_id = self.select_delete_student_combo.currentText().split(":")[1].strip()
            message, status = remove_student(int(student_id))

            if status == 200:
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def select_add_student_to_course_command(self):
            student_id = self.select_student_combo.currentText().split(":")[1].strip()
            course_id = self.select_course_combo.currentText().split(":")[1].strip()
            message, status = add_student_to_course(int(student_id), int(course_id))

            if status == 200:
                self.show_message(message["message"], "green")
            else:
                self.show_message(message["message"], "red")

        def select_remove_student_from_course_command(self):
            student_id = self.select_student_remove_combo.currentText().split(":")[1].strip()
            course_id = self.select_course_remove_combo.currentText().split(":")[1].strip()
            message, status = remove_student_from_course(int(student_id), int(course_id))

            if status == 200:
                self.show_message(message["message"], "green")
            else:
                self.show_message(message["message"], "red")

        def register_instructor_command(self):
            name = self.instructor_name_entry.text().strip()
            age = self.instructor_age_entry.text()
            email = self.instructor_email_entry.text().strip()
            message, status = register_instructor(name, int(age), email)

            if status == 200:
                self.instructor_name_entry.clear()
                self.instructor_age_entry.clear()
                self.instructor_email_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def delete_instructor_command(self):
            instructor_id = self.delete_instructor_id_entry.text()
            message, status = remove_instructor(int(instructor_id))

            if status == 200:
                self.delete_instructor_id_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def select_delete_instructor_command(self):
            instructor_id = self.select_delete_instructor_combo.currentText().split(":")[1].strip()
            message, status = remove_instructor(int(instructor_id))

            if status == 200:
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def select_add_instructor_to_course_command(self):
            instructor_id = self.select_instructor_combo.currentText().split(":")[1].strip()
            course_id = self.select_course_instructor_combo.currentText().split(":")[1].strip()
            message, status = add_instructor_to_course(int(instructor_id), int(course_id))

            if status == 200:
                self.show_message(message["message"], "green")
            else:
                self.show_message(message["message"], "red")

        def select_remove_instructor_from_course_command(self):
            instructor_id = self.select_instructor_remove_combo.currentText().split(":")[1].strip()
            course_id = self.select_course_instructor_remove_combo.currentText().split(":")[1].strip()
            message, status = remove_instructor_from_course(int(instructor_id), int(course_id))

            if status == 200:
                self.show_message(message["message"], "green")
            else:
                self.show_message(message["message"], "red")

        def add_course_command(self):
            name = self.add_course_name_entry.text().strip()
            description = self.add_course_description_entry.toPlainText().strip()
            message, status = add_course(name, description)

            if status == 200:
                self.add_course_name_entry.clear()
                self.add_course_description_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def remove_course_command(self):
            course_id = self.remove_course_id_entry.text()
            message, status = remove_course(int(course_id))

            if status == 200:
                self.remove_course_id_entry.clear()
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def select_delete_course_command(self):
            course_id = self.select_delete_course_combo.currentText().split(":")[1].strip()
            message, status = remove_course(int(course_id))

            if status == 200:
                self.show_message(message["message"], "green")
                self.update_dropdowns()
            else:
                self.show_message(message["message"], "red")

        def view_students(self):
            students, status = get_students()
            self.view_students_list.clear()
            
            if status == 200 and students:
                for student in students['students'].values():
                    courses = get_student_courses(student.student_id)
                    course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                    self.view_students_list.addItem(f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                    self.view_students_list.addItem(f"Courses: {course_names}")
                    self.view_students_list.addItem("")
                self.show_message("Students retrieved successfully", "green")
            else:
                self.show_message("No students found", "red")

        def view_instructors(self):
            instructors, status = get_instructors()
            self.view_instructors_list.clear()
            
            if status == 200 and instructors:
                for instructor in instructors['instructors'].values():
                    courses = get_instructor_courses(instructor.instructor_id)
                    course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                    self.view_instructors_list.addItem(f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                    self.view_instructors_list.addItem(f"Courses: {course_names}")
                    self.view_instructors_list.addItem("")
                self.show_message("Instructors retrieved successfully", "green")
            else:
                self.show_message("No instructors found", "red")

        def populate_courses(self):
            courses, status = get_courses()
            self.course_listbox.clear()
            
            if status == 200 and courses:
                for course in courses['courses'].values():
                    self.course_listbox.addItem(f"{course.name}: {course.course_id}")
                self.show_message("Courses retrieved successfully", "green")
            else:
                self.show_message("No courses found", "red")

        def search_students_command(self):
            name = self.search_student_name_entry.text().strip()
            student_id = self.search_student_id_entry.text().strip()
            email = self.search_student_email_entry.text().strip()
            
            students, status = search_students(name, student_id, email)
            self.view_students_list.clear()
            
            if status == 200 and students:
                for student in students['students']:
                    courses = get_student_courses(student.student_id)
                    course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                    self.view_students_list.addItem(f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                    self.view_students_list.addItem(f"Courses: {course_names}")
                    self.view_students_list.addItem("")
                self.show_message("Students found", "green")
            else:
                self.show_message("No students found", "red")

        def search_instructors_command(self):
            name = self.search_instructor_name_entry.text().strip()
            instructor_id = self.search_instructor_id_entry.text().strip()
            email = self.search_instructor_email_entry.text().strip()
            
            instructors, status = search_instructors(name, instructor_id, email)
            self.view_instructors_list.clear()
            
            if status == 200 and instructors:
                for instructor in instructors['instructors']:
                    courses = get_instructor_courses(instructor.instructor_id)
                    course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                    self.view_instructors_list.addItem(f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                    self.view_instructors_list.addItem(f"Courses: {course_names}")
                    self.view_instructors_list.addItem("")
                self.show_message("Instructors found", "green")
            else:
                self.show_message("No instructors found", "red")

    class SaveSessionWindow(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.should_quit = False
            self.initUI()

        def initUI(self):
            self.setWindowTitle("Save Session")
            self.setGeometry(100, 100, 400, 250)
            
            layout = QVBoxLayout()

            label = QLabel("Save session as:")
            layout.addWidget(label)

            self.save_format = QComboBox()
            self.save_format.addItems(["csv", "json", "pickle"])
            self.save_format.setCurrentIndex(-1)  # No default selection
            self.save_format.currentIndexChanged.connect(self.enable_save_button)
            layout.addWidget(self.save_format)

            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(self.save_and_close)
            self.save_button.setEnabled(False)  # Disabled by default
            layout.addWidget(self.save_button)

            info_label1 = QLabel("This session will be restored the next time you start the app.")
            info_label1.setWordWrap(True)
            info_label1.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label1)

            info_label2 = QLabel("Please note that any previous sessions found will be deleted.")
            info_label2.setWordWrap(True)
            info_label2.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label2)

            button_layout = QHBoxLayout()
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)

            no_button = QPushButton("No")
            no_button.clicked.connect(self.close_without_saving)
            button_layout.addWidget(no_button)

            layout.addLayout(button_layout)

            self.setLayout(layout)

        def enable_save_button(self, index):
            self.save_button.setEnabled(index != -1)

        def save_and_close(self):
            format = self.save_format.currentText()
            if format:
                self.parent.save_session_as(format)
                self.should_quit = True
                self.accept()

        def close_without_saving(self):
            self.should_quit = True
            self.accept()

    class BackupDatabaseWindow(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.should_quit = False
            self.initUI()
        def initUI(self):
            self.setWindowTitle("Backup Database")
            self.setGeometry(100, 100, 400, 300)

            layout = QVBoxLayout()

            label = QLabel("Backup Database")
            label.setStyleSheet("font-size: 14pt; font-weight: bold;")
            layout.addWidget(label)

            self.path_label = QLabel("Select backup path:")
            layout.addWidget(self.path_label)

            path_layout = QHBoxLayout()
            self.path_entry = QLineEdit()
            self.path_entry.setReadOnly(True)
            path_layout.addWidget(self.path_entry)

            browse_button = QPushButton("Browse")
            browse_button.clicked.connect(self.browse_path)
            path_layout.addWidget(browse_button)

            layout.addLayout(path_layout)

            button_layout = QHBoxLayout()
            self.backup_button = QPushButton("Backup")
            self.backup_button.clicked.connect(self.perform_backup)
            self.backup_button.setEnabled(False)
            button_layout.addWidget(self.backup_button)

            no_button = QPushButton("No")
            no_button.clicked.connect(self.no_backup)
            button_layout.addWidget(no_button)

            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)

            self.setLayout(layout)

        def browse_path(self):
            folder_selected = QFileDialog.getExistingDirectory(self, "Select Backup Directory")
            if folder_selected:
                self.path_entry.setText(folder_selected)
                self.backup_button.setEnabled(True)

        def perform_backup(self):
            if self.path_entry.text():
                backup_database(self.path_entry.text())
            self.should_quit = True
            self.accept()

        def no_backup(self):
            self.should_quit = True
            self.accept()

    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
