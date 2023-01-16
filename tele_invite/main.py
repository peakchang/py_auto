from ongo import *



def th():
    getDict = {}
    onth = threading.Thread(target=lambda: goScript(getDict))
    
    onth.daemon = True
    onth.start()
    


# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("텔레그램 자동화")
root.geometry("300x550+500+300")
root.resizable(False, FALSE)

frame2 = LabelFrame(root, text='버튼', padx=60, pady=10)  # padx / pady 내부여백
frame2.pack(padx=10, pady=5)  # padx / pady 외부여백

# 시작 버튼 생성
btn1 = Button(frame2, text='텔레그램 자동화', command=th, padx=50)
btn1.pack()



# ********************************

# 윈도우창 계속 띄우기
root.mainloop()
