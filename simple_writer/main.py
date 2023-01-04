from ongo import *



def th():
    getDict = {}
    onth = threading.Thread(goScript())
    onth.daemon = True
    onth.start()



# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("카페 자동화")
root.geometry("300x360+500+300")
root.resizable(False, FALSE)

frame0 = LabelFrame(root, text='버튼을 클릭하세요!', padx=60, pady=5)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백

# 시작 버튼 생성
f_btn2 = Button(frame0, text='심플글쓰기', command=th, padx=50)
f_btn2.pack()


# 윈도우창 계속 띄우기
root.mainloop()
