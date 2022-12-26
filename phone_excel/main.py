from ongo import *



# def th():
#     getDict = {'getTong': tongVal.current(), 'getLine' : entry.get()}
    
#     onth = threading.Thread(target=lambda: goScript(getDict))
#     onth.daemon = True
#     onth.start()

def th2():
    # getDict = {'getTong': tongVal.current(), 'getLine' : entry.get()}
    
    onth = threading.Thread(target=lambda: make_link())
    onth.daemon = True
    onth.start()
    
def th3():
    getDict = {'getTong': tongVal.current(), 'getLine' : entry.get()}
    
    onth = threading.Thread(target=lambda: gogoScript(getDict))
    onth.daemon = True
    onth.start()

def th4():
    getDict = {'goTong': goTong.get(), 'getLine' : getLine.get()}
    
    onth = threading.Thread(target=lambda: calculScript(getDict))
    onth.daemon = True
    onth.start()
    
def th5():
    onth = threading.Thread(target=lambda: make_link_calcul())
    onth.daemon = True
    onth.start()

def th6():
    getDict = {'getTong': tongChkVal.get(),}
    
    onth = threading.Thread(target=lambda: getGongsi(getDict))
    onth.daemon = True
    onth.start()

# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("이미지 생성하기")
root.geometry("300x450+500+300")
root.resizable(False, FALSE)

frame1 = LabelFrame(root, text='가즈아', padx=40, pady=10)  # padx / pady 내부여백
frame1.pack(padx=10, pady=5)  # padx / pady 외부여백


frame2 = LabelFrame(root, text='계산기', padx=40, pady=10)  # padx / pady 내부여백
frame2.pack(padx=10, pady=5)  # padx / pady 외부여백

frame3 = LabelFrame(root, text='공시지원금', padx=40, pady=10)  # padx / pady 내부여백
frame3.pack(padx=10, pady=5)  # padx / pady 외부여백

# # 시작 버튼 생성
# btn1 = Button(frame1, text='GOGOGO~~!!', command=th, padx=50)
# btn1.pack()

btn2 = Button(frame1, text='링크생성~!!', command=th2, padx=50)
btn2.pack()

btn3 = Button(frame1, text='프로그래밍 요금제!!', command=th3, padx=50)
btn3.pack()

tongVal = ttk.Combobox(frame1, values=['SK','KT','LG'])
tongVal.current(0)
tongVal.pack()

entry = Entry(frame1)
entry.pack()








goTong = Entry(frame2)
goTong.insert(0, 'SK,KT,LG')
goTong.pack()


getLine = Entry(frame2)
getLine.insert(0, '라인 리스트')
getLine.pack()

btn4 = Button(frame2, text='GOGOGO', command=th4, padx=50)
btn4.pack()

btn5 = Button(frame2, text='링크생성', command=th5, padx=50)
btn5.pack()


tongChkVal = StringVar()
tongChk1 = Radiobutton(frame3, text="SKT", value="SKT", variable=tongChkVal)
tongChk1.select()
tongChk2 = Radiobutton(frame3, text="KT", value="KT", variable=tongChkVal)
tongChk3 = Radiobutton(frame3, text="LG U+", value="LG U+", variable=tongChkVal)
tongChk1.pack()
tongChk2.pack()
tongChk3.pack()

gongsi_btn = Button(frame3, text='링크생성', command=th6, padx=50)
gongsi_btn.pack()

# btn2 = Button(frame1, text='쇼핑 순위 체크', command=th2, padx=50)
# btn2.pack()


# # 시작 버튼 생성
# f_btn1 = Button(frame2, text='모바일', command=th2, padx=50)
# f_btn1.pack()

# # 시작 버튼 생성
# f_btn2 = Button(frame2, text='체크체크', command=th3, padx=50)
# f_btn2.pack()


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
