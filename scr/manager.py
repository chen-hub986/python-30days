from scr.student import Student
from scr.exceptions import StudentNotFoundException, DuplicateStudentException, InvalidScoreException, emptyStudentListException
from typing import List, Optional
from scr.base_repository import BaseRepository
from scr.logger import Logger


class StudentManager:
    def __init__(self, repository: BaseRepository, data_file='students.json'):
        self.repository = repository
        self.students = self.repository.load_students()

    def save_students(self) -> None:
        self.repository.save_students(self.students)

    def find_student(self, name: str) -> Student:
        for student in self.students:
            if student.name == name:
                return student
        raise StudentNotFoundException(f"學生 {name} 不存在。")

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
        
    def _validate_empty_student_list(self) -> None:
        if not self.students:
            raise emptyStudentListException("沒有學生資料，無法進行操作。")
        
    def add_student(self, name: str, scores: List[float]) -> Student:
         self._validate_name(name)
         self._validate_scores(scores)

         student = Student(name, scores)
         self.students.append(student)

         self.save_students()

         Logger().log_info(f"成功添加學生 {name} 的資料，平均成績為 {student.average_score():.2f}")

         return student

    def delete_student(self, name: str) -> None:
        self._validate_empty_student_list()

        student_to_deleted = self.find_student(name)
        
        self.students.remove(student_to_deleted)
        
        self.save_students()
        Logger().log_info(f"成功刪除學生 {name}")
        return

    def modify_student(self, name: str, scores: List[float]) -> Optional[Student]:
        self._validate_scores(scores)
        self._validate_empty_student_list()

        student = self.find_student(name)
        student.scores = scores

        self.save_students()
        Logger().log_info(f"成功修改學生 {name} 的資料，平均成績為 {student.average_score():.2f}")
        return student  # 返回修改後的學生資料

    def get_avg_score(self) -> dict:
        self._validate_empty_student_list()
        
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
        self._validate_empty_student_list()
        sorted_students = sorted(self.students, key=lambda student: student.average_score(), reverse=True)
        return sorted_students
