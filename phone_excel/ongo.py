
import random
import threading
import time
from datetime import date, datetime, timedelta
import sys
import os
from pathlib import Path
from typing import Optional
import pyautogui as pg
import json
import re
from PIL import ImageGrab

import win32com.client
# from openpyxl import load_workbook
from tkinter import *
from tkinter import ttk
import winsound as ws
import pythoncom
import gspread

"""
주요 변수
nowAction ( write / reply ) / 글쓰는지 댓글인지 체크
nowWriteStatus (optimize / basic ) / 최적화인지 아닌지 체크
allCount : 전체 변수, 글 / 댓글 나누기 위함
writeCount : 글쓰기 변수 nowAction 이 write일때 하나씩 증가, 최적화 아이디인지 판별하기 위함

cafe_id.cell(세로(열), 가로(행)).value
"""

###


def goScript(getDict):
    
    json_file_name = 'ecstatic-magpie-310310-5c58a2ab08ef.json'
    gc = gspread.service_account(filename=json_file_name)
    
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1gWxGWnVPMBN6qDrHglE75Qn5j2Fq9sixEX14mW8qsMo/edit?usp=sharing')
    workSheet = doc.worksheet('SK')
    
    basicCount = 0
    endCount = 0
    while True:
        basicCount += 1
        tempVal = workSheet.acell(f'A{basicCount}').value
        pg.alert(tempVal)
        if tempVal == 'STOP':
            pg.alert('작업이 완료 되었습니다!')
            break
        if tempVal is not None:
            endCount = 0
            if '갤럭시' in tempVal or '아이폰' in tempVal:
                capaAsc = 65
                while True:
                    capaAsc += 1
                    getNowCapa = workSheet.acell(f'{chr(capaAsc)}{basicCount}').value
                    getNowfPrice = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    for i in range(5):
                        for k in range(7):
                            getGongsi = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    if getNowCapa is None:
                        break
        
    
    # for i in range(10):
    #     if i == 0:
    #         continue
    #     tempList = workSheet.acell(f'B{i}').value
    #     pg.alert(tempList)
    # print('나ㅣㅓ이러니야러ㅣㅑㄴ어리ㅑ넝ㄹ')
    
    # xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    # excel = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    # excel.visible = False

    # wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    # ws = wb.Worksheets['sk_sheet']
    
    # chkVal = ws.cells(5,2).Value
    # pg.alert(chkVal)

    # ws.Range(ws.Cells(5,2),ws.Cells(13,8)).Copy()  
    # img = ImageGrab.grabclipboard()
    # imgFile = os.path.join(os.getcwd(),'test.jpg')
    # img.save(imgFile)
    
    
    # excel.Quit()