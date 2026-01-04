# services/database_service.py
"""
Database service module for Student Management System
"""


import sqlite3
from typing import List, Dict, Any, Optional

from config.database_config import DatabaseConfig
from models.student_model import Student
from models.course_model import Grade


class DatabaseService:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def add_student(self, student: Student) -> int:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO students (nim, name, major, email, phone, admission_year)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            student.nim, student.name, student.major,
            student.email, student.phone, student.admission_year
        ))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return student_id
    
    def get_students(self, filters: Optional[Dict] = None) -> List[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        query = '''
        SELECT s.*,
               COUNT(g.id) as course_count,
               COALESCE(AVG(g.grade_value), 0) as avg_grade
        FROM students s
        LEFT JOIN grades g ON s.id = g.student_id
        WHERE 1=1
        '''
        
        params = []
        
        if filters:
            if 'search_term' in filters:
                query += " AND (s.nim LIKE ? OR s.name LIKE ?)"
                params.extend([f"%{filters['search_term']}%", f"%{filters['search_term']}%"])
            
            if 'major' in filters:
                query += " AND s.major = ?"
                params.append(filters['major'])
            
            if 'year' in filters:
                query += " AND s.admission_year = ?"
                params.append(filters['year'])
        
        query += " GROUP BY s.id ORDER BY s.nim"
        
        cursor.execute(query, params)
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return students
    
    def get_student_by_nim(self, nim: str) -> Optional[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT s.*,
               COUNT(g.id) as course_count,
               COALESCE(AVG(g.grade_value), 0) as avg_grade
        FROM students s
        LEFT JOIN grades g ON s.id = g.student_id
        WHERE s.nim = ?
        GROUP BY s.id
        ''', (nim,))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """Get student by ID"""
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT s.*,
               COUNT(g.id) as course_count,
               COALESCE(AVG(g.grade_value), 0) as avg_grade
        FROM students s
        LEFT JOIN grades g ON s.id = g.student_id
        WHERE s.id = ?
        GROUP BY s.id
        ''', (student_id,))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def update_student(self, student_id: int, student: Student) -> bool:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE students
        SET nim = ?, name = ?, major = ?, email = ?, phone = ?,
            admission_year = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (
            student.nim, student.name, student.major,
            student.email, student.phone, student.admission_year, student_id
        ))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
    
    def delete_student(self, student_id: int) -> bool:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        return rows_affected > 0
    
    def add_grade(self, grade: Grade) -> int:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO grades (student_id, course_id, semester, academic_year, grade_value, grade_letter)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            grade.student_id, grade.course_id, grade.semester,
            grade.academic_year, grade.grade_value, grade.grade_letter
        ))
        
        grade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return grade_id
    
    def get_student_grades(self, student_id: int) -> List[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT g.*, c.code as course_code, c.name as course_name, c.credits
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id = ?
        ORDER BY g.semester, g.academic_year
        ''', (student_id,))
        
        grades = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return grades
    
    def get_student_gpa(self, student_id: int) -> Dict[str, Any]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT
            COUNT(g.id) as total_courses,
            SUM(c.credits) as total_credits,
            SUM(g.grade_value * c.credits) as weighted_sum,
            CASE
                WHEN SUM(c.credits) > 0 THEN SUM(g.grade_value * c.credits) / SUM(c.credits)
                ELSE 0
            END as gpa
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id = ?
        ''', (student_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else {
            'total_courses': 0,
            'total_credits': 0,
            'weighted_sum': 0,
            'gpa': 0
        }
    
    def get_courses(self, major_code: Optional[str] = None,
                   semester: Optional[int] = None) -> List[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM courses WHERE 1=1"
        params = []
        
        if major_code:
            query += " AND major_code = ?"
            params.append(major_code)
        
        if semester:
            query += " AND semester = ?"
            params.append(semester)
        
        query += " ORDER BY semester, code"
        cursor.execute(query, params)
        courses = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return courses
    
    def get_course_by_code(self, course_code: str) -> Optional[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses WHERE code = ?', (course_code,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict]:
        """Get course by ID"""
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_majors(self) -> List[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM majors ORDER BY code')
        majors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return majors
    
    def get_major_statistics(self) -> List[Dict]:
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT
            m.code,
            m.name,
            m.faculty,
            COUNT(s.id) as student_count,
            COALESCE(AVG(g.grade_value), 0) as avg_gpa
        FROM majors m
        LEFT JOIN students s ON m.name = s.major
        LEFT JOIN grades g ON s.id = g.student_id
        GROUP BY m.code, m.name, m.faculty
        ORDER BY m.code
        ''')
        
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats