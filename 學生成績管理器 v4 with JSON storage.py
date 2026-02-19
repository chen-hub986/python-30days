import json
import os

DATA_FILE = 'students.json'

def load_students(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_students(file_path, students):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(students, file, ensure_ascii=False, indent=4)

def add_student(students):
    while True:
        name = input("請輸入學生姓名（或輸入 'q' 結束）：")
        if not name.strip():
            print("請輸入學生姓名!")
            continue
        if name.lower() == 'q':
            return students
        scores = get_score()
        average = average_score(scores)

        student = {
            "name": name,
            "scores": scores,
        }
        
        students.append(student)
        print(f"已添加學生 {name}，平均成績為 {average:.2f}")
        break
    return students

def show_students(students):
    if not students:
        print("沒有學生資料。")
        return
    print("\n學生資料列表:")
    for student in students:
        average = average_score(student['scores'])
        print(f"{student['name']} - 平均成績: {average:.2f}")

def delete_student(students):
    if not students:
        print("沒有學生資料。")
        return students
    print(f"學生資料列表: {[student['name'] for student in students]}")
    name = input("請輸入要刪除的學生姓名：")
    
    if not name.strip():
        print("請輸入學生姓名!")
        return students
    
    if not any(student['name'] == name for student in students):
        print(f"未找到學生 {name} 的資料。")
        return students
    
    print(f"正在刪除學生 {name} 的資料...")
    students = [student for student in students if student['name'] != name]
    print(f"已刪除學生 {name} 的資料。")
    return students


def modify_student(students):
    if not students:
        print("沒有學生資料。")
        return students
    print(f"學生資料列表: {[student['name'] for student in students]}")
    name = input("請輸入要修改的學生姓名：")
    score = input("請輸入新的成績（用逗號分隔）：")
    print(f"正在修改學生 {name} 的資料...")
    for i, student in enumerate(students):
        if student['name'] == name:
            try:
                scores = [float(s.strip()) for s in score.split(',')]
                average = average_score(scores)
                students[i]['scores'] = scores
                print(f"已修改學生 {name} 的資料，新的平均成績為 {average:.2f}")
                return students
            except ValueError:
                print("請輸入有效的成績！")
                return students
    print(f"未找到學生 {name} 的資料。")
    return students

def get_score():
    while True:
        try:
            scores = input("請輸入學生的成績（用逗號分隔）：")
            return [float(score.strip()) for score in scores.split(',')]
        except ValueError:
            print("請輸入有效的成績！")

def average_score(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)

def print_avg_score(students):
    if not students:
        print("沒有學生資料。")
        return
    averages = [
        average_score(student['scores'])
        for student in students
    ]
    overall_average = sum(averages) / len(averages)

    student_average = list(zip([student['name'] for student in students], averages))
    
    max_student, max_average_score = max(student_average, key=lambda x: x[1])
    min_student, min_average_score = min(student_average, key=lambda x: x[1])
    
    print(f"\n各個學生平均成績:{', '.join(f'{name}: {avg:.2f}' for name, avg in student_average)}")
    print(f"\n所有學生的平均成績為: {overall_average:.2f}")
    print(f"\n最高平均成績的學生是: {max_student}，成績為 {max_average_score:.2f}")
    print(f"\n最低平均成績的學生是: {min_student}，成績為 {min_average_score:.2f}")



def print_ranking(students):
    if not students:
        print("沒有學生資料。")
        return
    sorted_students = sorted(students, key=lambda student: average_score(student['scores']), reverse=True)
    print("\n成績排名:")
    for rank, student in enumerate(sorted_students, 1):
        average = average_score(student['scores'])
        print(f"{rank}. {student['name']} - 平均成績: {average:.2f}")


def main():
    students = load_students(DATA_FILE)
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
            students = add_student(students)
            save_students(DATA_FILE, students)
        elif choice == '2':
            show_students(students)
        elif choice == '3':
            print_avg_score(students)
        elif choice == '4':
            print_ranking(students)
        elif choice == '5':
            students = delete_student(students)
            save_students(DATA_FILE, students)
        elif choice == '6':
            students = modify_student(students)
            save_students(DATA_FILE, students)
        elif choice == '7':
            print("退出程式。")
            break
        else:
            print("無效的選項，請重新輸入！")

if __name__ == "__main__":
    main()
        

