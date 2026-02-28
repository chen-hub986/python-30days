scores = []

while True:
    try:
        score_input = int(input("請輸入成績 (輸入 -1 結束)"))
    except ValueError:
        print("請輸入有效的整數成績。")
        continue
    if score_input == -1:
        break
    scores.append(score_input)
if len(scores) == 0:
    print("沒有成績可以計算")
else:
     average_score = sum(scores) / len(scores)
     max_score = max(scores)
     min_score = min(scores)
     print("總成績:", sum(scores))
     print("平均成績:", f"{average_score:.2f}")
     print("最高分:", max_score)
     print("最低分:", min_score)
     print("共輸入了", len(scores), "筆成績")
