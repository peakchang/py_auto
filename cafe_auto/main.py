from ongo import *



def th():
    getDict = {'ipval': ipVal.get()}
    onth = threading.Thread(target=lambda: goScript(getDict))
    onth.daemon = True
    onth.start()

def th2():
    getDict = {'ipval': ipVal.get()}
    onth = threading.Thread(target=lambda: mobile_chrome(getDict))
    onth.daemon = True
    onth.start()
    
def th3():
    onth = threading.Thread(simple_writer())
    onth.daemon = True
    onth.start()

def th4():
    onth = threading.Thread(login_step())
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
ipChk2 = Radiobutton(frame0, text="아이피 미변경", value=0, variable=ipVal)
ipChk1.select()
ipChk1.pack()
ipChk2.pack()

frame1 = LabelFrame(root, text='카페', padx=40, pady=10)  # padx / pady 내부여백
frame1.pack(padx=10, pady=5)  # padx / pady 외부여백

frame2 = LabelFrame(root, text='Only', padx=60, pady=10)  # padx / pady 내부여백
frame2.pack(padx=10, pady=5)  # padx / pady 외부여백

frame3 = LabelFrame(root, text='아이피 변경', padx=60, pady=0)  # padx / pady 내부여백
frame3.pack(padx=10, pady=5)  # padx / pady 외부여백

# 시작 버튼 생성
btn1 = Button(frame1, text='카페 ALL 자동화', command=th, padx=50)
btn1.pack()

btn2 = Button(frame1, text='순차 로그인', command=th4, padx=50)
btn2.pack()

btn3 = Button(frame1, text="종료하기", command=exitApp, padx=50)
btn3.pack()


# 시작 버튼 생성
f_btn1 = Button(frame2, text='모바일', command=th2, padx=50)
f_btn1.pack()

# 시작 버튼 생성
f_btn2 = Button(frame2, text='심플글쓰기', command=th3, padx=50)
f_btn2.pack()


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
