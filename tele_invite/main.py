from ongo import *



def th():
    getDict = {'add_addr_val': addAddr.get(), 'join_group_val': joinGroup.get()}
    onth = threading.Thread(target=lambda: goScript(getDict))
    
    onth.daemon = True
    onth.start()
    
def th2():
    getDict = {}
    onth = threading.Thread(target=lambda: authListChk())
    
    onth.daemon = True
    onth.start()

def th3():
    getDict = {}
    onth = threading.Thread(target=lambda: delAuthList())
    
    onth.daemon = True
    onth.start()

def th4():
    getDict = {}
    onth = threading.Thread(target=lambda: inviteManager())
    
    onth.daemon = True
    onth.start()
    


# 윈도우 창 생성 및 버튼 화면 조절
root = Tk()
root.title("텔레그램 자동화")
root.geometry("300x300+500+300")
root.resizable(False, FALSE)

frame0 = LabelFrame(root, text='프로그램 시작', padx=60, pady=10)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백

addAddr = IntVar()
addAddrVal = Checkbutton(frame0,text="연락처 추가",variable=addAddr)
addAddrVal.select()
addAddrVal.pack()

joinGroup = IntVar()
joinGroupVal = Checkbutton(frame0,text="그룹초대",variable=joinGroup)
joinGroupVal.select()
joinGroupVal.pack()

# 시작 버튼 생성
startBtn = Button(frame0, text='텔레그램 자동화', command=th, padx=50)
startBtn.pack()

frame1 = LabelFrame(root, text='인증관련', padx=60, pady=10)  # padx / pady 내부여백
frame1.pack(padx=10, pady=5)  # padx / pady 외부여백

authBtn = Button(frame1, text='인증따기 / 확인', command=th2, padx=50)
authBtn.pack()

delAuthBtn = Button(frame1, text='인증삭제', command=th3, padx=50)
delAuthBtn.pack()

invite = Button(frame1, text='관리자추가', command=th4, padx=50)
invite.pack()

# ********************************

# 윈도우창 계속 띄우기
root.mainloop()
