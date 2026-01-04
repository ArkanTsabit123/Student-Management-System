#models/grade_model.py
"""
Grade data model for Student Management System
"""


from dataclasses import dataclass
from typing import Optional


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
    
    # Joined fields (for display)
    student_nim: Optional[str] = None
    student_name: Optional[str] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    course_credits: Optional[int] = None
    
    def to_dict(self):
        """Convert grade to dictionary"""
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
        
        # Add joined fields if available
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


__all__ = ['Grade']