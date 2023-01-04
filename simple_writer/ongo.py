import pyautogui as pg
from tkinter import *
from tkinter import ttk
import keyboard
import threading
import time
import os.path
import sys

def goScript():
    filename='./content.txt'
    
    
    if not os.path.isfile(filename):
        pg.alert('파일이 존재하지 않습니다. content.txt 파일을 추가해주세요!')
        return
    
    try:
        with open('./content.txt', 'rt', encoding='UTF8') as r:
            getContent = r.readlines()
    except:
         with open('./content.txt', 'r') as r:
            getContent = r.readlines()
            
    pg.alert('글쓰기를 시작합니다. 첫줄은 제목 입니다! 제목 부분을 클릭해주세요!')
    
    time.sleep(3)
    for idx,content in enumerate(getContent):
        content = content.replace('\n', '')
        if content == '' or content is None:
            continue
        
        if content == 'img_line':
            pg.alert('이미지를 넣어주세요! 이후, 엔터 치고 화면을 클릭 해주세요!')
            time.sleep(2)
        else:
            keyboard.write(text=content, delay=0.1)
            
        if idx == 0:
            pg.alert('제목 작성 완료! 본문 부분을 클릭 해주세요!')
        
        pg.press('enter')
        time.sleep(2)
    
    pg.alert('완료! 종료합니다!')
    sys.exit(0)
    
        