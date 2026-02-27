from scr.student import Student
from scr.exceptions import StudentNotFoundException, DuplicateStudentException, InvalidScoreException
from typing import List, Optional
from scr.base_repository import BaseRepository


class StudentManager:
    def __init__(self, repository: BaseRepository, data_file='students.json'):
        self.repository = repository
        self.students = self.repository.load_students()

    def save_students(self) -> None:
        self.repository.save_students(self.students)

    def _validate_scores(self, scores: List[float]) -> None:
        if not all(isinstance(score, (int, float)) for score in scores):
             raise InvalidScoreException("成績無效，請確保所有成績都是數字。")
        
        if not scores:
            raise InvalidScoreException("成績列表不能為空。")

        if any(score < 0 or score > 100 for score in scores):
             raise InvalidScoreException("成績無效，請確保成績在 0 到 100 之間。")
        
    def _validate_name(self, name: str) -> None:
        if any(student.name == name for student in self.students):
            raise DuplicateStudentException(f"學生 {name} 已存在，無法重複添加。")

    def add_student(self, name: str, scores: List[float]) -> Student:
         self._validate_name(name)
         self._validate_scores(scores)

         student = Student(name, scores)
         self.students.append(student)
         self.save_students()
         return student

    def delete_student(self, name: str) -> None:
        original_students = self.students.copy()
        self.students = [student for student in self.students if student.name != name]
        
        deleted = len(self.students) < len(original_students)
        if deleted:
            self.save_students()
            return
        else:
            raise StudentNotFoundException(f"學生 {name} 不存在，無法刪除。")

    def modify_student(self, name: str, scores: List[float]) -> Optional[Student]:
        self._validate_scores(scores)
        
        for student in self.students:
            if student.name == name:
                student.scores = scores
                self.save_students()
                return student  # 返回修改後的學生資料
        raise StudentNotFoundException(f"學生 {name} 不存在，無法修改。")

    def get_avg_score(self) -> dict:
        if not self.students:
            return {
                "student_averages": [],
                "overall_average": 0,
                "max_student": None,
                "max_average_score": 0,
                "min_student": None,
                "min_average_score": 0
            }
        
        averages = [student.average_score() for student in self.students]
        overall_average = sum(averages) / len(averages)

        student_average = list(zip([student.name for student in self.students], averages))
        
        max_student, max_average_score = max(student_average, key=lambda x: x[1])
        min_student, min_average_score = min(student_average, key=lambda x: x[1])
        
        return {
            "student_averages": student_average,
            "overall_average": overall_average,
            "max_student": max_student,
            "max_average_score": max_average_score,
            "min_student": min_student,
            "min_average_score": min_average_score
        }
        
    def get_ranking(self) -> List[Student]:
        sorted_students = sorted(self.students, key=lambda student: student.average_score(), reverse=True)
        return sorted_students
