# services/validation_service.py
"""
Validation service module for Student Management System
"""

import re
from typing import Dict, Any
from datetime import datetime


class ValidationService:
    def __init__(self):
        self.current_year = datetime.now().year
    
    def validate_nim(self, nim: str) -> Dict[str, Any]:
        if not nim.strip():
            return {'valid': False, 'message': 'NIM cannot be empty'}
        
        if not re.match(r'^[A-Za-z0-9]{8,20}$', nim):
            return {'valid': False, 'message': 'Invalid NIM format (8-20 alphanumeric characters)'}
        
        return {'valid': True}
    
    def validate_name(self, name: str) -> Dict[str, Any]:
        if not name.strip():
            return {'valid': False, 'message': 'Name cannot be empty'}
        
        if len(name.strip()) < 2:
            return {'valid': False, 'message': 'Name too short'}
        
        if len(name.strip()) > 100:
            return {'valid': False, 'message': 'Name too long (max 100 characters)'}
        
        if not re.match(r'^[a-zA-Z\s\.\']+$', name):
            return {'valid': False, 'message': 'Name can only contain letters, spaces, dots, and apostrophes'}
        
        return {'valid': True}
    
    def validate_major(self, major: str) -> Dict[str, Any]:
        if not major.strip():
            return {'valid': False, 'message': 'Major cannot be empty'}
        
        valid_majors = ['Informatics Engineering', 'Information Systems', 
                       'Informatics Management', 'Computer Engineering']
        
        if major not in valid_majors:
            return {'valid': False, 'message': f'Major must be one of: {", ".join(valid_majors)}'}
        
        return {'valid': True}
    
    def validate_admission_year(self, year: int) -> Dict[str, Any]:
        if year < 2000 or year > self.current_year:
            return {'valid': False, 'message': f'Admission year must be between 2000 and {self.current_year}'}
        
        return {'valid': True}
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        if not email.strip():
            return {'valid': True}
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return {'valid': False, 'message': 'Invalid email format'}
        
        return {'valid': True}
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        if not phone.strip():
            return {'valid': True}
        
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned_phone):
            return {'valid': False, 'message': 'Invalid phone number format (10-15 digits)'}
        
        return {'valid': True}
    
    def validate_grade(self, grade_value: float) -> Dict[str, Any]:
        if grade_value < 0 or grade_value > 4.0:
            return {'valid': False, 'message': 'Grade must be between 0.00 and 4.00'}
        
        return {'valid': True}
    
    def validate_student_data(self, nim: str, name: str, major: str,
                             admission_year: int, email: str = "", phone: str = "") -> Dict[str, Any]:
        validations = [
            self.validate_nim(nim),
            self.validate_name(name),
            self.validate_major(major),
            self.validate_admission_year(admission_year),
            self.validate_email(email),
            self.validate_phone(phone)
        ]
        
        for validation in validations:
            if not validation['valid']:
                return validation
        
        return {'valid': True, 'message': 'Data is valid'}