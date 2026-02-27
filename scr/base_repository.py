from abc import ABC, abstractmethod
from typing import List
from scr.student import Student

class BaseRepository(ABC):
    @abstractmethod
    def load_students(self) -> list[Student]:
        pass

    @abstractmethod
    def save_students(self, students_list: list[Student]) -> None:
        pass
