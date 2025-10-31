import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# ------------------ OOP Classes ------------------

class Person:
    def __init__(self, id, name, email, phone, gender, address):
        self._id = id
        self._name = name
        self._email = email
        self._phone = phone
        self._gender = gender
        self._address = address

    def get_name(self):
        return self._name

    def display_info(self):
        return f"{self._id}: {self._name}, {self._email}"

class Student(Person):
    def __init__(self, id, name, email, phone, gender, qualification=None, address=None, grades=None):
        super().__init__(id, name, email, phone, gender, address)
        self._qualification = qualification if qualification else "Unknown"
        self._grades = grades if grades else [0, 0, 0]
        self._gpa = self.calculate_gpa()
        self._grade = self.calculate_grade()

    def calculate_gpa(self):
        return round(sum(self._grades) / len(self._grades), 2)

    def calculate_grade(self):
        gpa = self._gpa
        if gpa >= 90:
            return "A"
        elif gpa >= 80:
            return "B"
        elif gpa >= 70:
            return "C"
        elif gpa >= 60:
            return "D"
        else:
            return "F"

    def get_data_as_list(self):
        return [
            self._id, self._name, self._email, self._phone,
            self._gender, self._qualification, self._address,
            self._grades[0], self._grades[1], self._grades[2],
            self._gpa, self._grade
        ]

    def display_info(self):
        return f"Student {self._id}: {self._name}, GPA: {self._gpa}, Grade: {self._grade}"

class Teacher(Person):
    def __init__(self, id, name, email, phone, gender, address, subject):
        super().__init__(id, name, email, phone, gender, address)
        self._subject = subject

    def display_info(self):
        return f"Teacher {self._id}: {self._name}, Subject: {self._subject}"

# ------------------ App Logic ------------------

students = []

def save_to_csv():
    with open("students.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID", "Name", "Email", "Phone", "Gender", "Qualification", "Address",
            "Software", "English", "Programming", "GPA", "Grade"
        ])
        for student in students:
            writer.writerow(student.get_data_as_list())

def load_from_csv():
    if os.path.exists("students.csv"):
        with open("students.csv", mode="r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                (
                    id, name, email, phone, gender, qual, addr,
                    software, english, programming, gpa, grade
                ) = row
                grades = [float(software), float(english), float(programming)]
                student = Student(id, name, email, phone, gender, qual, addr, grades)
                student._gpa = float(gpa)
                student._grade = grade
                students.append(student)

def add_student():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    gender = gender_var.get()
    qual = qual_var.get()
    address = address_var.get()

    try:
        grades = list(map(float, [grade1_var.get(), grade2_var.get(), grade3_var.get()]))
    except:
        messagebox.showerror("Error", "Invalid grades input.")
        return

    if not all([name, email, phone, gender, qual, address]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    id = str(len(students) + 1)
    student = Student(id, name, email, phone, gender, qual, address, grades)
    students.append(student)
    update_table()
    save_to_csv()
    clear_fields()

def delete_student():
    selected = tree.selection()
    if selected:
        index = int(tree.item(selected[0])['values'][0]) - 1
        del students[index]
        for i, student in enumerate(students):
            student._id = str(i + 1)
        update_table()
        save_to_csv()
    else:
        messagebox.showwarning("Warning", "Select a student to delete.")

def edit_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to edit.")
        return

    index = int(tree.item(selected[0])['values'][0]) - 1

    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    gender = gender_var.get()
    qual = qual_var.get()
    address = address_var.get()

    try:
        grades = list(map(float, [grade1_var.get(), grade2_var.get(), grade3_var.get()]))
    except:
        messagebox.showerror("Error", "Invalid grades input.")
        return

    if not all([name, email, phone, gender, qual, address]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    student = Student(str(index + 1), name, email, phone, gender, qual, address, grades)
    students[index] = student
    update_table()
    save_to_csv()
    clear_fields()

def update_table():
    for item in tree.get_children():
        tree.delete(item)
    for student in students:
        tree.insert('', tk.END, values=student.get_data_as_list())

def clear_fields():
    for var in vars:
        var.set("")

def search_student():
    query = search_var.get().strip().lower()
    for item in tree.get_children():
        tree.delete(item)
    for student in students:
        if query in student.get_name().lower():
            tree.insert('', tk.END, values=student.get_data_as_list())

def reset_search():
    search_var.set("")
    update_table()

def on_tree_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        for i, var in enumerate(vars):
            var.set(values[i+1])  # Skip ID

# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title("University Student System")
root.geometry("1200x600")

# Search Frame
search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, padx=10, pady=5)

search_var = tk.StringVar()
tk.Label(search_frame, text="Search Student by Name:").pack(side=tk.LEFT)
tk.Entry(search_frame, textvariable=search_var).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_student).pack(side=tk.LEFT)
tk.Button(search_frame, text="Show All", command=reset_search).pack(side=tk.LEFT)

# Form Frame
form_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

labels = ["Student Name", "Student Email", "Phone", "Gender", "Qualification", "Address", "Software", "English", "Programming"]
vars = [tk.StringVar() for _ in labels]
name_var, email_var, phone_var, gender_var, qual_var, address_var, grade1_var, grade2_var, grade3_var = vars

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=3)
    tk.Entry(form_frame, textvariable=vars[i]).grid(row=i, column=1, padx=10)

# Buttons
btn_frame = tk.LabelFrame(form_frame, text="Controls")
btn_frame.grid(row=10, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Add Student", width=15, command=add_student).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Edit Student", width=15, command=edit_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Student", width=15, command=delete_student).grid(row=1, column=0, padx=5)
tk.Button(btn_frame, text="Clear Fields", width=15, command=clear_fields).grid(row=1, column=1, padx=5)
tk.Button(btn_frame, text="Exit", width=32, command=root.quit).grid(row=2, column=0, columnspan=2, pady=5)

# Table
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = [
    "ID", "Name", "Email", "Phone", "Gender", "Qualification", "Address",
    "Software", "English", "Programming", "GPA", "Grade"
]
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=100)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Load Data
load_from_csv()
update_table()

root.mainloop()