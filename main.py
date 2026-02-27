from scr.manager import StudentManager
from scr.exceptions import StudentNotFoundException, DuplicateStudentException, InvalidScoreException
from scr.repository import StudentRepository


def main():
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
            while True:
                name = input("請輸入學生姓名（或輸入 'q' 結束）：")

                if not name.strip():
                    print("請輸入學生姓名!")
                    continue

                if name.lower() == 'q':
                    break
                
                try: 
                    score = input("請輸入學生的成績（用逗號分隔）：")
                    scores = [float(s.strip()) for s in score.split(',')]
                    students_manager.add_student(name, scores)
                    print(f"已添加學生 {name} 的資料，平均成績為 {students_manager.students[-1].average_score():.2f}")
                except ValueError:
                    print("成績輸入無效，請確保成績是數字並用逗號分隔。")
                except DuplicateStudentException as e:
                    print(e)
                except InvalidScoreException as e:
                    print(e)
        
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
            
            print(f"正在刪除學生 {name} 的資料...")
            try:
                students_manager.delete_student(name)
                print(f"已刪除學生 {name} 的資料。")
            except StudentNotFoundException as e:
                print(e)

        
        elif choice == '6':
            if not students_manager.students:
                print("沒有學生資料。")
                continue
            print(f"學生資料列表: {[student.name for student in students_manager.students]}")
            name = input("請輸入要修改的學生姓名：")

            if not name.strip():
                print("請輸入學生姓名!")
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
                print("成績輸入無效，請確保成績是數字並用逗號分隔。")
            except InvalidScoreException as e:
                print(e)
            except StudentNotFoundException as e:
                print(e)
        
        elif choice == '7':
            print("退出程式。")
            break
        else:
            print("無效的選項，請重新輸入！")

if __name__ == "__main__":
    main()
        


