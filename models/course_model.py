#models/course_model.py
"""
Course and Grade data models for Student Management System
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    credits: int = 0
    semester: int = 0
    major_code: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'credits': self.credits,
            'semester': self.semester,
            'major_code': self.major_code
        }


@dataclass
class Grade:
    id: Optional[int] = None
    student_id: int = 0
    course_id: int = 0
    semester: int = 0
    academic_year: str = ""
    grade_value: float = 0.0
    grade_letter: str = ""
    created_at: Optional[str] = None
    
    student_nim: Optional[str] = None
    student_name: Optional[str] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    course_credits: Optional[int] = None
    
    def to_dict(self):
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'grade_value': self.grade_value,
            'grade_letter': self.grade_letter,
            'created_at': self.created_at
        }
        
        if self.student_nim:
            data['student_nim'] = self.student_nim
        if self.student_name:
            data['student_name'] = self.student_name
        if self.course_code:
            data['course_code'] = self.course_code
        if self.course_name:
            data['course_name'] = self.course_name
        if self.course_credits:
            data['course_credits'] = self.course_credits
        
        return data