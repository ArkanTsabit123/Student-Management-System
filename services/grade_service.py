from typing import List, Dict, Any, Optional

from ..models.course_model import Grade
from .database_service import DatabaseService
from .validation_service import ValidationService


class GradeService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.validator = ValidationService()
    
    def calculate_grade_letter(self, grade_value: float) -> str:
        if grade_value >= 3.7:
            return 'A'
        elif grade_value >= 3.3:
            return 'A-'
        elif grade_value >= 3.0:
            return 'B+'
        elif grade_value >= 2.7:
            return 'B'
        elif grade_value >= 2.3:
            return 'B-'
        elif grade_value >= 2.0:
            return 'C+'
        elif grade_value >= 1.7:
            return 'C'
        elif grade_value >= 1.3:
            return 'C-'
        elif grade_value >= 1.0:
            return 'D+'
        else:
            return 'D'
    
    def add_student_grade(self, student_id: int, course_id: int,
                         semester: int, academic_year: str, grade_value: float) -> Dict[str, Any]:
        try:
            grade_validation = self.validator.validate_grade(grade_value)
            if not grade_validation['valid']:
                return {
                    'success': False,
                    'error': grade_validation['message']
                }
            
            grade_letter = self.calculate_grade_letter(grade_value)
            
            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                semester=semester,
                academic_year=academic_year,
                grade_value=grade_value,
                grade_letter=grade_letter
            )
            
            grade_id = self.db_service.add_grade(grade)
            
            return {
                'success': True,
                'grade_id': grade_id,
                'message': f'Grade successfully added: {grade_letter}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    def get_student_academic_record(self, student_id: int) -> Dict[str, Any]:
        grades = self.db_service.get_student_grades(student_id)
        gpa_data = self.db_service.get_student_gpa(student_id)
        
        semesters = {}
        for grade in grades:
            semester_key = f"{grade['semester']}_{grade['academic_year']}"
            if semester_key not in semesters:
                semesters[semester_key] = {
                    'semester': grade['semester'],
                    'academic_year': grade['academic_year'],
                    'courses': [],
                    'total_credits': 0,
                    'weighted_sum': 0
                }
            
            semesters[semester_key]['courses'].append(grade)
            semesters[semester_key]['total_credits'] += grade['credits']
            semesters[semester_key]['weighted_sum'] += grade['grade_value'] * grade['credits']
        
        for semester in semesters.values():
            if semester['total_credits'] > 0:
                semester['gpa'] = semester['weighted_sum'] / semester['total_credits']
            else:
                semester['gpa'] = 0
        
        return {
            'grades_by_semester': list(semesters.values()),
            'overall_gpa': round(gpa_data['gpa'], 2),
            'total_credits': gpa_data['total_credits'],
            'completed_courses': gpa_data['total_courses']
        }
    
    def get_course_statistics(self, course_id: int) -> Dict[str, Any]:
        return {
            'course_id': course_id,
            'total_students': 0,
            'average_grade': 0,
            'grade_distribution': {}
        }