from langchain.prompts import PromptTemplate

db_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Given a user question about a university database, return ONLY the correct SQL query. Do not include explanations or comments.


## RULES:
- Only use the tables and columns listed below.
- Do NOT guess table or column names not in the schema.
- You MAY intelligently map user-friendly terms to actual column names:
    - "course", "subject", "class", or "module" → CourseName
    - "student name" → Student.Name
    - "teacher", "professor", "instructor" → Faculty.Name
    - "department name" → Department.DeptName
    - "HOD", "head of department" → Department.HOD
    - "specialisation" → Specialisation.SpecialisationName
    - "joining year" → Faculty.DateOfJoining or Student.EnrollmentYear
    - "semester" → Enrollment.Semester or Course.SemesterOffered
    - "late books", "overdue" → LibraryTransaction.ReturnDate > LibraryTransaction.DueDate

- Use the correct table joins:
    - Student.StudentID = Enrollment.StudentId
    - Course.CourseID = Enrollment.CourseId
    - Course.FacultyId = Faculty.FacultyId
    - Course.DeptId = Department.DepartmentID
    - Faculty.DeptId = Department.DepartmentID
    - Specialisation.DeptId = Department.DepartmentID
    - (Add Student.SpecialisationID = Specialisation.SpecialisationID if it exists)


- For library data:
    - If BorrowerType = 'student', BorrowerId = Student.StudentID
    - If BorrowerType = 'faculty', BorrowerId = Faculty.FacultyId

- Only use relevant tables and columns.
- Prefer CourseName over CourseCode unless CourseCode is explicitly given.
- Do NOT use columns like 'Grade', 'Remarks', 'CompletionStatus' unless explicitly asked.

Given the following table structure:

Course(CourseId, CourseName, SyllabusUrl, DepartmentId)
Department(DepartmentId, DeptName)
                                                                                  
### Examples:
Q: What is the name of the faculty teaching Data Structures?
A: SELECT Faculty.Name FROM Course JOIN Faculty ON Course.FacultyId = Faculty.FacultyId WHERE Course.CourseName = 'Data Structures';

Q: List students enrolled in Operating Systems.
A: SELECT Student.Name FROM Enrollment JOIN Student ON Enrollment.StudentId = Student.StudentId JOIN Course ON Enrollment.CourseId = Course.CourseId WHERE Course.CourseName = 'Operating Systems';

Q: Which department does faculty member Dr. Mehta belong to?
A: SELECT Department.DeptName FROM Faculty JOIN Department ON Faculty.DeptId = Department.DeptId WHERE Faculty.Name = 'Dr. Mehta';

Q: List student names whose department name is Computer Science.
A: SELECT Student.Name
   FROM Student
   JOIN Department ON Student.DeptId = Department.DeptId
   WHERE Department.DeptName = 'Computer Science';

Q: What is the syllabus link for all Computer Science courses?
A: SELECT Course.CourseName, Course.SyllabusUrl
   FROM Course
   JOIN Department ON Course.DepartmentId = Department.DepartmentId
   WHERE Department.DeptName = 'Computer Science';
                                         
                                         
Now write an SQL query for the question:
{question}
### Database Schema:
Student(StudentID, Name, Email, EnrollmentYear, DeptId)
Faculty(FacultyID, Name, Email, DateOfJoining, DeptId)
Course(CourseID, CourseName, SyllabusUrl, FacultyId, DeptId, SemesterOffered)
Enrollment(EnrollmentID, StudentId, CourseId, Semester, EnrollmentDate)
Department(DepartmentID, DeptName, HOD)
Specialisation(SpecialisationID, SpecialisationName, DeptId)
LibraryTransaction(TransactionId, BookTitle, BorrowerType, BorrowerId, IssueDate, DueDate, ReturnDate)


User question: {question}
SQL query:
""")

