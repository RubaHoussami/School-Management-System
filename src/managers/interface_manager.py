from src.interfaces.tkinter_gui import boot_tkinter
from src.interfaces.pyqt_gui import boot_pyqt
import tkinter as tk
from tkinter import ttk

def boot_app():
    def start_application():
        interface_choice = app_choice.get()
        data_method = data_choice.get()
        
        if not interface_choice or not data_method:
            error_label.config(text="Please select both interface and data management method.")
            return
        
        data_value = 1 if data_method == "Database" else 0
        
        root.destroy()
        if interface_choice == "Tkinter":
            boot_tkinter(data_value)
        elif interface_choice == "PyQt":
            boot_pyqt(data_value)

    def check_selections(*args):
        if app_choice.get() and data_choice.get():
            start_button.config(state=tk.NORMAL)
            error_label.config(text="")
        else:
            start_button.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Choose Application Settings")
    root.geometry("300x250")

    tk.Label(root, text="Choose the application interface:").pack(pady=(10, 5))
    app_choice = ttk.Combobox(root, values=["Tkinter", "PyQt"], state="readonly")
    app_choice.pack(pady=5)

    tk.Label(root, text="Choose the data management method:").pack(pady=(10, 5))
    data_choice = ttk.Combobox(root, values=["Database", "File"], state="readonly")
    data_choice.pack(pady=5)

    app_choice.bind("<<ComboboxSelected>>", check_selections)
    data_choice.bind("<<ComboboxSelected>>", check_selections)

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=5)

    start_button = tk.Button(root, text="Start Application", command=start_application, state=tk.DISABLED)
    start_button.pack(pady=20)

    root.mainloop()