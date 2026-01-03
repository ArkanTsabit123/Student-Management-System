from typing import List, Dict


class DataFormatter:
    @staticmethod
    def format_student_display(students: List[Dict]) -> List[Dict]:
        formatted = []
        
        for student in students:
            formatted_student = student.copy()
            
            if 'avg_grade' in student:
                formatted_student['gpa_display'] = f"{student['avg_grade']:.2f}"
            else:
                formatted_student['gpa_display'] = "N/A"
            
            course_count = student.get('course_count', 0)
            formatted_student['courses_display'] = f"{course_count} courses"
            
            formatted.append(formatted_student)
        
        return formatted
    
    @staticmethod
    def format_grade_display(grades: List[Dict]) -> List[Dict]:
        formatted = []
        
        for grade in grades:
            formatted_grade = grade.copy()
            formatted_grade['grade_display'] = f"{grade['grade_value']:.2f}"
            formatted_grade['credits_display'] = f"{grade.get('credits', 0)} credits"
            formatted.append(formatted_grade)
        
        return formatted
    
    @staticmethod
    def format_academic_year(year: str) -> str:
        if '/' in year:
            return year
        else:
            return f"{year}/{int(year) + 1}"
    
    @staticmethod
    def get_major_icon(major: str) -> str:
        icons = {
            'Informatics Engineering': '💻',
            'Information Systems': '📊',
            'Informatics Management': '👔',
            'Computer Engineering': '🔧'
        }
        return icons.get(major, '🎓')