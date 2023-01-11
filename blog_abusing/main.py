from ongo import *



def th():
    getDict = {'ipval': ipVal.get()}
    onth = threading.Thread(target=lambda: goScript(getDict))
    onth.daemon = True
    onth.start()

# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("카페 자동화")
root.geometry("300x360+500+300")
root.resizable(False, FALSE)

frame0 = LabelFrame(root, text='아이피 변경', padx=60, pady=5)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백

ipVal = IntVar()
ipChk1 = Radiobutton(frame0, text="아이피 변경", value=1, variable=ipVal)
ipChk1.select()
ipChk2 = Radiobutton(frame0, text="아이피 미변경", value=0, variable=ipVal)
ipChk1.pack()
ipChk2.pack()

# 시작 버튼 생성
btn1 = Button(frame0, text='카페 ALL 자동화', command=th, padx=50)
btn1.pack()




# ********************************

# 윈도우창 계속 띄우기
root.mainloop()
