from scr.student import Student
from typing import List, Optional
import json
import os

class StudentManager:
    def __init__(self, data_file='students.json'):
        self.data_file = data_file
        self.students = self.load_students()

    def load_students(self) -> List[Student]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return [Student.from_dict(student) for student in data]
            except (json.JSONDecodeError, KeyError):
                print(f"無法讀取學生資料檔案 {self.data_file}，請確保檔案格式正確。")
        return []

    def save_students(self) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([student.to_dict() for student in self.students], file, ensure_ascii=False, indent=4)
    
    def add_student(self, name: str, scores: List[float]) -> Student:
         student = Student(name, scores)
         self.students.append(student)
         self.save_students()
         return student

    def delete_student(self, name: str) -> bool:
        original_students = self.students.copy()
        self.students = [student for student in self.students if student.name != name]
        
        deleted = len(self.students) < len(original_students)
        if deleted:
            self.save_students()
        return deleted  # 返回是否成功刪除學生

    def modify_student(self, name: str, scores: List[float]) -> Optional[Student]:
        for student in self.students:
            if student.name == name:
                student.scores = scores
                self.save_students()
                return student  # 返回修改後的學生資料
        return None  # 沒有找到學生

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
