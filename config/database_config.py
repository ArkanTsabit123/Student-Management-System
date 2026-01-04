# student-management/config/database_config.py

"""
Database configuration module for Student Management System
"""

import sqlite3
from pathlib import Path

class DatabaseConfig:
    def __init__(self, db_name="student_management.db"):
        self.db_path = Path(__file__).parent.parent / "data" / db_name
        self.db_path.parent.mkdir(exist_ok=True)
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA recursive_triggers = ON;")
        return conn
    
    def initialize_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            major VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(20),
            admission_year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            faculty VARCHAR(50) NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            credits INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            major_code VARCHAR(10) NOT NULL,
            FOREIGN KEY (major_code) REFERENCES majors (code)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            academic_year VARCHAR(10) NOT NULL,
            grade_value DECIMAL(3,2) NOT NULL,
            grade_letter VARCHAR(2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
            UNIQUE(student_id, course_id, semester, academic_year)
        )
        ''')
        
        default_majors = [
            ('TI', 'Informatics Engineering', 'Faculty of Information Technology'),
            ('SI', 'Information Systems', 'Faculty of Information Technology'),
            ('MI', 'Informatics Management', 'Faculty of Information Technology'),
            ('TK', 'Computer Engineering', 'Faculty of Engineering')
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO majors (code, name, faculty) VALUES (?, ?, ?)",
            default_majors
        )
        
        sample_courses = [
            ('TI101', 'Basic Programming', 3, 1, 'TI'),
            ('TI102', 'Discrete Mathematics', 3, 1, 'TI'),
            ('TI103', 'Introduction to Information Technology', 2, 1, 'TI'),
            ('TI201', 'Data Structures', 3, 2, 'TI'),
            ('TI202', 'Algorithms and Programming', 3, 2, 'TI'),
            ('TI203', 'Database Systems', 3, 2, 'TI'),
            ('SI101', 'Information Systems Fundamentals', 3, 1, 'SI'),
            ('SI102', 'Business Introduction', 2, 1, 'SI'),
            ('SI103', 'Economic Mathematics', 3, 1, 'SI'),
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO courses (code, name, credits, semester, major_code) VALUES (?, ?, ?, ?, ?)",
            sample_courses
        )
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")