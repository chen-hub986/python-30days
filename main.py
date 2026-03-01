from scr.manager import StudentManager
from scr.repository import StudentRepository
from scr.logger import Logger
from scr.decorators import MenuErrorHandler


@MenuErrorHandler
def student_add(students_manager):
    while True:
        name = input("請輸入學生姓名（或輸入 'q' 結束）：")

        if not name.strip():
            print("請輸入學生姓名!")
            continue

        if name.lower() == 'q':
            break
                
        score = input("請輸入學生的成績（用逗號分隔）：")
        scores = [float(s.strip()) for s in score.split(',')]
        students_manager.add_student(name, scores)
    
@MenuErrorHandler
def show_students(students_manager):
    students_manager._validate_empty_student_list()
    print("\n學生資料列表:")
    for student in students_manager.students:
        print(f"{student.name} - 平均成績: {student.average_score():.2f}")


@MenuErrorHandler
def show_avg_score(students_manager):
    students_manager._validate_empty_student_list()
    avg_info = students_manager.get_avg_score()
    print(f"\n各個學生平均成績:{', '.join(f'{name}: {avg:.2f}' for name, avg in avg_info['student_averages'])}")
    print(f"\n所有學生的平均成績為: {avg_info['overall_average']:.2f}")
    print(f"\n最高平均成績的學生是: {avg_info['max_student']}，成績為 {avg_info['max_average_score']:.2f}")
    print(f"\n最低平均成績的學生是: {avg_info['min_student']}，成績為 {avg_info['min_average_score']:.2f}")

@MenuErrorHandler
def show_ranking(students_manager):
    students_manager._validate_empty_student_list()
    ranking = students_manager.get_ranking()
    print("\n成績排名:")

    for rank, student in enumerate(ranking, 1):
        print(f"{rank}. {student.name} - 平均成績: {student.average_score():.2f}")

@MenuErrorHandler
def delete_student(students_manager):
    students_manager._validate_empty_student_list()

    print(f"學生資料列表: {[student.name for student in students_manager.students]}")   
    name = input("請輸入要刪除的學生姓名：")
            
    if not name.strip():
        print("請輸入學生姓名!")
        return
    
    students_manager.find_student(name)

    print(f"正在刪除學生 {name} 的資料...")
                
    students_manager.delete_student(name)

@MenuErrorHandler
def modify_student(students_manager):
    students_manager._validate_empty_student_list()

    print(f"學生資料列表: {[student.name for student in students_manager.students]}")
    name = input("請輸入要修改的學生姓名：")

    if not name.strip():
        print("請輸入學生姓名!")
        return

    students_manager.find_student(name)
    
    score = input("請輸入新的成績（用逗號分隔）：")
    print(f"正在修改學生 {name} 的資料...")

    scores = [float(s.strip()) for s in score.split(',')]
    update_result = students_manager.modify_student(name, scores)
    if update_result:
        return


def main():
    Logger().log_info("學生管理系統啟動")
    students_repository = StudentRepository('students.json')
    students_manager = StudentManager(students_repository)
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
            student_add(students_manager)
        elif choice == '2':
            show_students(students_manager)
        elif choice == '3':
            show_avg_score(students_manager)
        elif choice == '4':
            show_ranking(students_manager)
        elif choice == '5':
            delete_student(students_manager)
        elif choice == '6':
            modify_student(students_manager)
        elif choice == '7':
            print("退出程式。")
            Logger().log_info("學生管理系統關閉")
            break
        else:
            print("無效的選項，請重新輸入！")

if __name__ == "__main__":
    main()
        
