import json
import os

from scr.student import Student
from typing import List
from scr.base_repository import BaseRepository
from scr.logger import Logger


class StudentRepository(BaseRepository):
    def __init__(self, data_file='students.json' ) -> None:
        self.data_file = data_file
        self.students = self.load_students()

    def load_students(self) -> List[Student]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return [Student.from_dict(student) for student in data]
            except (json.JSONDecodeError, KeyError):
                Logger().log_error(f"讀取學生資料檔案 {self.data_file} 時發生錯誤。")
        return []

    def save_students(self , students_list) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(
                [student.to_dict() for student in students_list], file,
                ensure_ascii=False,
                indent=4
            )