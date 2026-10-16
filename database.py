import sqlite3

def init_db():
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, class_id INTEGER, roll_number INTEGER, name TEXT NOT NULL, phone TEXT, email TEXT, FOREIGN KEY (class_id) REFERENCES classes(id))")
    conn.commit()
    conn.close()

def add_class(name):
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (name) VALUES (?)", (name,))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def get_classes():
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM classes")
    turmas = cursor.fetchall()
    conn.close()
    return turmas

def delete_class(class_id):
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE class_id = ?", (class_id,))
    cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
    conn.commit()
    conn.close()

def add_student(class_id, roll_number, name, phone="", email=""):
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (class_id, roll_number, name, phone, email) VALUES (?, ?, ?, ?, ?)", (class_id, roll_number, name, phone, email))
    conn.commit()
    conn.close()

def get_students_by_class(class_id):
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, roll_number, name, phone, email FROM students WHERE class_id = ? ORDER BY roll_number ASC", (class_id,))
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def delete_student(student_id):
    conn = sqlite3.connect("app_local.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()