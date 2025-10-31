import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# قاعدة البيانات المؤقتة
students = []

def save_to_csv():
    with open("students.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Phone", "Gender", "Qualification", "Address", "GPA", "Grade"])
        for student in students:
            writer.writerow(student)

def load_from_csv():
    if os.path.exists("students.csv"):
        with open("students.csv", mode="r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                students.append(row)

def calculate_gpa_and_grade():
    try:
        grades = list(map(float, [grade1_var.get(), grade2_var.get(), grade3_var.get()]))
        gpa = sum(grades) / len(grades)
        if gpa >= 90:
            grade = "A"
        elif gpa >= 80:
            grade = "B"
        elif gpa >= 70:
            grade = "C"
        elif gpa >= 60:
            grade = "D"
        else:
            grade = "F"
        return round(gpa, 2), grade
    except:
        return "", ""

def add_student():
    id = str(len(students) + 1)
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    gender = gender_var.get()
    qual = qual_var.get()
    address = address_var.get()
    gpa, grade = calculate_gpa_and_grade()
    if name and email:
        students.append([id, name, email, phone, gender, qual, address, gpa, grade])
        update_table()
        save_to_csv()
        clear_fields()
    else:
        messagebox.showwarning("Warnning", "Name and email must be entered")

def delete_student():
    selected = tree.selection()
    if selected:
        index = int(tree.item(selected[0])['values'][0]) - 1
        del students[index]
        update_table()
        save_to_csv()
    else:
        messagebox.showwarning("Warnning", "Select a Student to Delete")

def update_table():
    for item in tree.get_children():
        tree.delete(item)
    for student in students:
        tree.insert('', tk.END, values=student)

def clear_fields():
    name_var.set("")
    email_var.set("")
    phone_var.set("")
    gender_var.set("")
    qual_var.set("")
    address_var.set("")
    grade1_var.set("")
    grade2_var.set("")
    grade3_var.set("")

# gui
root = tk.Tk()
root.title("Student Grading System")
root.geometry("1100x600")

# data
form_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

labels = ["Student Name", "Student Gmail", "Student Number", "Gender", "Qualification", "Student Address", "Software ","English", "Programming"]
vars = [tk.StringVar() for _ in range(len(labels))]
name_var, email_var, phone_var, gender_var, qual_var, address_var, grade1_var, grade2_var, grade3_var = vars

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=3)
    entry = tk.Entry(form_frame, textvariable=vars[i])
    entry.grid(row=i, column=1, padx=10)

# control buttons
btn_frame = tk.LabelFrame(form_frame, text="Contol panel")
btn_frame.grid(row=10, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Add Student", width=15, command=add_student).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Delete student", width=15, command=delete_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Empty", width=15, command=clear_fields).grid(row=1, column=0, padx=5)
tk.Button(btn_frame, text="Exit", width=15, command=root.quit).grid(row=1, column=1, padx=5)

# table show
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ["ID", "Name", "Email", "Phone", "Gender", "Qualification", "Address", "GPA", "Grade"]
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=100)
tree.pack(fill=tk.BOTH, expand=True)

load_from_csv()
update_table()

root.mainloop()