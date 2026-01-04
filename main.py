# main.py
"""
Student Management System - Main Application
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


class StudentManagementSystem:
    def __init__(self):
        self.db_config = None
        self.student_service = None
        self.grade_service = None
        self.initialize_services()
    
    def initialize_services(self):
        from config.database_config import DatabaseConfig
        from services.student_service import StudentService
        from services.grade_service import GradeService
        
        self.db_config = DatabaseConfig()
        self.student_service = StudentService()
        self.grade_service = GradeService()
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display main menu"""
        self.clear_screen()
        print("=" * 60)
        print("STUDENT MANAGEMENT SYSTEM")
        print("=" * 60)
        print()
        print("MAIN MENU")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. View Student Details")
        print("7. View Academic Summary")
        print("8. Manage Grades")
        print("9. Exit")
        print()
    
    def add_student(self):
        """Handle adding new student"""
        print("\n" + "-" * 40)
        print("ADD NEW STUDENT")
        print("-" * 40)
        
        nim = input("NIM: ")
        name = input("Full Name: ")
        
        print("\nAvailable Majors:")
        print("1. Informatics Engineering")
        print("2. Information Systems")
        print("3. Informatics Management")
        print("4. Computer Engineering")
        
        major_choice = input("Select major (1-4): ")
        majors = [
            "Informatics Engineering",
            "Information Systems",
            "Informatics Management",
            "Computer Engineering"
        ]
        
        if major_choice.isdigit() and 1 <= int(major_choice) <= 4:
            major = majors[int(major_choice) - 1]
        else:
            print("Invalid choice. Defaulting to Informatics Engineering")
            major = majors[0]
        
        admission_year = input("Admission Year: ")
        email = input("Email (optional): ")
        phone = input("Phone (optional): ")
        
        result = self.student_service.create_student(
            nim=nim,
            name=name,
            major=major,
            admission_year=int(admission_year) if admission_year.isdigit() else 2023,
            email=email,
            phone=phone
        )
        
        print(f"\nResult: {result['message'] if result.get('success') else result.get('error', 'Unknown error')}")
    
    def view_all_students(self):
        """Display all students"""
        print("\n" + "-" * 40)
        print("ALL STUDENTS")
        print("-" * 40)
        
        students = self.student_service.search_students()
        
        if not students:
            print("No students found in database.")
            return
        
        print(f"Total Students: {len(students)}\n")
        print(f"{'ID':<5} {'NIM':<15} {'NAME':<25} {'MAJOR':<20}")
        print("-" * 70)
        
        for student in students:
            print(f"{student['id']:<5} {student['nim']:<15} {student['name']:<25} {student['major']:<20}")
    
    def search_students(self):
        """Search for students"""
        print("\n" + "-" * 40)
        print("SEARCH STUDENTS")
        print("-" * 40)
        
        search_term = input("Search term (NIM or Name): ")
        
        students = self.student_service.search_students(search_term=search_term)
        
        if not students:
            print("No students found matching search criteria.")
            return
        
        print(f"\nFound {len(students)} student(s):\n")
        for student in students:
            print(f"NIM: {student['nim']}")
            print(f"Name: {student['name']}")
            print(f"Major: {student['major']}")
            print(f"Year: {student['admission_year']}")
            if student.get('email'):
                print(f"Email: {student['email']}")
            if student.get('phone'):
                print(f"Phone: {student['phone']}")
            print("-" * 40)
    
    def update_student(self):
        """Update student information"""
        print("\n" + "-" * 40)
        print("UPDATE STUDENT")
        print("-" * 40)
        
        student_id = input("Student ID to update: ")
        
        if not student_id.isdigit():
            print("Invalid student ID")
            return
        
        # Get current student data first
        students = self.student_service.search_students()
        current_student = None
        for student in students:
            if student['id'] == int(student_id):
                current_student = student
                break
        
        if not current_student:
            print("Student not found.")
            return
        
        print(f"\nCurrent data for {current_student['name']} ({current_student['nim']}):")
        print(f"Email: {current_student.get('email', 'Not set')}")
        print(f"Phone: {current_student.get('phone', 'Not set')}")
        
        print("\nLeave blank to keep current value")
        email = input(f"New Email [{current_student.get('email', '')}]: ")
        phone = input(f"New Phone [{current_student.get('phone', '')}]: ")
        
        update_data = {}
        if email.strip():
            update_data['email'] = email.strip()
        else:
            update_data['email'] = current_student.get('email', '')
        
        if phone.strip():
            update_data['phone'] = phone.strip()
        else:
            update_data['phone'] = current_student.get('phone', '')
        
        result = self.student_service.update_student(int(student_id), update_data)
        
        print(f"\nResult: {result['message'] if result.get('success') else result.get('error', 'Unknown error')}")
    
    def delete_student(self):
        """Delete a student"""
        print("\n" + "-" * 40)
        print("DELETE STUDENT")
        print("-" * 40)
        
        student_id = input("Student ID to delete: ")
        
        if not student_id.isdigit():
            print("Invalid student ID")
            return
        
        # Show student info first
        detail = self.student_service.get_student_detail(int(student_id))
        if not detail:
            print("Student not found.")
            return
        
        print(f"\nStudent to delete:")
        print(f"NIM: {detail.get('nim')}")
        print(f"Name: {detail.get('name')}")
        print(f"Major: {detail.get('major')}")
        
        confirm = input("\nAre you sure you want to delete this student? (yes/no): ")
        
        if confirm.lower() == 'yes':
            from services.database_service import DatabaseService
            db_service = DatabaseService()
            success = db_service.delete_student(int(student_id))
            
            if success:
                print("\nStudent deleted successfully!")
            else:
                print("\nFailed to delete student.")
        else:
            print("\nDeletion cancelled.")
    
    def view_student_details(self):
        """View detailed student information"""
        print("\n" + "-" * 40)
        print("STUDENT DETAILS")
        print("-" * 40)
        
        student_id = input("Student ID: ")
        
        if not student_id.isdigit():
            print("Invalid student ID")
            return
        
        detail = self.student_service.get_student_detail(int(student_id))
        
        if not detail:
            print("Student not found.")
            return
        
        print(f"\nSTUDENT DETAILS:")
        print(f"NIM: {detail.get('nim')}")
        print(f"Name: {detail.get('name')}")
        print(f"Major: {detail.get('major')}")
        print(f"Admission Year: {detail.get('admission_year')}")
        print(f"GPA: {detail.get('gpa', 'N/A')}")
        print(f"Total Credits: {detail.get('total_credits', 0)}")
        print(f"Completed Courses: {detail.get('completed_courses', 0)}")
        
        if detail.get('email'):
            print(f"Email: {detail['email']}")
        if detail.get('phone'):
            print(f"Phone: {detail['phone']}")
        
        # Show grades if any
        if detail.get('grades'):
            print(f"\nGrades ({len(detail['grades'])} courses):")
            for grade in detail['grades']:
                print(f"  {grade.get('course_code')}: {grade.get('grade_value')} ({grade.get('grade_letter')})")
    
    def view_academic_summary(self):
        """Display academic summary"""
        print("\n" + "-" * 40)
        print("ACADEMIC SUMMARY")
        print("-" * 40)
        
        summary = self.student_service.get_academic_summary()
        
        print(f"Total Students: {summary['total_students']}")
        print(f"Students with Grades: {summary['students_with_grades']}")
        print(f"Overall GPA: {summary['overall_gpa']}")
        
        if summary['majors_statistics']:
            print("\nSTATISTICS BY MAJOR:")
            print("-" * 50)
            for stats in summary['majors_statistics']:
                print(f"{stats['name']}:")
                print(f"  Students: {stats['student_count']}")
                print(f"  Average GPA: {stats['avg_gpa']:.2f}")
    
    def manage_grades(self):
        """Manage student grades"""
        while True:
            print("\n" + "-" * 40)
            print("MANAGE GRADES")
            print("-" * 40)
            
            print("1. Add Grade")
            print("2. View Student Transcript")
            print("3. Back to Main Menu")
            
            choice = input("\nSelect option (1-3): ")
            
            if choice == '1':
                self.add_grade()
            elif choice == '2':
                self.view_transcript()
            elif choice == '3':
                break
            else:
                print("Invalid option")
            
            input("\nPress Enter to continue...")
    
    def add_grade(self):
        """Add grade for student"""
        print("\n" + "-" * 40)
        print("ADD GRADE")
        print("-" * 40)
        
        from services.database_service import DatabaseService
        db_service = DatabaseService()
        
        student_id = input("Student ID: ")
        
        if not student_id.isdigit():
            print("Invalid student ID")
            return
        
        # Get student info
        student = db_service.get_student_by_id(int(student_id))
        if not student:
            print("Student not found.")
            return
        
        print(f"\nStudent: {student['name']} ({student['nim']})")
        print(f"Major: {student['major']}")
        
        # Show available courses for student's major
        major_code = student['major'][:2] if student['major'] else "TI"
        courses = db_service.get_courses(major_code=major_code)
        
        if not courses:
            print(f"No courses available for {student['major']} major.")
            return
        
        print(f"\nAvailable Courses for {student['major']}:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['code']} - {course['name']} ({course['credits']} credits)")
        
        course_choice = input("\nSelect course (number): ")
        
        if not course_choice.isdigit() or not (1 <= int(course_choice) <= len(courses)):
            print("Invalid course selection")
            return
        
        course = courses[int(course_choice) - 1]
        course_id = course['id']
        
        semester = input("Semester: ")
        academic_year = input("Academic Year (e.g., 2023/2024): ")
        grade_value = input("Grade (0.00-4.00): ")
        
        try:
            result = self.grade_service.add_student_grade(
                student_id=int(student_id),
                course_id=course_id,
                semester=int(semester),
                academic_year=academic_year,
                grade_value=float(grade_value)
            )
            
            print(f"\nResult: {result['message'] if result.get('success') else result.get('error', 'Unknown error')}")
        except ValueError:
            print("\nInvalid input. Please enter valid numbers.")
    
    def view_transcript(self):
        """View student academic transcript"""
        print("\n" + "-" * 40)
        print("STUDENT TRANSCRIPT")
        print("-" * 40)
        
        student_id = input("Student ID: ")
        
        if not student_id.isdigit():
            print("Invalid student ID")
            return
        
        student_id = int(student_id)
        
        # Get student details
        detail = self.student_service.get_student_detail(student_id)
        if not detail:
            print("Student not found.")
            return
        
        # Get academic record
        academic_record = self.grade_service.get_student_academic_record(student_id)
        
        print(f"\nTRANSCRIPT FOR: {detail.get('name')} ({detail.get('nim')})")
        print(f"Major: {detail.get('major')}")
        print(f"Overall GPA: {academic_record['overall_gpa']}")
        print(f"Total Credits: {academic_record['total_credits']}")
        print(f"Completed Courses: {academic_record['completed_courses']}")
        
        if academic_record['grades_by_semester']:
            print("\nGrades by Semester:")
            for semester in academic_record['grades_by_semester']:
                print(f"\nSemester {semester['semester']} ({semester['academic_year']}) - GPA: {semester['gpa']:.2f}")
                for course in semester['courses']:
                    print(f"  {course['course_code']}: {course['grade_value']} ({course['grade_letter']}) - {course['credits']} credits")
        else:
            print("\nNo grades recorded yet.")
    
    def run(self):
        """Main entry point for the system"""
        try:
            # Initialize database
            self.db_config.initialize_database()
            print("Database initialized successfully")
            input("Press Enter to continue to main menu...")
            
            while True:
                self.display_menu()
                choice = input("Select option (1-9): ").strip()
                
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.view_all_students()
                elif choice == '3':
                    self.search_students()
                elif choice == '4':
                    self.update_student()
                elif choice == '5':
                    self.delete_student()
                elif choice == '6':
                    self.view_student_details()
                elif choice == '7':
                    self.view_academic_summary()
                elif choice == '8':
                    self.manage_grades()
                elif choice == '9':
                    print("\nExiting system. Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
                
                input("\nPress Enter to continue...")
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            traceback.print_exc()
            input("Press Enter to exit...")


def main():
    """Main entry point"""
    system = StudentManagementSystem()
    system.run()


if __name__ == "__main__":
    main()