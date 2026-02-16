students = []

while True:
    try:
        name = input("請輸入學生姓名（或輸入 'q' 結束）：")
        if name.lower() == 'q':
            break
        scores_input = input("請輸入學生的成績（用逗號分隔）：")
        scores = [float(score.strip()) for score in scores_input.split(',')]
        students.append((name, sum(scores) / len(scores)))
    except ValueError:
        print("請輸入有效的成績！")
    except ZeroDivisionError:
        print("請至少輸入一個成績！")
        print("請輸入學生姓名!")


if students:
        min_average_score = min(score for _, score in students)
        min_student = next(name for name, score in students if score == min_average_score)

        max_average_score = max(score for _, score in students)
        max_student = next(name for name, score in students if score == max_average_score)

        print(f"\n平均成績最高的學生是 {max_student}，平均成績為 {max_average_score:.2f}")

        print(f"\n成績排名：")
        sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(sorted_students, 1):
            print(f"{i}. {name} - 平均成績: {score:.2f}")

        if min_average_score < 60:
          print(f"\n平均成績不及格的學生是 {min_student}，平均成績為 {min_average_score:.2f}")
else:    
    print("\n沒有學生資料可計算平均成績。")
