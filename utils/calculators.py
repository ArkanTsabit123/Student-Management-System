# utils/calculators.py
"""
Utility calculators for Student Management System
"""


from typing import List, Dict


class GradeCalculator:
    @staticmethod
    def calculate_gpa(grades: List[Dict]) -> float:
        if not grades:
            return 0.0
        
        total_credits = 0
        weighted_sum = 0
        
        for grade in grades:
            credits = grade.get('credits', 0)
            grade_value = grade.get('grade_value', 0)
            total_credits += credits
            weighted_sum += grade_value * credits
        
        return weighted_sum / total_credits if total_credits > 0 else 0.0
    
    @staticmethod
    def get_grade_distribution(grades: List[Dict]) -> Dict[str, int]:
        distribution = {
            'A': 0, 'A-': 0, 'B+': 0, 'B': 0, 'B-': 0,
            'C+': 0, 'C': 0, 'C-': 0, 'D+': 0, 'D': 0
        }
        
        for grade in grades:
            letter_grade = grade.get('grade_letter', '')
            if letter_grade in distribution:
                distribution[letter_grade] += 1
        
        return distribution
    
    @staticmethod
    def calculate_semester_gpa(semester_grades: List[Dict]) -> float:
        return GradeCalculator.calculate_gpa(semester_grades)
    
    @staticmethod
    def get_academic_standing(gpa: float) -> str:
        """Determine academic standing based on GPA"""
        if gpa >= 3.5:
            return "Cum Laude"
        elif gpa >= 3.0:
            return "Excellent"  
        elif gpa >= 2.5:
            return "Good"
        elif gpa >= 2.0:
            return "Satisfactory"
        else:
            return "Needs Improvement"