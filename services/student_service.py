# services/student_service.py
"""
Student service module for Student Management System
"""

from typing import List, Dict, Any, Optional

from models.student_model import Student
from services.database_service import DatabaseService
from services.validation_service import ValidationService


class StudentService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.validator = ValidationService()
    
    def create_student(self, nim: str, name: str, major: str,
                      admission_year: int, email: str = "", phone: str = "") -> Dict[str, Any]:
        try:
            validation_result = self.validator.validate_student_data(
                nim, name, major, admission_year, email, phone
            )
            
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['message']
                }
            
            existing_student = self.db_service.get_student_by_nim(nim)
            if existing_student:
                return {
                    'success': False,
                    'error': f'NIM {nim} is already registered'
                }
            
            student = Student(
                nim=nim,
                name=name,
                major=major,
                email=email or None,
                phone=phone or None,
                admission_year=admission_year
            )
            
            student_id = self.db_service.add_student(student)
            
            return {
                'success': True,
                'student_id': student_id,
                'message': 'Student successfully added'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    def get_students(self) -> List[Dict]:
        """Get all students"""
        return self.db_service.get_students()
    
    def search_students(self, search_term: str = "",
                       major: str = "", year: int = 0) -> List[Dict]:
        filters = {}
        
        if search_term.strip():
            filters['search_term'] = search_term.strip()
        if major:
            filters['major'] = major
        if year > 0:
            filters['year'] = year
        
        return self.db_service.get_students(filters)
    
    def update_student(self, student_id: int, kwargs) -> Dict[str, Any]:
        try:
            students = self.db_service.get_students()
            current_student = next((s for s in students if s['id'] == student_id), None)
            
            if not current_student:
                return {
                    'success': False,
                    'error': 'Student not found'
                }
            
            updated_data = current_student.copy()
            updated_data.update(kwargs)
            
            # Handle None values for email and phone
            email = updated_data.get('email', '')
            phone = updated_data.get('phone', '')
            
            validation_result = self.validator.validate_student_data(
                updated_data['nim'],
                updated_data['name'],
                updated_data['major'],
                updated_data['admission_year'],
                email if email is not None else '',
                phone if phone is not None else ''
            )
            
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['message']
                }
            
            if updated_data['nim'] != current_student['nim']:
                existing = self.db_service.get_student_by_nim(updated_data['nim'])
                if existing and existing['id'] != student_id:
                    return {
                        'success': False,
                        'error': f'NIM {updated_data["nim"]} is already used'
                    }
            
            student = Student(
                id=student_id,
                nim=updated_data['nim'],
                name=updated_data['name'],
                major=updated_data['major'],
                email=updated_data.get('email'),
                phone=updated_data.get('phone'),
                admission_year=updated_data['admission_year']
            )
            
            success = self.db_service.update_student(student_id, student)
            
            if success:
                return {
                    'success': True,
                    'message': 'Student data successfully updated'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to update student data'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    def get_student_detail(self, student_id: int) -> Dict[str, Any]:
        students = self.db_service.get_students()
        student = next((s for s in students if s['id'] == student_id), None)
        
        if not student:
            return {}
        
        grades = self.db_service.get_student_grades(student_id)
        gpa_data = self.db_service.get_student_gpa(student_id)
        
        detail = {
            **student,
            'grades': grades,
            'gpa': round(gpa_data['gpa'], 2),
            'total_credits': gpa_data['total_credits'],
            'completed_courses': gpa_data['total_courses']
        }
        
        return detail
    
    def get_academic_summary(self) -> Dict[str, Any]:
        students = self.db_service.get_students()
        majors_stats = self.db_service.get_major_statistics()
        
        total_students = len(students)
        students_with_grades = [s for s in students if s['avg_grade'] > 0]
        
        if students_with_grades:
            overall_gpa = sum(s['avg_grade'] for s in students_with_grades) / len(students_with_grades)
        else:
            overall_gpa = 0
        
        return {
            'total_students': total_students,
            'students_with_grades': len(students_with_grades),
            'overall_gpa': round(overall_gpa, 2),
            'majors_statistics': majors_stats
        }
    
    def delete_student(self, student_id: int) -> Dict[str, Any]:
        """Delete student from database"""
        try:
            # First check if student exists
            detail = self.get_student_detail(student_id)
            if not detail:
                return {
                    'success': False,
                    'error': 'Student not found'
                }
            
            # Delete from database
            success = self.db_service.delete_student(student_id)
            
            if success:
                return {
                    'success': True,
                    'message': f'Student {detail.get("name", "")} deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to delete student'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """Get student by ID"""
        return self.db_service.get_student_by_id(student_id)