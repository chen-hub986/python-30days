from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Student:
    name: str
    scores: List[float] = field(default_factory=list)

    def average_score(self) -> float:
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "scores": self.scores
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        return cls(name=data['name'], scores=data['scores'])


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




def main():
    students_manager = StudentManager()
    while True:
        print("\n選擇操作：")
        print("1. 添加學生資料")
        print("2. 顯示學生資料")
        print("3. 顯示平均成績")
        print("4. 顯示成績排名")
        print("5. 刪除學生資料")
        print("6. 修改學生資料")
        print("7. 退出程式")
        choice = input("請輸入選項（1-7）：")
        
        if choice == '1':
            while True:
                name = input("請輸入學生姓名（或輸入 'q' 結束）：")
                
                if not name.strip():
                    print("請輸入學生姓名!")
                    continue

                if name.lower() == 'q':
                    break
                
                score = input("請輸入學生的成績（用逗號分隔）：")
                try: 
                    scores = [float(s.strip()) for s in score.split(',')]
                    students_manager.add_student(name, scores)
                    print(f"已添加學生 {name} 的資料，平均成績為 {students_manager.students[-1].average_score():.2f}")
                except ValueError:
                    print("請輸入有效的成績！")

        elif choice == '2':
            if not students_manager.students: 
                print("沒有學生資料。")
                continue
            
            print("\n學生資料列表:")
            for student in students_manager.students:
                print(f"{student.name} - 平均成績: {student.average_score():.2f}")

        elif choice == '3':
            if not students_manager.students:
                print("沒有學生資料。")
                continue
            avg_info = students_manager.get_avg_score()
            print(f"\n各個學生平均成績:{', '.join(f'{name}: {avg:.2f}' for name, avg in avg_info['student_averages'])}")
            print(f"\n所有學生的平均成績為: {avg_info['overall_average']:.2f}")
            print(f"\n最高平均成績的學生是: {avg_info['max_student']}，成績為 {avg_info['max_average_score']:.2f}")
            print(f"\n最低平均成績的學生是: {avg_info['min_student']}，成績為 {avg_info['min_average_score']:.2f}")
        
        elif choice == '4':
            if not students_manager.students:
                print("沒有學生資料。")
                continue
            print("\n成績排名:")
            for rank, student in enumerate(students_manager.get_ranking(), 1):
             print(f"{rank}. {student.name} - 平均成績: {student.average_score():.2f}")

        elif choice == '5':
            if not students_manager.students:
                print("沒有學生資料。")
                continue
            print(f"學生資料列表: {[student.name for student in students_manager.students]}")
            name = input("請輸入要刪除的學生姓名：")
            
            if not name.strip():
                print("請輸入學生姓名!")
                continue
            
            if not any(student.name == name for student in students_manager.students):
                print(f"未找到學生 {name} 的資料。")
                continue
            
            print(f"正在刪除學生 {name} 的資料...")
            if students_manager.delete_student(name):
                print(f"已刪除學生 {name} 的資料。")
        
        elif choice == '6':
            if not students_manager.students:
                print("沒有學生資料。")
                continue
            print(f"學生資料列表: {[student.name for student in students_manager.students]}")
            name = input("請輸入要修改的學生姓名：")

            if not name.strip():
                print("請輸入學生姓名!")
                continue

            if not any(student.name == name for student in students_manager.students):
                print(f"未找到學生 {name} 的資料。")
                continue

            score = input("請輸入新的成績（用逗號分隔）：")
            print(f"正在修改學生 {name} 的資料...")
            try:
                scores = [float(s.strip()) for s in score.split(',')]
                update_result = students_manager.modify_student(name, scores)
                if update_result:
                    print(f"已修改學生 {name} 的資料，新的平均成績為 {update_result.average_score():.2f}")
                else:
                    print(f"未找到學生 {name} 的資料。")
            except ValueError:
                print("請輸入有效的成績！")
        
        elif choice == '7':
            print("退出程式。")
            break
        else:
            print("無效的選項，請重新輸入！")

if __name__ == "__main__":
    main()
        

