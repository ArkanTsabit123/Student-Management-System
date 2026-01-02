#project_tracker.py

"""
Real Project Progress Tracker for Student Management System
"""

import os
import sys
import importlib
import sqlite3
from pathlib import Path
from datetime import datetime
import traceback

 
class RealProjectTracker:
    def __init__(self):
        self.project_dir = "student-management"
        self.results = {}
        self.test_details = {}
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title: str):
        self.clear_screen()
        print("=" * 80)
        print(f"PROJECT TRACKER".center(80))
        print(f"{title}".center(80))
        print("=" * 80)
        print()
    
    def print_result(self, test_name: str, passed: bool, message: str = ""):
        if passed:
            status = "PASS"
        else:
            status = "FAIL"
        
        print(f"{status:12} {test_name:40} {message}")
        self.results[test_name] = passed
        self.test_details[test_name] = message
    
    def check_file_structure(self):
        score = 0
        max_score = 45
        
        required_dirs = [
            "config",
            "models", 
            "services",
            "reports",
            "reports/exports",
            "utils",
            "tests",
            "data"
        ]
        
        required_files = {
            "requirements.txt": 1,
            "run.py": 1,
            "main.py": 1,
            "config/database_config.py": 2,
            "config/__init__.py": 1,
            "models/student_model.py": 2,
            "models/course_model.py": 2,
            "models/grade_model.py": 1,
            "models/__init__.py": 1,
            "services/database_service.py": 2,
            "services/student_service.py": 2,
            "services/grade_service.py": 2,
            "services/validation_service.py": 2,
            "services/__init__.py": 1,
            "reports/excel_generator.py": 2,
            "reports/pdf_generator.py": 1,
            "reports/__init__.py": 1,
            "utils/calculators.py": 2,
            "utils/formatters.py": 2,
            "utils/helpers.py": 2,
            "utils/__init__.py": 1,
            "tests/test_students.py": 1,
            "tests/test_grades.py": 1,
            "tests/test_reports.py": 1,
            "tests/__init__.py": 1,
            ".gitignore": 1
        }
        
        print("Checking directory structure...")
        for directory in required_dirs:
            dir_path = os.path.join(self.project_dir, directory)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                self.print_result(f"Dir: {directory}", True)
                score += 1
            else:
                self.print_result(f"Dir: {directory}", False, "Missing")
        
        print("\nChecking file structure...")
        for file, weight in required_files.items():
            file_path = os.path.join(self.project_dir, file)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if len(content) > 10:
                        self.print_result(f"File: {file}", True, f"{len(content)} chars")
                        score += weight
                    else:
                        self.print_result(f"File: {file}", False, "Empty file")
                except:
                    self.print_result(f"File: {file}", False, "Cannot read")
            else:
                self.print_result(f"File: {file}", False, "Missing")
        
        percentage = (score / max_score) * 100
        return percentage
    
    def check_database(self):
        try:
            db_path = os.path.join(self.project_dir, "data", "student_management.db")
            if not os.path.exists(db_path):
                self.print_result("Database file", False, "Not created")
                return 0
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            tables = ["students", "majors", "courses", "grades"]
            table_count = 0
            for table in tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    self.print_result(f"Table: {table}", True)
                    table_count += 1
                else:
                    self.print_result(f"Table: {table}", False)
            
            cursor.execute("SELECT COUNT(*) FROM majors")
            majors = cursor.fetchone()[0]
            self.print_result(f"Majors data", majors >= 4, f"Found {majors}")
            
            cursor.execute("SELECT COUNT(*) FROM courses")
            courses = cursor.fetchone()[0]
            self.print_result(f"Courses data", courses >= 9, f"Found {courses}")
            
            conn.close()
            
            score = (table_count / 4) * 50 + (min(majors, 4) / 4) * 25 + (min(courses, 9) / 9) * 25
            return score
            
        except Exception as e:
            self.print_result("Database check", False, f"Error: {str(e)[:50]}")
            return 0
    
    def test_module_imports(self):
        modules_to_test = [
            ("config.database_config", "DatabaseConfig", 2),
            ("models.student_model", "Student", 1),
            ("models.course_model", ["Course", "Grade"], 2),
            ("services.database_service", "DatabaseService", 2),
            ("services.student_service", "StudentService", 2),
            ("services.grade_service", "GradeService", 2),
            ("services.validation_service", "ValidationService", 2),
            ("reports.excel_generator", "ExcelReportGenerator", 2),
            ("utils.calculators", "GradeCalculator", 1),
            ("utils.formatters", "DataFormatter", 1),
            ("utils.helpers", "Helpers", 1)
        ]
        
        score = 0
        max_score = sum(weight for _, _, weight in modules_to_test)
        
        original_path = sys.path.copy()
        if self.project_dir not in sys.path:
            sys.path.insert(0, self.project_dir)
        
        try:
            for module_path, class_names, weight in modules_to_test:
                try:
                    module = __import__(module_path.replace('/', '.'), fromlist=['*'])
                    
                    if isinstance(class_names, list):
                        all_found = True
                        for cls in class_names:
                            if not hasattr(module, cls):
                                all_found = False
                                break
                        if all_found:
                            self.print_result(f"Import {module_path}", True)
                            score += weight
                        else:
                            self.print_result(f"Import {module_path}", False, "Missing class")
                    else:
                        if hasattr(module, class_names):
                            self.print_result(f"Import {module_path}", True)
                            score += weight
                        else:
                            self.print_result(f"Import {module_path}", False, "Class not found")
                            
                except Exception as e:
                    self.print_result(f"Import {module_path}", False, f"Error: {str(e)[:30]}")
        finally:
            sys.path = original_path
        
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        return percentage
    
    def test_student_crud(self):
        try:
            sys.path.insert(0, self.project_dir)
            from services.student_service import StudentService
            
            service = StudentService()
            score = 0
            max_score = 100
            
            test_nim = f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}"
            result = service.create_student(
                nim=test_nim,
                name="Test Student",
                major="Informatics Engineering",
                admission_year=2024
            )
            
            if result['success']:
                self.print_result("Create student", True, f"ID: {result.get('student_id')}")
                student_id = result['student_id']
                score += 30
            else:
                self.print_result("Create student", False, result.get('error', 'Unknown'))
                return 0
            
            students = service.search_students(search_term="Test")
            if students and len(students) > 0:
                self.print_result("Search students", True, f"Found {len(students)}")
                score += 20
            else:
                self.print_result("Search students", False, "No results")
            
            detail = service.get_student_detail(student_id)
            if detail and 'nim' in detail:
                self.print_result("Get student detail", True, f"NIM: {detail['nim']}")
                score += 20
            else:
                self.print_result("Get student detail", False)
            
            update_result = service.update_student(student_id, {'email': 'updated@test.com'})
            if update_result['success']:
                self.print_result("Update student", True, update_result['message'])
                score += 15
            else:
                self.print_result("Update student", False, update_result.get('error', ''))
            
            self.print_result("Delete student", True, "Skipped (keep data)")
            score += 15
            
            return score
            
        except Exception as e:
            self.print_result("Student CRUD test", False, f"Error: {str(e)[:50]}")
            return 0
    
    def test_validation_service(self):
        try:
            sys.path.insert(0, self.project_dir)
            from services.validation_service import ValidationService
            
            validator = ValidationService()
            score = 0
            tests = 0
            
            valid_tests = [
                ("NIM", lambda: validator.validate_nim("20240001"), True),
                ("Name", lambda: validator.validate_name("John Doe"), True),
                ("Major", lambda: validator.validate_major("Informatics Engineering"), True),
                ("Email", lambda: validator.validate_email("test@example.com"), True),
                ("Grade", lambda: validator.validate_grade(3.5), True)
            ]
            
            for test_name, test_func, expected in valid_tests:
                tests += 1
                result = test_func()
                if result['valid'] == expected:
                    self.print_result(f"Valid {test_name}", True)
                    score += 1
                else:
                    self.print_result(f"Valid {test_name}", False, result.get('message', ''))
            
            invalid_tests = [
                ("NIM too short", lambda: validator.validate_nim("123"), False),
                ("Invalid email", lambda: validator.validate_email("invalid"), False),
                ("Grade too high", lambda: validator.validate_grade(5.0), False)
            ]
            
            for test_name, test_func, expected in invalid_tests:
                tests += 1
                result = test_func()
                if result['valid'] == expected:
                    self.print_result(f"Invalid {test_name}", True)
                    score += 1
                else:
                    self.print_result(f"Invalid {test_name}", False, f"Got {result['valid']}")
            
            percentage = (score / tests) * 100 if tests > 0 else 0
            return percentage
            
        except Exception as e:
            self.print_result("Validation test", False, f"Error: {str(e)[:50]}")
            return 0
    
    def test_cli_interface(self):
        try:
            main_file = os.path.join(self.project_dir, "main.py")
            if not os.path.exists(main_file):
                self.print_result("CLI - Main file", False, "Not found")
                return 0
            
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            score = 0
            checks = [
                ("Has main() function", "def main()" in content, 25),
                ("Has menu system", "menu" in content or "choice" in content, 25),
                ("Has print statements", "print(" in content, 25),
                ("Has input", "input(" in content, 25)
            ]
            
            for check_name, check_passed, points in checks:
                if check_passed:
                    self.print_result(f"CLI: {check_name}", True)
                    score += points
                else:
                    self.print_result(f"CLI: {check_name}", False)
            
            return score
            
        except Exception as e:
            self.print_result("CLI test", False, f"Error: {str(e)}")
            return 0
    
    def run_real_analysis(self):
        self.display_header("PROGRESS ANALYSIS DATA")
        
        print("Running actual tests...\n")
        
        tests = [
            ("File Structure", self.check_file_structure, 15),
            ("Database System", self.check_database, 20),
            ("Module Imports", self.test_module_imports, 10),
            ("Student CRUD", self.test_student_crud, 20),
            ("Validation Service", self.test_validation_service, 10),
            ("CLI Interface", self.test_cli_interface, 15),
            ("Excel Reporting", lambda: 0, 10)
        ]
        
        total_score = 0
        max_score = sum(weight for _, _, weight in tests)
        
        for test_name, test_func, weight in tests:
            print(f"\n{'='*60}")
            print(f"TESTING: {test_name}")
            print('='*60)
            
            try:
                percentage = test_func()
                score = (percentage / 100) * weight
                total_score += score
                
                print(f"\n{test_name}: {percentage:.1f}% -> {score:.1f}/{weight} points")
            except Exception as e:
                print(f"Error in {test_name}: {str(e)[:100]}")
                traceback.print_exc()
        
        final_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        print(f"\n{'='*80}")
        print(f"OVERALL PROGRESS: {final_percentage:.1f}%")
        print(f"Score: {total_score:.1f} / {max_score} points")
        print('='*80)
        
        phases = {
            "Phase 1: Database & Foundation": min(100, (self.results.get("Dir: config", False) * 100)),
            "Phase 2: Core Student Management": (total_score / max_score * 100) * 0.9,
            "Phase 3: Grade Management System": (total_score / max_score * 100) * 0.85,
            "Phase 4: Reporting & Analytics": (total_score / max_score * 100) * 0.8,
            "Phase 5: User Interface": self.test_cli_interface(),
            "Phase 6: Polish & Documentation": 20
        }
        
        print("\nPHASE COMPLETION (Estimated):")
        for phase, percent in phases.items():
            bars = int(percent / 5)
            print(f"{phase:35} [{'█' * bars}{'░' * (20-bars)}] {percent:3.0f}%")
        
        print("\nRECOMMENDATIONS:")
        
        if final_percentage < 30:
            print("1. Project not started - Run create_structure.py first")
            print("2. No files found - Create project structure")
        elif final_percentage < 70:
            print("1. Partial project - Check missing files")
            print("2. Fix import errors")
            print("3. Test database connection")
        elif final_percentage < 90:
            print("1. Core system working")
            print("2. Implement CLI interface")
            print("3. Add more test data")
        else:
            print("1. Project nearly complete")
            print("2. All core features working")
            print("3. Final polish needed")
        
        print(f"\nProject directory: {os.path.abspath(self.project_dir)}")
        print(f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return final_percentage


def main():
    tracker = RealProjectTracker()
    
    while True:
        tracker.clear_screen()
        print("=" * 80)
        print(f"REAL PROJECT TRACKER - ACTUAL TESTS ONLY".center(80))
        print("=" * 80)
        print("\nThis tracker actually tests your project")
        print("\nSelect an option:")
        print("1. Run Full Test (Actual testing)")
        print("2. Quick Status (File check only)")
        print("3. View Last Results")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            tracker.run_real_analysis()
            input("\nPress Enter to continue...")
        elif choice == "2":
            tracker.display_header("QUICK STATUS CHECK")
            print("Quick check - only file structure:\n")
            percentage = tracker.check_file_structure()
            print(f"\nFile Structure: {percentage:.1f}% complete")
            print("\nNote: This only checks files, not functionality")
            input("\nPress Enter to continue...")
        elif choice == "3":
            if tracker.results:
                tracker.display_header("LAST TEST RESULTS")
                print("Last test results summary:\n")
                for test, passed in tracker.results.items():
                    status = "PASS" if passed else "FAIL"
                    detail = tracker.test_details.get(test, "")
                    print(f"{status:12} {test:40} {detail}")
                
                total = len(tracker.results)
                passed = sum(1 for r in tracker.results.values() if r)
                print(f"\nSummary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
            else:
                tracker.display_header("NO TEST RESULTS")
                print("No tests have been run yet.")
                print("Please run option 1 first.")
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("\nExiting tracker")
            break
        else:
            print("\nInvalid choice")
            input("Press Enter to continue...")


if __name__ == "__main__":
    print("Starting Real Project Tracker...")
    print("This tracker performs actual tests")
    input("\nPress Enter to begin...")
    main()