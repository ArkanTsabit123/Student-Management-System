# Student Management System

## Project Overview
A professional academic management system for handling student data, courses, grades, and reports. The system implements real-world educational business logic with a structured database.

## Objectives
*   Design and implement database relationships for students, courses, and grades.
*   Develop logic for academic calculations like GPA and transcripts.
*   Build a robust input validation and business rules system.
*   Create a professional reporting system with Excel export.
*   Develop a modular service-oriented architecture.

## Key Features
*   **Student Management**: Full CRUD operations for student records.
*   **Grade System**: Input grades and calculate GPA using a credit-based system.
*   **Academic Tracking**: Manage grades by semester and academic year.
*   **Reporting**: Generate transcripts, course statistics, and institutional reports.
*   **Search and Filter**: Advanced search across multiple student criteria.

## Technology Stack
*   **Backend**: Python 3.8+
*   **Database**: SQLite with relational design
*   **Reporting**: Pandas and OpenPyXL for Excel reports
*   **Validation**: input validation system
*   **Architecture**: Service layer pattern with data models

## Database Schema
The system uses four main tables with foreign key relationships:

1.  **students**: Student information (NIM, name, major, contact, admission year).
2.  **courses**: Course data (code, name, credits, semester, major).
3.  **grades**: Student grade records (semester, year, grade value, letter grade).
4.  **majors**: Available majors and faculty information.

## Project Structure
```
student-management/
├── config/           # Database configuration
├── data/            # SQLite database storage
├── models/          # Data classes (Student, Course, Grade)
├── services/        # Business logic layer
├── reports/         # Excel report generation
├── tests/           # Unit tests
├── utils/           # Helper functions
├── main.py          # Main application logic
├── run.py           # Application entry point
└── requirements.txt # Python dependencies
```

## Installation and Setup
1.  Ensure Python 3.8 or higher is installed.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python run.py
    ```

## Dependencies
*   pandas==2.0.3
*   openpyxl==3.1.2
*   python-dateutil==2.8.2

## Core Components
*   **Database Configuration**: Manages connections, table creation, and initial data.
*   **Data Models**: `Student`, `Course`, and `Grade` classes.
*   **Services**:
    *   `DatabaseService`: Core database operations.
    *   `StudentService`: Student business logic and validation.
    *   `GradeService`: Grade calculations and academic records.
    *   `ValidationService`: Input validation.
*   **Reporting**: `ExcelReportGenerator` for student lists and transcripts.
*   **Utilities**: `GradeCalculator` for GPA and `DataFormatter` for display.

## Usage
Run the application and use the numeric keys (1-9) to navigate the main menu:

1.  **Add New Student** – Create a new student record.
2.  **View All Students** – Display all students.
3.  **Search Students** – Find students by criteria.
4.  **Update Student** – Modify student information.
5.  **Delete Student** – Remove a student and related data.
6.  **View Student Details** – Show complete student info and grades.
7.  **View Academic Summary** – Display overall statistics.
8.  **Manage Grades** – Access the grade management submenu.
9.  **Exit** – Close the application.

### Grade Management Submenu
From the main menu, option 8 provides:
*   Add new grades for students.
*   View and edit existing grades.
*   Calculate and display student GPA.
*   Generate academic transcripts.

### Quick Start Guide
1.  Run `python run.py`.
2.  Select "1. Add New Student" to create a record.
3.  Enter the student information as prompted.
4.  Use "8. Manage Grades" to add grades and view GPA.
5.  Export reports from the student detail view.

## Implementation Timeline
*   **Day 1**: Database and Foundation – Schema, models, and initialization.
*   **Day 2**: Core Student Management – CRUD operations, validation, and search.
*   **Day 3**: Grade Management System – Grade operations and GPA calculation.
*   **Day 4**: Reporting and Analytics – Excel reports and transcripts.
*   **Day 5**: User Interface and Integration – CLI and menu navigation.
*   **Day 6**: Polish and Documentation – Refactoring and final testing.

## Key Features in Detail
*   **Student Management**: Full record handling with validated inputs.
*   **Grade System**: Numeric grade input with automatic letter grade conversion and weighted GPA.
*   **Reporting System**: Export to Excel with professional formatting.
*   **Validation System**: Checks for NIM format, names, email, phone, grades, and years.

## Skills Demonstrated
*   Relational database design with SQL.
*   Input validation and business rule implementation.
*   Professional report generation with Excel.
*   Service-oriented architecture and layered design.
*   Error handling and data consistency.

## Future Enhancements
*   Web interface using Flask or Django.
*   User authentication and role-based access.
*   REST API for mobile integration.
*   Data visualization and charting.
*   Attendance and payment tracking systems.

## License
This project is available for educational and professional use.