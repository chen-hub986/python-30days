count = 0
total_score = 0

while True:
    try:
        score = int(input("請輸入成績 (輸入 -1 結束)"))
    except ValueError:
        print("請輸入有效的整數成績。")
        continue
    if score == -1:
        break

    if count == 0:
        max_score = score
        min_score = score 
    else:
        if score > max_score:
            max_score = score
        if score < min_score:
            min_score = score

    total_score += score
    count += 1
if count == 0:
    print("沒有成績可以計算")
else:
    average = total_score / count
    print(f"總分: {total_score}, 平均: {average:.2f}, 最高分: {max_score}, 最低分: {min_score}")