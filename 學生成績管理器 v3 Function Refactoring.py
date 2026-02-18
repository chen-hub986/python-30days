def get_score():
 while True:
    try:
       scores = input("請輸入學生的成績（用逗號分隔）：")
       return [float(score.strip()) for score in scores.split(',')]
    except ValueError:
       print("請輸入有效的成績！")
    except ZeroDivisionError:
       print("請至少輸入一個成績！")

def average_score(scores):
   if not scores:
       return 0
   return sum(scores) / len(scores)

def print_ranking(students):
    max_average_score = max(score for _, score in students)
    max_student = next(name for name, score in students if score == max_average_score)

    min_average_score = min(score for _, score in students)
    min_student = next(name for name, score in students if score == min_average_score)
    
    print(f"\n平均成績最高的學生是 {max_student}，平均成績為 {max_average_score:.2f}")

    print(f"\n平均成績最低的學生是 {min_student}，平均成績為 {min_average_score:.2f}")
    if min_average_score < 60:
        print(f"\n平均成績不及格的學生是 {min_student}，平均成績為 {min_average_score:.2f}")

    sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
    print("\n成績排名:")
    for rank, (name, score) in enumerate(sorted_students, 1):
        print(f"{rank}. {name} - 平均成績: {score:.2f}")

def main():
    students = []
    while True:
        name = input("請輸入學生姓名（或輸入 'q' 結束）：")
        if not name.strip():           
            print("請輸入學生姓名!")
            continue
        if name.lower() == 'q':
            break
        scores = get_score()
        average = average_score(scores)
        students.append((name, average))
    if not students:
        print("沒有學生資料。")
    else:
        print_ranking(students)
if __name__ == "__main__":    main()
        
