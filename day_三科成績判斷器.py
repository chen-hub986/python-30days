
A=int(input("請輸入第一科成績: "))
B=int(input("請輸入第二科成績: "))
C=int(input("請輸入第三科成績: "))
Average=(A+B+C)/3

print(f"平均成績為{Average:.2f}")

if Average>=90:
  print("成績優秀")
elif Average>=60 and Average<90:
  print("成績及格")
else:  print("成績不及格")

if A < 40 or B < 40 or C < 40:
  print("有單科過低，需特別注意")

