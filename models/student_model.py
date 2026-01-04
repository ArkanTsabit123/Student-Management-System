#models/student_model.py
"""
Student data models for Student Management System
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    id: Optional[int] = None
    nim: str = ""
    name: str = ""
    major: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    admission_year: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'nim': self.nim,
            'name': self.name,
            'major': self.major,
            'email': self.email,
            'phone': self.phone,
            'admission_year': self.admission_year,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __str__(self):
        return f"{self.nim} - {self.name} ({self.major})"


@dataclass
class StudentWithGPA(Student):
    gpa: float = 0.0
    total_credits: int = 0
    completed_courses: int = 0
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'gpa': self.gpa,
            'total_credits': self.total_credits,
            'completed_courses': self.completed_courses
        })
        return base_dict