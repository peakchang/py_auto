from ongo import *



def th():
    getDict = {'ipval': ipVal.get()}
    onth = threading.Thread(target=lambda: goScript(getDict))
    onth.daemon = True
    onth.start()

def th2():
    onth = threading.Thread(ongo_searchItem())
    onth.daemon = True
    onth.start()


def th3():
    onth = threading.Thread(gabi_chk())
    onth.daemon = True
    onth.start()    
    


# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("쇼핑 자동화")
root.geometry("300x250+500+300")
root.resizable(False, FALSE)


frame0 = LabelFrame(root, text='아이피 변경', padx=60, pady=0)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백

frame1 = LabelFrame(root, text='버튼', padx=40, pady=20)  # padx / pady 내부여백
frame1.pack(padx=10, pady=5)  # padx / pady 외부여백



ipVal = IntVar()
ipChk=Checkbutton(frame0,text="아이피 변경",variable=ipVal)
ipChk.select()
ipChk.pack()


# 시작 버튼 생성
btn1 = Button(frame1, text='쇼핑상위 시작', command=th, padx=50)
btn1.pack()

btn2 = Button(frame1, text='쇼핑순위 체크', command=th2, padx=50)
btn2.pack()

btn3 = Button(frame1, text="가격비교 체크", command=th3, padx=50)
btn3.pack()








# 윈도우창 계속 띄우기
root.mainloop()
