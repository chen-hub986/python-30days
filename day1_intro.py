
name=input("輸入姓名")
while True:
  try:
    age=int(input("輸入年齡"))
  except ValueError:
    print("請輸入數字")
  else:
    break
major=input("輸入你的就讀科系")

print(f"我叫{name},我今年{age}歲,我就讀的科系是{major}")

