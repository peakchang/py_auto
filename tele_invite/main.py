from ongo import *



def th():
    getDict = {'ipval': ipVal.get(), 'middleVal': middleVal.get(), 'profileVal': profileVal.get()}
    onth = threading.Thread(target=lambda: goScript(getDict))
    
    onth.daemon = True
    onth.start()
    


# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("블로그 자동화")
root.geometry("300x550+500+300")
root.resizable(False, FALSE)

frame0 = LabelFrame(root, text='아이피 변경', padx=60, pady=5)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백

ipVal = IntVar()
ipChk1 = Radiobutton(frame0, text="아이피 변경", value=1, variable=ipVal)
ipChk2 = Radiobutton(frame0, text="아이피 미변경", value=0, variable=ipVal)
ipChk1.select()
ipChk1.pack()
ipChk2.pack()


frame4 = LabelFrame(root, text='중간체크', padx=60, pady=5)  # padx / pady 내부여백
frame4.pack(padx=10, pady=5)  # padx / pady 외부여백

middleVal = IntVar()
middleChk1 = Radiobutton(frame4, text="체크 안하기", value=1, variable=middleVal)
middleChk2 = Radiobutton(frame4, text="체크 하기", value=0, variable=middleVal)
middleChk1.select()
middleChk1.pack()
middleChk2.pack()


frame5 = LabelFrame(root, text='프로필 체크', padx=60, pady=5)  # padx / pady 내부여백
frame5.pack(padx=10, pady=5)  # padx / pady 외부여백

profileVal = IntVar()
profileChk1 = Radiobutton(frame5, text="체크 안하기", value=1, variable=profileVal)
profileChk2 = Radiobutton(frame5, text="체크 하기", value=0, variable=profileVal)
profileChk1.select()
profileChk1.pack()
profileChk2.pack()


frame1 = LabelFrame(root, text='입력 란', padx=40, pady=20)  # padx / pady 내부여백
frame1.pack(padx=10, pady=5)  # padx / pady 외부여백

frame2 = LabelFrame(root, text='버튼', padx=60, pady=10)  # padx / pady 내부여백
frame2.pack(padx=10, pady=5)  # padx / pady 외부여백

frame3 = LabelFrame(root, text='아이피 변경', padx=60, pady=0)  # padx / pady 내부여백
frame3.pack(padx=10, pady=5)  # padx / pady 외부여백

# 시작 버튼 생성
btn1 = Button(frame2, text='블로그 자동화', command=th, padx=50)
btn1.pack()


# ipVal = IntVar()
# ipChk1 = Radiobutton(frame2, text="아이피 변경", value=1, variable=ipVal)
# ipChk1.select()
# ipChk2 = Radiobutton(frame2, text="아이피 미변경", value=0, variable=ipVal)
# ipChk1.pack()
# ipChk2.pack()


# loginVal = IntVar()
# loginChk1 = Radiobutton(frame3, text="랜덤 로그인", value=1, variable=loginVal)
# loginChk1.select()
# loginChk2 = Radiobutton(frame3, text="로그인 안함", value=0, variable=loginVal)
# loginChk1.pack()
# loginChk2.pack()





# ********************************

# 윈도우창 계속 띄우기
root.mainloop()
