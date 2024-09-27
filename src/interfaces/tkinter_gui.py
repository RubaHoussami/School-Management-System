import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from src.managers.data_manager import DataManager


def boot_tkinter(database):
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

    def save_session_as(format):
        directory = os.getcwd()
        data_manager = DataManager(directory)
        students, instructors, courses = terminate()
        if format == "pickle":
            data_manager.pickle_data(students, instructors, courses)
        elif format == "csv":
            data_manager.save_to_csv(students, instructors, courses)
        elif format == "json":
            data_manager.save_to_json(students, instructors, courses)

    def on_closing():
        def save_and_close():
            format = save_format.get()
            if format:
                save_session_as(format)
                root.quit()

        def close_without_saving():
            root.quit()

        def enable_save_button(event):
            save_button.config(state=tk.NORMAL)

        save_window = tk.Toplevel(root)
        save_window.title("Save Session")
        save_window.geometry("400x250")

        tk.Label(save_window, text="Save session as:").pack(pady=10)
        save_format = ttk.Combobox(save_window, values=["csv", "json", "pickle"], state="readonly")
        save_format.pack(pady=5)

        save_button = tk.Button(save_window, text="Save", command=save_and_close, state=tk.DISABLED)
        save_button.pack(pady=10)

        info_frame = tk.Frame(save_window)
        info_frame.pack(pady=10)

        tk.Label(info_frame, text="This session will be restored the next time you start the app.", wraplength=350, justify="center").pack()
        tk.Label(info_frame, text="Please note that any previous sessions found will be deleted.", wraplength=350, justify="center").pack(pady=5)

        save_format.bind("<<ComboboxSelected>>", enable_save_button)

        button_frame = tk.Frame(save_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="Cancel", command=save_window.destroy).pack(side=tk.LEFT, padx=20)
        tk.Button(button_frame, text="No", command=close_without_saving).pack(side=tk.RIGHT, padx=20)

    def db_on_closing():
        global should_quit

        def perform_backup():
            if backup_path.get():
                backup_database(backup_path.get())
            global should_quit
            should_quit = True
            backup_window.destroy()

        def no_backup():
            global should_quit
            should_quit = True
            backup_window.destroy()

        def cancel():
            backup_window.destroy()

        backup_window = tk.Toplevel(root)
        backup_window.title("Backup Database")
        backup_window.geometry("400x300")

        tk.Label(backup_window, text="Backup Database", font=('Helvetica', 14, 'bold')).pack(pady=10)

        tk.Label(backup_window, text="Select backup path:").pack(pady=5)
        backup_path = tk.StringVar()
        path_entry = tk.Entry(backup_window, textvariable=backup_path, width=50, state='readonly')
        path_entry.pack(pady=5)

        def browse_path():
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                backup_path.set(folder_selected)
                backup_button.config(state=tk.NORMAL)

        browse_button = tk.Button(backup_window, text="Browse", command=browse_path)
        browse_button.pack(pady=5)

        button_frame = tk.Frame(backup_window)
        button_frame.pack(pady=20)

        backup_button = tk.Button(button_frame, text="Backup", command=perform_backup, state=tk.DISABLED)
        backup_button.grid(row=0, column=0, padx=10)

        no_button = tk.Button(button_frame, text="No", command=no_backup)
        no_button.grid(row=0, column=1, padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", command=cancel)
        cancel_button.grid(row=0, column=2, padx=10)

        backup_window.protocol("WM_DELETE_WINDOW", cancel)
        backup_window.transient(root)
        backup_window.grab_set()
        root.wait_window(backup_window)

        if should_quit:
            root.quit()

    def validate_register_student_fields():
        if student_name.get() and student_age.get() and student_email.get():
            register_student_button.config(state=tk.NORMAL)
        else:
            register_student_button.config(state=tk.DISABLED)

    def validate_add_student_to_course_fields():
        if add_student_id.get() and add_student_course_id.get():
            add_student_to_course_button.config(state=tk.NORMAL)
        else:
            add_student_to_course_button.config(state=tk.DISABLED)

    def validate_select_add_student_to_course_fields():
        if select_student.get() and select_course.get():
            select_add_student_to_course_button.config(state=tk.NORMAL)
        else:
            select_add_student_to_course_button.config(state=tk.DISABLED)

    def validate_remove_student_from_course_fields():
        if remove_student_id.get() and remove_student_course_id.get():
            remove_student_from_course_button.config(state=tk.NORMAL)
        else:
            remove_student_from_course_button.config(state=tk.DISABLED)

    def validate_register_instructor_fields():
        if instructor_name.get() and instructor_age.get() and instructor_email.get():
            register_instructor_button.config(state=tk.NORMAL)
        else:
            register_instructor_button.config(state=tk.DISABLED)

    def validate_add_instructor_to_course_fields():
        if add_instructor_id.get() and add_instructor_course_id.get():
            add_instructor_to_course_button.config(state=tk.NORMAL)
        else:
            add_instructor_to_course_button.config(state=tk.DISABLED)

    def validate_remove_instructor_from_course_fields():
        if remove_instructor_id_entry.get() and remove_instructor_course_id.get():
            remove_instructor_from_course_button.config(state=tk.NORMAL)
        else:
            remove_instructor_from_course_button.config(state=tk.DISABLED)

    def validate_add_course_fields():
        if add_course_name.get():
            add_course_button.config(state=tk.NORMAL)
        else:
            add_course_button.config(state=tk.DISABLED)
    
    def validate_remove_course_fields():
        if remove_course_id.get():
            remove_course_button.config(state=tk.NORMAL)
        else:
            remove_course_button.config(state=tk.DISABLED)

    def validate_select_remove_student_from_course_fields():
        if select_student_remove.get() and select_course_remove.get():
            select_remove_student_from_course_button.config(state=tk.NORMAL)
        else:
            select_remove_student_from_course_button.config(state=tk.DISABLED)

    def validate_select_add_instructor_to_course_fields():
        if select_instructor.get() and select_course_instructor.get():
            select_add_instructor_to_course_button.config(state=tk.NORMAL)
        else:
            select_add_instructor_to_course_button.config(state=tk.DISABLED)

    def validate_select_remove_instructor_from_course_fields():
        if select_instructor_remove.get() and select_course_instructor_remove.get():
            select_remove_instructor_from_course_button.config(state=tk.NORMAL)
        else:
            select_remove_instructor_from_course_button.config(state=tk.DISABLED)

    def validate_delete_student_fields():
        if delete_student_id.get():
            delete_student_button.config(state=tk.NORMAL)
        else:
            delete_student_button.config(state=tk.DISABLED)

    def validate_delete_instructor_fields():
        if delete_instructor_id.get():
            delete_instructor_button.config(state=tk.NORMAL)
        else:
            delete_instructor_button.config(state=tk.DISABLED)

    def validate_select_delete_student_fields():
        if select_delete_student.get():
            select_delete_student_button.config(state=tk.NORMAL)
        else:
            select_delete_student_button.config(state=tk.DISABLED)

    def validate_select_delete_instructor_fields():
        if select_delete_instructor.get():
            select_delete_instructor_button.config(state=tk.NORMAL)
        else:
            select_delete_instructor_button.config(state=tk.DISABLED)

    def validate_student_search_fields(*args):
        if search_student_name.get() or search_student_id.get() or search_student_email.get():
            search_student_button.config(state=tk.NORMAL)
        else:
            search_student_button.config(state=tk.DISABLED)

    def validate_instructor_search_fields(*args):
        if search_instructor_name.get() or search_instructor_id.get() or search_instructor_email.get():
            search_instructor_button.config(state=tk.NORMAL)
        else:
            search_instructor_button.config(state=tk.DISABLED)

    def validate_course_search_fields(*args):
        if search_course_name.get() or search_course_id.get():
            search_course_button.config(state=tk.NORMAL)
        else:
            search_course_button.config(state=tk.DISABLED)

    def validate_age_input(P):
        if P.isdigit() or P == "":
            return True
        return False
    
    def clear_message():
        message_label.config(text="")

    def update_dropdowns():
        student_options = get_student_options()
        course_options = get_course_options()
        instructor_options = get_instructor_options()

        student_dropdown['values'] = student_options
        student_dropdown_remove['values'] = student_options
        student_dropdown_delete['values'] = student_options
        course_dropdown['values'] = course_options
        course_dropdown_remove['values'] = course_options
        course_dropdown_instructor['values'] = course_options
        course_dropdown_instructor_remove['values'] = course_options
        course_dropdown_delete['values'] = course_options
        instructor_dropdown['values'] = instructor_options
        instructor_dropdown_remove['values'] = instructor_options
        instructor_dropdown_delete['values'] = instructor_options

    def disable_other_student_search_fields(*args):
        if search_student_name.get():
            search_student_id_entry.config(state=tk.DISABLED)
            search_student_email_entry.config(state=tk.DISABLED)
        elif search_student_id.get():
            search_student_name_entry.config(state=tk.DISABLED)
            search_student_email_entry.config(state=tk.DISABLED)
        elif search_student_email.get():
            search_student_name_entry.config(state=tk.DISABLED)
            search_student_id_entry.config(state=tk.DISABLED)
        else:
            search_student_name_entry.config(state=tk.NORMAL)
            search_student_id_entry.config(state=tk.NORMAL)
            search_student_email_entry.config(state=tk.NORMAL)
        validate_student_search_fields()

    def disable_other_instructor_search_fields(*args):
        if search_instructor_name.get():
            search_instructor_id_entry.config(state=tk.DISABLED)
            search_instructor_email_entry.config(state=tk.DISABLED)
        elif search_instructor_id.get():
            search_instructor_name_entry.config(state=tk.DISABLED)
            search_instructor_email_entry.config(state=tk.DISABLED)
        elif search_instructor_email.get():
            search_instructor_name_entry.config(state=tk.DISABLED)
            search_instructor_id_entry.config(state=tk.DISABLED)
        else:
            search_instructor_name_entry.config(state=tk.NORMAL)
            search_instructor_id_entry.config(state=tk.NORMAL)
            search_instructor_email_entry.config(state=tk.NORMAL)
        validate_instructor_search_fields()

    def disable_other_course_search_fields(*args):
        if search_course_name.get():
            search_course_id_entry.config(state=tk.DISABLED)
        elif search_course_id.get():
            search_course_name_entry.config(state=tk.DISABLED)
        else:
            search_course_name_entry.config(state=tk.NORMAL)
            search_course_id_entry.config(state=tk.NORMAL)
        validate_course_search_fields()

    def register_student_command():
        name = student_name_entry.get().strip()
        age = student_age_entry.get()
        email = student_email_entry.get().strip()
        message, status = register_student(name, int(age), email)

        if status == 200:
            student_name_entry.delete(0, tk.END)
            student_age_entry.delete(0, tk.END)
            student_email_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def add_student_to_course_command():
        student_id = add_student_id_entry.get()
        course_id = add_student_course_id_entry.get()
        message, status = add_student_to_course(int(student_id), int(course_id))

        if status == 200:
            add_student_id_entry.delete(0, tk.END)
            add_student_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_add_student_to_course_command():
        student_id = select_student.get().split(":")[1].strip()
        course_id = select_course.get().split(":")[1].strip()
        message, status = add_student_to_course(int(student_id), int(course_id))

        if status == 200:
            select_student.set("")
            select_course.set("")
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def remove_student_from_course_command():
        student_id = select_student.get().split(":")[1].strip()
        course_id = select_course.get().split(":")[1].strip()
        message, status = remove_student_from_course(int(student_id), int(course_id))

        if status == 200:
            remove_student_id_entry.delete(0, tk.END)
            remove_student_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def remove_student_from_course_command():
        student_id = remove_student_id_entry.get()
        course_id = remove_student_course_id_entry.get()
        message, status = remove_student_from_course(int(student_id), int(course_id))

        if status == 200:
            remove_student_id_entry.delete(0, tk.END)
            remove_student_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_remove_student_from_course_command():
        student_id = select_student_remove.get().split(":")[1].strip()
        course_id = select_course_remove.get().split(":")[1].strip()
        message, status = remove_student_from_course(int(student_id), int(course_id))

        if status == 200:
            select_student_remove.set("")
            select_course_remove.set("")
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def delete_student_command():
        student_id = delete_student_id_entry.get()
        message, status = remove_student(int(student_id))

        if status == 200:
            delete_student_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_delete_student_command():
        student_id = select_delete_student.get().split(":")[1].strip()
        message, status = remove_student(int(student_id))

        if status == 200:
            select_delete_student.set("")
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def search_student():
        name = search_student_name.get().strip()
        student_id = search_student_id.get().strip()
        email = search_student_email.get().strip()

        if name:
            search_type = 'name'
            search_term = name
        elif student_id:
            search_type = 'id'
            search_term = student_id
        else:
            search_type = 'email'
            search_term = email

        students, status = search_students(search_type, search_term)
        if status != 200:
            message_label.config(text=students["message"], fg="red")
            root.after(4000, clear_message)
            return
        search_student_results.delete(0, tk.END)
        
        if status == 200 and students:
            for student in students['students']:
                search_student_results.insert(tk.END, f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                courses, _ = get_student_courses(student.registered_courses)
                course_names = ", ".join(courses['courses']) if courses['courses'] != [] else "No courses registered"
                search_student_results.insert(tk.END, f"Courses: {course_names}")
                search_student_results.insert(tk.END, "")
            search_student_name_entry.delete(0, tk.END)
            search_student_id_entry.delete(0, tk.END)
            search_student_email_entry.delete(0, tk.END)
            message_label.config(text="Search completed", fg="green")
        else:
            message_label.config(text="No students found", fg="red")
        root.after(4000, clear_message)
    
    def search_instructor():
        name = search_instructor_name.get().strip()
        instructor_id = search_instructor_id.get().strip()
        email = search_instructor_email.get().strip()

        if name:
            search_type = 'name'
            search_term = name
        elif instructor_id:
            search_type = 'id'
            search_term = instructor_id
        else:
            search_type = 'email'
            search_term = email

        instructors, status = search_instructors(search_type, search_term)
        if status != 200:
            message_label.config(text=instructors["message"], fg="red")
            root.after(4000, clear_message)
            return
        search_instructor_results.delete(0, tk.END)
        
        if status == 200 and instructors:
            for instructor in instructors['instructors']:
                search_instructor_results.insert(tk.END, f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                courses, _ = get_instructor_courses(instructor.assigned_courses)
                course_names = ", ".join(courses['courses']) if courses['courses'] != [] else "No courses assigned"
                search_instructor_results.insert(tk.END, f"Courses: {course_names}")
                search_instructor_results.insert(tk.END, "")
            search_instructor_name_entry.delete(0, tk.END)
            search_instructor_id_entry.delete(0, tk.END)
            search_instructor_email_entry.delete(0, tk.END)
            message_label.config(text="Search completed", fg="green")
        else:
            message_label.config(text="No instructors found", fg="red")
        
        root.after(4000, clear_message)

    def search_course():
        name = search_course_name.get().strip()
        course_id = search_course_id.get().strip()

        if name:
            search_type = 'name'
            search_term = name
        else:
            search_type = 'id'
            search_term = course_id

        courses, status = search_courses(search_type, search_term)
        search_course_results.delete(0, tk.END)
        
        if status == 200 and courses:
            for course in courses['courses']:
                search_course_results.insert(tk.END, f"Name: {course.name}, ID: {course.course_id}")
                search_course_results.insert(tk.END, f"Description: {course['description']}")
                instructors, _ = get_instructors_by_course(course.course_id)
                instructor_names = ", ".join(instructors['instructors']) if instructors['instructors'] else "No instructors assigned"
                search_course_results.insert(tk.END, f"Instructors: {instructor_names}")
                students, _ = get_students_by_course(course.course_id)
                student_count = len(students['students']) if students['students'] else 0
                search_course_results.insert(tk.END, f"Number of students: {student_count}")
                search_course_results.insert(tk.END, "")
            search_course_name_entry.delete(0, tk.END)
            search_course_id_entry.delete(0, tk.END)
            message_label.config(text="Search completed", fg="green")
        else:
            message_label.config(text="No courses found", fg="red")
        root.after(4000, clear_message)

    
    def register_instructor_command():
        name = instructor_name_entry.get().strip()
        age = instructor_age_entry.get()
        email = instructor_email_entry.get().strip()
        message, status = register_instructor(name, int(age), email)

        if status == 200:
            instructor_name_entry.delete(0, tk.END)
            instructor_age_entry.delete(0, tk.END)
            instructor_email_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def add_instructor_to_course_command():
        instructor_id = add_instructor_id_entry.get()
        course_id = add_instructor_course_id_entry.get()
        message, status = add_instructor_to_course(int(instructor_id), int(course_id))

        if status == 200:
            add_instructor_id_entry.delete(0, tk.END)
            add_instructor_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_add_instructor_to_course_command():
        instructor_id = select_instructor.get().split(":")[1].strip()
        course_id = select_course_instructor.get().split(":")[1].strip()
        message, status = add_instructor_to_course(int(instructor_id), int(course_id))

        if status == 200:
            select_instructor.set("")
            select_course_instructor.set("")
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def remove_instructor_from_course_command():
        instructor_id = remove_instructor_id_entry.get()
        course_id = remove_instructor_course_id_entry.get()
        message, status = remove_instructor_from_course(int(instructor_id), int(course_id))

        if status == 200:
            remove_instructor_id_entry.delete(0, tk.END)
            remove_instructor_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_remove_instructor_from_course_command():
        instructor_id = select_instructor.get().split(":")[1].strip()
        course_id = select_course_instructor.get().split(":")[1].strip()
        message, status = remove_instructor_from_course(int(instructor_id), int(course_id))

        if status == 200:
            select_instructor_remove.set("")
            select_course_instructor_remove.set("")
            message_label.config(text=message["message"], fg="green")
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)


    def delete_instructor_command():
        instructor_id = delete_instructor_id_entry.get()
        message, status = remove_instructor(int(instructor_id))

        if status == 200:
            delete_instructor_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def select_delete_instructor_command():
        instructor_id = select_delete_instructor.get().split(":")[1].strip()
        message, status = remove_instructor(int(instructor_id))

        if status == 200:
            select_delete_instructor.set("")
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def add_course_command():
        name = add_course_name_entry.get().strip()
        description = add_course_description_entry.get("1.0", tk.END).strip()
        message, status = add_course(name, description)

        if status == 200:
            add_course_name_entry.delete(0, tk.END)
            add_course_description_entry.delete("1.0", tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def remove_course_command():
        course_id = remove_course_id_entry.get()
        message, status = remove_course(int(course_id))

        if status == 200:
            remove_course_id_entry.delete(0, tk.END)
            message_label.config(text=message["message"], fg="green")
            update_dropdowns()
        else:
            message_label.config(text=message["message"], fg="red")
        root.after(4000, clear_message)

    def get_student_options():
        students, _ = get_students()
        students = students['students']
        student_options = []

        for student_id, student in students.items():
            student_options.append(f"{student.name}: {student_id}")
        
        return student_options
    
    def get_course_options():
        courses, _ = get_courses()
        courses = courses['courses']
        course_options = []

        for course_id, course in courses.items():
            course_options.append(f"{course.name}: {course_id}")
        
        return course_options

    def display_course_details(event):
        selected_indices = course_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_course = course_listbox.get(selected_index)
            course_id = selected_course.split(",")[1].strip()

            instructors, status = get_instructors_by_course(int(course_id))
            instructor_listbox.delete(0, tk.END)
            
            if status == 200 and 'instructors' in instructors:
                for instructor_id, instructor in instructors['instructors'].items():
                    instructor_listbox.insert(tk.END, f"{instructor.name}, {instructor_id}, {instructor._email}")
                if len(instructors['instructors']) == 0:
                    instructor_listbox.insert(tk.END, "No instructors assigned to this course")

            students, status = get_students_by_course(int(course_id))
            student_listbox.delete(0, tk.END)
            
            if status == 200 and 'students' in students:
                for student_id, student in students['students'].items():
                    student_listbox.insert(tk.END, f"{student.name}, {student_id}, {student._email}")
                if len(students['students']) == 0:
                    student_listbox.insert(tk.END, "No students enrolled in this course")

            message_label.config(text="Course details retrieved successfully", fg="green")
        else:
            message_label.config(text="Please select a course", fg="red")
            
            root.after(4000, clear_message)

    def view_students():
        students, status = get_students()
        view_students_listbox.delete(0, tk.END)
        
        if status == 200 and students:
            for student in students['students'].values():
                courses, _ = get_student_courses(student.registered_courses)
                course_names = ", ".join(courses['courses']) if courses['courses'] != [] else "No courses registered"
                view_students_listbox.insert(tk.END, f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                view_students_listbox.insert(tk.END, f"Courses: {course_names}")
                view_students_listbox.insert(tk.END, "")
            message_label.config(text="Students retrieved successfully", fg="green")
        else:
            message_label.config(text="No students found", fg="red")
        
        root.after(4000, clear_message)

    def view_instructors():
        instructors, status = get_instructors()
        view_instructors_listbox.delete(0, tk.END)
        
        if status == 200 and instructors:
            for instructor in instructors['instructors'].values():
                courses, _ = get_instructor_courses(instructor.assigned_courses)
                course_names = ", ".join(courses['courses']) if courses['courses'] != [] else "No courses assigned"
                view_instructors_listbox.insert(tk.END, f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                view_instructors_listbox.insert(tk.END, f"Courses: {course_names}")
                view_instructors_listbox.insert(tk.END, "")
            message_label.config(text="Instructors retrieved successfully", fg="green")
        else:
            message_label.config(text="No instructors found", fg="red")
        
        root.after(4000, clear_message)


    def populate_courses():
        courses, status = get_courses()
        course_listbox.delete(0, tk.END)
        
        for course_id, course in courses['courses'].items():
            text =  f"{course.name}, {str(course_id)}, {course.description}" if course.description != "" else f"{course.name}, {str(course_id)}"
            course_listbox.insert(tk.END, text)
        message_label.config(text="Courses retrieved successfully", fg="green")
        root.after(4000, clear_message)
        

    def get_instructor_options():
        instructors, _ = get_instructors()
        instructors = instructors['instructors']
        instructor_options = []

        for instructor_id, instructor in instructors.items():
            instructor_options.append(f"{instructor.name}: {instructor_id}")
        
        return instructor_options

    def clear_tab_fields(tab_name):
        tab = notebook.nametowidget(tab_name)
        for widget in tab.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')

    def validate_select_delete_course_fields(*args):
        if select_delete_course.get():
            select_delete_course_button.config(state=tk.NORMAL)
        else:
            select_delete_course_button.config(state=tk.DISABLED)

    def select_delete_course_command():
        selected_course = select_delete_course.get()
        if selected_course:
            course_id = selected_course.split(": ")[1]
            result, status = remove_course(int(course_id))
            if status == 200:
                message_label.config(text=f"Course {course_id} deleted successfully", fg="green")
                course_dropdown_delete['values'] = get_course_options()
                select_delete_course.set('')
                update_dropdowns()
            else:
                message_label.config(text=f"Failed to delete course {course_id}", fg="red")
        else:
            message_label.config(text="Please select a course to delete", fg="red")
        
        root.after(4000, clear_message)

    def get_course_options():
        courses, status = get_courses()
        if status == 200 and courses:
            return [f"{course.name}: {course.course_id}" for course in courses['courses'].values()]
        return []

    root = tk.Tk()
    root.title("School Management System")
    root.geometry("720x650")

    vcmd = (root.register(validate_age_input), '%P')

    notebook = ttk.Notebook(root)

    message_label = tk.Label(root, text="", fg="green")
    message_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

    tab1 = tk.Frame(notebook)
    tab2 = tk.Frame(notebook)
    tab3 = tk.Frame(notebook)

    notebook.add(tab1, text="Students")
    notebook.add(tab2, text="Instructors")
    notebook.add(tab3, text="Courses")

    notebook.grid(row=0, column=0, sticky="nsew", columnspan=3)
    notebook.bind("<<NotebookTabChanged>>", lambda event: clear_tab_fields(notebook.select()))


    """
    STUDENT RELATED
    """


    tk.Label(tab1, text="Register Student", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(20, 5))
    tk.Label(tab1, text="Name: ").grid(row=1, column=0)
    tk.Label(tab1, text="Age: ").grid(row=2, column=0)
    tk.Label(tab1, text="Email: ").grid(row=3, column=0)

    student_name = tk.StringVar()
    student_age = tk.StringVar()
    student_email = tk.StringVar()

    student_name.trace_add("write", lambda *args: validate_register_student_fields())
    student_age.trace_add("write", lambda *args: validate_register_student_fields())
    student_email.trace_add("write", lambda *args: validate_register_student_fields())

    student_name_entry = tk.Entry(tab1, textvariable=student_name)
    student_name_entry.grid(row=1, column=1)

    student_age_entry = tk.Entry(tab1, textvariable=student_age, validate="key", validatecommand=vcmd)
    student_age_entry.grid(row=2, column=1)

    student_email_entry = tk.Entry(tab1, textvariable=student_email)
    student_email_entry.grid(row=3, column=1)

    register_student_button = tk.Button(tab1, text="Register Student", state=tk.DISABLED, command=register_student_command)
    register_student_button.grid(row=4, column=1)

    tk.Label(tab1, text="Delete Student", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, columnspan=2, pady=(20, 5))

    tk.Label(tab1, text="Student ID: ").grid(row=1, column=2)
    delete_student_id = tk.StringVar()
    delete_student_id.trace_add("write", lambda *args: validate_delete_student_fields())

    delete_student_id_entry = tk.Entry(tab1, textvariable=delete_student_id, validate="key", validatecommand=vcmd, width=24)
    delete_student_id_entry.grid(row=1, column=3)

    delete_student_button = tk.Button(tab1, text="Delete", state=tk.DISABLED, command=delete_student_command)
    delete_student_button.grid(row=2, column=3)

    tk.Label(tab1, text="Select Student: ").grid(row=3, column=2)
    select_delete_student = tk.StringVar()
    select_delete_student.trace_add("write", lambda *args: validate_select_delete_student_fields())

    student_dropdown_delete = ttk.Combobox(tab1, textvariable=select_delete_student, values=get_student_options(), state="readonly")
    student_dropdown_delete.grid(row=3, column=3)

    select_delete_student_button = tk.Button(tab1, text="Delete", state=tk.DISABLED, command=select_delete_student_command)
    select_delete_student_button.grid(row=4, column=3)

    tk.Label(tab1, text="Search Student", font=('Helvetica', 10, 'bold')).grid(row=0, column=4, columnspan=2, pady=(20, 5))

    tk.Label(tab1, text="Search by Name:").grid(row=1, column=4)
    search_student_name = tk.StringVar()
    search_student_name.trace_add("write", disable_other_student_search_fields)
    search_student_name_entry = tk.Entry(tab1, textvariable=search_student_name)
    search_student_name_entry.grid(row=1, column=5)

    tk.Label(tab1, text="Search by ID:").grid(row=2, column=4)
    search_student_id = tk.StringVar()
    search_student_id.trace_add("write", disable_other_student_search_fields)
    search_student_id_entry = tk.Entry(tab1, textvariable=search_student_id, validate="key", validatecommand=vcmd)
    search_student_id_entry.grid(row=2, column=5)

    tk.Label(tab1, text="Search by Email:").grid(row=3, column=4)
    search_student_email = tk.StringVar()
    search_student_email.trace_add("write", disable_other_student_search_fields)
    search_student_email_entry = tk.Entry(tab1, textvariable=search_student_email)
    search_student_email_entry.grid(row=3, column=5)

    search_student_button = tk.Button(tab1, text="Search", command=search_student, state=tk.DISABLED)
    search_student_button.grid(row=4, column=5)

    search_student_results = tk.Listbox(tab1, width=40)
    search_student_results.grid(row=5, column=4, columnspan=2, rowspan=4, padx=10, pady=10)

    tk.Label(tab1, text="View Students", font=('Helvetica', 10, 'bold')).grid(row=9, column=4, columnspan=2, pady=(20, 5))
    
    view_students_listbox = tk.Listbox(tab1, width=40)
    view_students_listbox.grid(row=10, column=4, columnspan=2, rowspan=3, padx=10, pady=5)
    
    view_students_button = tk.Button(tab1, text="View All Students", command=view_students)
    view_students_button.grid(row=13, column=4, columnspan=2, pady=5)

    tk.Label(tab1, text="Add Student to Course", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=4, pady=(20, 5))

    tk.Label(tab1, text="Student ID: ").grid(row=6, column=0)
    tk.Label(tab1, text="Course ID: ").grid(row=7, column=0)

    add_student_id = tk.StringVar()
    add_student_course_id = tk.StringVar()

    add_student_id.trace_add("write", lambda *args: validate_add_student_to_course_fields())
    add_student_course_id.trace_add("write", lambda *args: validate_add_student_to_course_fields())

    add_student_id_entry = tk.Entry(tab1, textvariable=add_student_id, validate="key", validatecommand=vcmd)
    add_student_id_entry.grid(row=6, column=1)

    add_student_course_id_entry = tk.Entry(tab1, textvariable=add_student_course_id, validate="key", validatecommand=vcmd)
    add_student_course_id_entry.grid(row=7, column=1)

    add_student_to_course_button = tk.Button(tab1, text="Add Student", state=tk.DISABLED, command=add_student_to_course_command)
    add_student_to_course_button.grid(row=8, column=1)

    tk.Label(tab1, text="Select Student: ").grid(row=6, column=2)
    tk.Label(tab1, text="Select Course: ").grid(row=7, column=2)

    select_student = tk.StringVar()
    select_course = tk.StringVar()

    student_dropdown = ttk.Combobox(tab1, textvariable=select_student, values=get_student_options(), state="readonly")
    student_dropdown.grid(row=6, column=3)

    course_dropdown = ttk.Combobox(tab1, textvariable=select_course, values=get_course_options(), state="readonly")
    course_dropdown.grid(row=7, column=3)

    select_student.trace_add("write", lambda *args: validate_select_add_student_to_course_fields())
    select_course.trace_add("write", lambda *args: validate_select_add_student_to_course_fields())

    select_add_student_to_course_button = tk.Button(tab1, text="Add Student", state=tk.DISABLED, command=select_add_student_to_course_command)
    select_add_student_to_course_button.grid(row=8, column=3)

    tk.Label(tab1, text="Remove Student from Course", font=('Helvetica', 10, 'bold')).grid(row=9, column=0, columnspan=4, pady=(20, 5))

    tk.Label(tab1, text="Student ID: ").grid(row=10, column=0)
    tk.Label(tab1, text="Course ID: ").grid(row=11, column=0)

    remove_student_id = tk.StringVar()
    remove_student_course_id = tk.StringVar()

    remove_student_id.trace_add("write", lambda *args: validate_remove_student_from_course_fields())
    remove_student_course_id.trace_add("write", lambda *args: validate_remove_student_from_course_fields())

    remove_student_id_entry = tk.Entry(tab1, textvariable=remove_student_id, validate="key", validatecommand=vcmd)
    remove_student_id_entry.grid(row=10, column=1)

    remove_student_course_id_entry = tk.Entry(tab1, textvariable=remove_student_course_id, validate="key", validatecommand=vcmd)
    remove_student_course_id_entry.grid(row=11, column=1)

    remove_student_from_course_button = tk.Button(tab1, text="Remove Student", state=tk.DISABLED, command=remove_student_from_course_command)
    remove_student_from_course_button.grid(row=12, column=1)

    tk.Label(tab1, text="Select Student: ").grid(row=10, column=2)
    tk.Label(tab1, text="Select Course: ").grid(row=11, column=2)

    select_student_remove = tk.StringVar()
    select_course_remove = tk.StringVar()

    student_dropdown_remove = ttk.Combobox(tab1, textvariable=select_student_remove, values=get_student_options(), state="readonly")
    student_dropdown_remove.grid(row=10, column=3)

    course_dropdown_remove = ttk.Combobox(tab1, textvariable=select_course_remove, values=get_course_options(), state="readonly")
    course_dropdown_remove.grid(row=11, column=3)

    select_student_remove.trace_add("write", lambda *args: validate_select_remove_student_from_course_fields())
    select_course_remove.trace_add("write", lambda *args: validate_select_remove_student_from_course_fields())

    select_remove_student_from_course_button = tk.Button(tab1, text="Remove Student", state=tk.DISABLED, command=select_remove_student_from_course_command)
    select_remove_student_from_course_button.grid(row=12, column=3)
    

    """
    INSTRUCTOR RELATED
    """


    tk.Label(tab2, text="Register Instructor", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(20, 5))
    tk.Label(tab2, text="Name: ").grid(row=1, column=0)
    tk.Label(tab2, text="Age: ").grid(row=2, column=0)
    tk.Label(tab2, text="Email: ").grid(row=3, column=0)

    instructor_name = tk.StringVar()
    instructor_age = tk.StringVar()
    instructor_email = tk.StringVar()

    instructor_name.trace_add("write", lambda *args: validate_register_instructor_fields())
    instructor_age.trace_add("write", lambda *args: validate_register_instructor_fields())
    instructor_email.trace_add("write", lambda *args: validate_register_instructor_fields())

    instructor_name_entry = tk.Entry(tab2, textvariable=instructor_name)
    instructor_name_entry.grid(row=1, column=1)

    instructor_age_entry = tk.Entry(tab2, textvariable=instructor_age, validate="key", validatecommand=vcmd)
    instructor_age_entry.grid(row=2, column=1)

    instructor_email_entry = tk.Entry(tab2, textvariable=instructor_email)
    instructor_email_entry.grid(row=3, column=1)

    register_instructor_button = tk.Button(tab2, text="Register Instructor", state=tk.DISABLED, command=register_instructor_command)
    register_instructor_button.grid(row=4, column=1)

    tk.Label(tab2, text="Delete Instructor", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, columnspan=2, pady=(20, 5))
    tk.Label(tab2, text="Instructor ID: ").grid(row=1, column=2)

    delete_instructor_id = tk.StringVar()
    delete_instructor_id.trace_add("write", lambda *args: validate_delete_instructor_fields())

    delete_instructor_id_entry = tk.Entry(tab2, textvariable=delete_instructor_id, validate="key", validatecommand=vcmd)
    delete_instructor_id_entry.grid(row=1, column=3)

    delete_instructor_button = tk.Button(tab2, text="Delete", state=tk.DISABLED, command=delete_instructor_command)
    delete_instructor_button.grid(row=2, column=3)

    tk.Label(tab2, text="Select Instructor: ").grid(row=3, column=2)
    select_delete_instructor = tk.StringVar()
    select_delete_instructor.trace_add("write", lambda *args: validate_select_delete_instructor_fields())

    instructor_dropdown_delete = ttk.Combobox(tab2, textvariable=select_delete_instructor, values=get_instructor_options(), state="readonly")
    instructor_dropdown_delete.grid(row=3, column=3)

    select_delete_instructor_button = tk.Button(tab2, text="Delete", state=tk.DISABLED, command=select_delete_instructor_command)
    select_delete_instructor_button.grid(row=4, column=3)

    tk.Label(tab2, text="Search Instructor", font=('Helvetica', 10, 'bold')).grid(row=0, column=4, columnspan=2, pady=(20, 5))

    tk.Label(tab2, text="Search by Name:").grid(row=1, column=4)
    search_instructor_name = tk.StringVar()
    search_instructor_name.trace_add("write", disable_other_instructor_search_fields)
    search_instructor_name_entry = tk.Entry(tab2, textvariable=search_instructor_name)
    search_instructor_name_entry.grid(row=1, column=5)

    tk.Label(tab2, text="Search by ID:").grid(row=2, column=4)
    search_instructor_id = tk.StringVar()
    search_instructor_id.trace_add("write", disable_other_instructor_search_fields)
    search_instructor_id_entry = tk.Entry(tab2, textvariable=search_instructor_id, validate="key", validatecommand=vcmd)
    search_instructor_id_entry.grid(row=2, column=5)

    tk.Label(tab2, text="Search by Email:").grid(row=3, column=4)
    search_instructor_email = tk.StringVar()
    search_instructor_email.trace_add("write", disable_other_instructor_search_fields)
    search_instructor_email_entry = tk.Entry(tab2, textvariable=search_instructor_email)
    search_instructor_email_entry.grid(row=3, column=5)

    search_instructor_button = tk.Button(tab2, text="Search", command=search_instructor, state=tk.DISABLED)
    search_instructor_button.grid(row=4, column=5)

    search_instructor_results = tk.Listbox(tab2, width=40)
    search_instructor_results.grid(row=5, column=4, columnspan=2, rowspan=4, padx=10, pady=10)

    tk.Label(tab2, text="View Instructors", font=('Helvetica', 10, 'bold')).grid(row=9, column=4, columnspan=2, pady=(20, 5))
    
    view_instructors_listbox = tk.Listbox(tab2, width=40)
    view_instructors_listbox.grid(row=10, column=4, columnspan=2, rowspan=3, padx=10, pady=5)
    
    view_instructors_button = tk.Button(tab2, text="View All Instructors", command=view_instructors)
    view_instructors_button.grid(row=13, column=4, columnspan=2, pady=5)

    tk.Label(tab2, text="Add Instructor to Course", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=4, pady=(20, 5))

    tk.Label(tab2, text="Instructor ID: ").grid(row=6, column=0)
    tk.Label(tab2, text="Course ID: ").grid(row=7, column=0)

    add_instructor_id = tk.StringVar()
    add_instructor_course_id = tk.StringVar()

    add_instructor_id.trace_add("write", lambda *args: validate_add_instructor_to_course_fields())
    add_instructor_course_id.trace_add("write", lambda *args: validate_add_instructor_to_course_fields())

    add_instructor_id_entry = tk.Entry(tab2, textvariable=add_instructor_id, validate="key", validatecommand=vcmd)
    add_instructor_id_entry.grid(row=6, column=1)

    add_instructor_course_id_entry = tk.Entry(tab2, textvariable=add_instructor_course_id, validate="key", validatecommand=vcmd)
    add_instructor_course_id_entry.grid(row=7, column=1)

    add_instructor_to_course_button = tk.Button(tab2, text="Add Instructor", state=tk.DISABLED, command=add_instructor_to_course_command)
    add_instructor_to_course_button.grid(row=8, column=1)

    tk.Label(tab2, text="Select Instructor: ").grid(row=6, column=2)
    tk.Label(tab2, text="Select Course: ").grid(row=7, column=2)

    select_instructor = tk.StringVar()
    select_course_instructor = tk.StringVar()

    instructor_dropdown = ttk.Combobox(tab2, textvariable=select_instructor, values=get_instructor_options(), state="readonly")
    instructor_dropdown.grid(row=6, column=3)

    course_dropdown_instructor = ttk.Combobox(tab2, textvariable=select_course_instructor, values=get_course_options(), state="readonly")
    course_dropdown_instructor.grid(row=7, column=3)

    select_instructor.trace_add("write", lambda *args: validate_select_add_instructor_to_course_fields())
    select_course_instructor.trace_add("write", lambda *args: validate_select_add_instructor_to_course_fields())

    select_add_instructor_to_course_button = tk.Button(tab2, text="Add Instructor", state=tk.DISABLED, command=select_add_instructor_to_course_command)
    select_add_instructor_to_course_button.grid(row=8, column=3)

    tk.Label(tab2, text="Remove Instructor from Course", font=('Helvetica', 10, 'bold')).grid(row=9, column=0, columnspan=4, pady=(20, 5))

    tk.Label(tab2, text="Instructor ID: ").grid(row=10, column=0)
    tk.Label(tab2, text="Course ID: ").grid(row=11, column=0)

    remove_instructor_id = tk.StringVar()
    remove_instructor_course_id = tk.StringVar()

    remove_instructor_id.trace_add("write", lambda *args: validate_remove_instructor_from_course_fields())
    remove_instructor_course_id.trace_add("write", lambda *args: validate_remove_instructor_from_course_fields())

    remove_instructor_id_entry = tk.Entry(tab2, textvariable=remove_instructor_id, validate="key", validatecommand=vcmd)
    remove_instructor_id_entry.grid(row=10, column=1)

    remove_instructor_course_id_entry = tk.Entry(tab2, textvariable=remove_instructor_course_id, validate="key", validatecommand=vcmd)
    remove_instructor_course_id_entry.grid(row=11, column=1)

    remove_instructor_from_course_button = tk.Button(tab2, text="Remove Instructor", state=tk.DISABLED, command=remove_instructor_from_course_command)
    remove_instructor_from_course_button.grid(row=12, column=1)

    tk.Label(tab2, text="Select Instructor: ").grid(row=10, column=2)
    tk.Label(tab2, text="Select Course: ").grid(row=11, column=2)

    select_instructor_remove = tk.StringVar()
    select_course_instructor_remove = tk.StringVar()

    instructor_dropdown_remove = ttk.Combobox(tab2, textvariable=select_instructor_remove, values=get_instructor_options(), state="readonly")
    instructor_dropdown_remove.grid(row=10, column=3)

    course_dropdown_instructor_remove = ttk.Combobox(tab2, textvariable=select_course_instructor_remove, values=get_course_options(), state="readonly")
    course_dropdown_instructor_remove.grid(row=11, column=3)

    select_instructor_remove.trace_add("write", lambda *args: validate_select_remove_instructor_from_course_fields())
    select_course_instructor_remove.trace_add("write", lambda *args: validate_select_remove_instructor_from_course_fields())

    select_remove_instructor_from_course_button = tk.Button(tab2, text="Remove Instructor", state=tk.DISABLED, command=select_remove_instructor_from_course_command)
    select_remove_instructor_from_course_button.grid(row=12, column=3)


    """
    COURSE RELATED
    """


    tk.Label(tab3, text="Add Course", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(5, 2))
    tk.Label(tab3, text="Course Name:").grid(row=1, column=0, sticky='e', padx=(5, 2))
    tk.Label(tab3, text="Description:").grid(row=2, column=0, sticky='ne', padx=(5, 2))

    add_course_name = tk.StringVar()
    add_course_description = tk.StringVar()

    add_course_name.trace_add("write", lambda *args: validate_add_course_fields())
    add_course_description.trace_add("write", lambda *args: validate_add_course_fields())

    add_course_name_entry = tk.Entry(tab3, textvariable=add_course_name, width=30)
    add_course_name_entry.grid(row=1, column=1, pady=(2, 2), sticky='w')

    add_course_description_entry = tk.Text(tab3, width=25, height=2)
    add_course_description_entry.grid(row=2, column=1, pady=(0, 2), sticky='w')

    add_course_button = tk.Button(tab3, text="Add Course", state=tk.DISABLED, command=add_course_command)
    add_course_button.grid(row=3, column=1, pady=(2, 5))

    tk.Label(tab3, text="Delete Course", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, columnspan=2, pady=(5, 2))
    tk.Label(tab3, text="Course ID:").grid(row=5, column=0, sticky='e', padx=(5, 2))
    
    remove_course_id = tk.StringVar()
    remove_course_id.trace_add("write", lambda *args: validate_remove_course_fields())

    remove_course_id_entry = tk.Entry(tab3, textvariable=remove_course_id, validate="key", validatecommand=vcmd, width=30)
    remove_course_id_entry.grid(row=5, column=1, pady=(2, 2), sticky='w')

    remove_course_button = tk.Button(tab3, text="Delete Course", state=tk.DISABLED, command=remove_course_command)
    remove_course_button.grid(row=6, column=1, pady=(2, 2))

    tk.Label(tab3, text="Select Course:").grid(row=7, column=0, sticky='e', padx=(5, 2))
    select_delete_course = tk.StringVar()
    select_delete_course.trace_add("write", lambda *args: validate_select_delete_course_fields())

    course_dropdown_delete = ttk.Combobox(tab3, textvariable=select_delete_course, values=get_course_options(), state="readonly", width=28)
    course_dropdown_delete.grid(row=7, column=1, pady=(2, 2), sticky='w')

    select_delete_course_button = tk.Button(tab3, text="Delete Course", state=tk.DISABLED, command=select_delete_course_command)
    select_delete_course_button.grid(row=8, column=1, pady=(2, 5))
    tk.Label(tab3, text="Search Course", font=('Helvetica', 10, 'bold')).grid(row=9, column=0, columnspan=2, pady=(5, 2))
    tk.Label(tab3, text="Course Name:").grid(row=10, column=0, sticky='e')
    tk.Label(tab3, text="Course ID:").grid(row=11, column=0, sticky='e')

    search_course_name = tk.StringVar()
    search_course_id = tk.StringVar()

    search_course_name_entry = tk.Entry(tab3, textvariable=search_course_name, width=30)
    search_course_name_entry.grid(row=10, column=1, sticky='w')

    search_course_id_entry = tk.Entry(tab3, textvariable=search_course_id, validate="key", validatecommand=vcmd, width=30)
    search_course_id_entry.grid(row=11, column=1, sticky='w')

    search_course_name.trace_add("write", disable_other_course_search_fields)
    search_course_id.trace_add("write", disable_other_course_search_fields)

    search_course_name.trace_add("write", validate_course_search_fields)
    search_course_id.trace_add("write", validate_course_search_fields)

    search_course_button = tk.Button(tab3, text="Search", command=search_course, state=tk.DISABLED)
    search_course_button.grid(row=12, column=1, sticky='w', pady=(2, 2))

    search_course_results = tk.Listbox(tab3, width=40, height=6)
    search_course_results.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

    tk.Label(tab3, text="View Courses", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, columnspan=2, pady=(5, 2))

    course_listbox = tk.Listbox(tab3, height=10, width=40)
    course_listbox.grid(row=1, column=2, columnspan=2, rowspan=6, sticky=(tk.W, tk.E), padx=5, pady=(0, 5))

    course_listbox.bind("<<ListboxSelect>>", display_course_details)

    populate_courses_button = tk.Button(tab3, text="View All Courses", command=populate_courses)
    populate_courses_button.grid(row=7, column=2, columnspan=2, pady=(2, 5))

    tk.Label(tab3, text="Course Details", font=('Helvetica', 10, 'bold')).grid(row=8, column=2, columnspan=2, pady=(5, 2))
    tk.Label(tab3, text="Select a course to view course information.").grid(row=9, column=2, columnspan=2, pady=(0, 5))
    
    tk.Label(tab3, text="Instructors:").grid(row=10, column=2, sticky='nw', padx=(5, 2))
    instructor_listbox = tk.Listbox(tab3, height=4, width=35)
    instructor_listbox.grid(row=11, column=2, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=(0, 2))

    tk.Label(tab3, text="Students:").grid(row=12, column=2, sticky='nw', padx=(5, 2))
    student_listbox = tk.Listbox(tab3, height=4, width=35)
    student_listbox.grid(row=13, column=2, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=(0, 2))

    if database:
        root.protocol("WM_DELETE_WINDOW", db_on_closing)
    else:
        root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
    