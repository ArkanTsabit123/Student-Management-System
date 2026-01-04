# student-management/reports/excel_generator.py
"""
Excel report generator for Student Management System
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class ExcelReportGenerator:
    def __init__(self):
        self.reports_dir = Path(__file__).parent.parent / "reports" / "exports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_students_report(self, students: List[Dict]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"students_report_{timestamp}.xlsx"
        filepath = self.reports_dir / filename
        
        df = pd.DataFrame(students)
        
        column_mapping = {
            'nim': 'Student ID',
            'name': 'Name',
            'major': 'Major',
            'email': 'Email',
            'phone': 'Phone',
            'admission_year': 'Admission Year',
            'course_count': 'Course Count',
            'avg_grade': 'Average Grade'
        }
        
        df = df.rename(columns=column_mapping)
        
        display_columns = ['Student ID', 'Name', 'Major', 'Admission Year',
                          'Course Count', 'Average Grade', 'Email', 'Phone']
        
        available_columns = [col for col in display_columns if col in df.columns]
        df = df[available_columns]
        
        if 'Average Grade' in df.columns:
            df['Average Grade'] = df['Average Grade'].round(2)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data Mahasiswa', index=False)  # Fix: nama sheet sesuai blueprint
            self._add_summary_sheet(writer, students)
            
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                self._auto_adjust_columns(worksheet, df)
        
        return str(filepath)
    
    def generate_academic_transcript(self, student_data: Dict, academic_record: Dict) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{student_data['nim']}_{timestamp}.xlsx"
        filepath = self.reports_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            info_data = {
                'Field': ['Student ID', 'Name', 'Major', 'Admission Year', 'GPA', 'Total Credits'],
                'Value': [
                    student_data['nim'],
                    student_data['name'],
                    student_data['major'],
                    student_data['admission_year'],
                    academic_record['overall_gpa'],
                    academic_record['total_credits']
                ]
            }
            
            info_df = pd.DataFrame(info_data)
            info_df.to_excel(writer, sheet_name='Student Information', index=False)
            
            for semester in academic_record['grades_by_semester']:
                sheet_name = f"Semester {semester['semester']}"
                grades_data = []
                
                for course in semester['courses']:
                    grades_data.append({
                        'Course Code': course['course_code'],
                        'Course Name': course['course_name'],
                        'Credits': course['credits'],
                        'Numeric Grade': course['grade_value'],
                        'Letter Grade': course['grade_letter']
                    })
                
                grades_df = pd.DataFrame(grades_data)
                grades_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                summary_data = {
                    'Semester': [semester['semester']],
                    'Academic Year': [semester['academic_year']],
                    'Semester GPA': [round(semester['gpa'], 2)],
                    'Total Credits': [semester['total_credits']]
                }
                
                summary_df = pd.DataFrame(summary_data)
                start_row = len(grades_df) + 3
                summary_df.to_excel(writer, sheet_name=sheet_name,
                                   startrow=start_row, index=False)
            
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                self._auto_adjust_columns(worksheet, pd.DataFrame())
        
        return str(filepath)
    
    def _add_summary_sheet(self, writer, students: List[Dict]):
        summary_data = []
        
        total_students = len(students)
        students_with_grades = [s for s in students if s.get('avg_grade', 0) > 0]
        
        if students_with_grades:
            avg_gpa = sum(s['avg_grade'] for s in students_with_grades) / len(students_with_grades)
        else:
            avg_gpa = 0
        
        summary_data.append({
            'Metric': 'Total Students',
            'Value': total_students
        })
        
        summary_data.append({
            'Metric': 'Students with Grades',
            'Value': len(students_with_grades)
        })
        
        summary_data.append({
            'Metric': 'Average GPA',
            'Value': round(avg_gpa, 2)
        })
        
        majors = {}
        for student in students:
            major = student['major']
            if major not in majors:
                majors[major] = {'count': 0, 'total_gpa': 0, 'with_grades': 0}
            majors[major]['count'] += 1
            if student.get('avg_grade', 0) > 0:
                majors[major]['total_gpa'] += student['avg_grade']
                majors[major]['with_grades'] += 1
        
        for major, stats in majors.items():
            avg_major_gpa = stats['total_gpa'] / stats['with_grades'] if stats['with_grades'] > 0 else 0
            
            summary_data.append({
                'Metric': f'Students in {major}',
                'Value': stats['count']
            })
            
            summary_data.append({
                'Metric': f'Average GPA for {major}',
                'Value': round(avg_major_gpa, 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    def _auto_adjust_columns(self, worksheet, df):
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width