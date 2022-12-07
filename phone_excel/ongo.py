
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
    
    
    # 스프레드 시트 열기
    json_file_name = 'ecstatic-magpie-310310-5c58a2ab08ef.json'
    gc = gspread.service_account(filename=json_file_name)
    
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1gWxGWnVPMBN6qDrHglE75Qn5j2Fq9sixEX14mW8qsMo/edit?usp=sharing')
    workSheet = doc.worksheet('SK')
    
    # 엑셀파일 열기
    excel = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    excel.visible = False
    
    wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    ws = wb.Worksheets['onSheet']
    
    
    basicCount = 0
    endCount = 0
    
    yogInfoList = workSheet.range(f'B1:H3')
    yogNameList = getArr(yogInfoList, 0)
    yogFeeList = getArr(yogInfoList, 7)
    yogDataList = getArr(yogInfoList, 14)
    
    
    
    startCount = 7
    for i, val in enumerate(yogNameList):
        ws.cells(startCount+i,2).Value = val
    
    
    excel.Quit()
    pg.alert('대기~~~')
        
    pg.alert(yogNameList)
    pg.alert(yogFeeList)
    pg.alert(yogDataList)
    
    
    
    
    
    
    while True:
        basicCount += 1
        tempVal = workSheet.acell(f'A{basicCount}').value
        if tempVal == 'STOP':
            pg.alert('작업이 완료 되었습니다!')
            break
        if tempVal is not None:
            endCount = 0
            if '갤럭시' in tempVal or '아이폰' in tempVal:
                while True:
                    
                    deviceName = tempVal
                    all_list = workSheet.range(f'B{basicCount}:H{basicCount+9}')
                    capa_list = getArr(all_list, 0, 'ok')
                    fPrice_list = getArr(all_list, 7, 'ok')
                    gongsi_list = getArr(all_list, 14)
                    mnp_ghal_list = getArr(all_list, 42)
                    mnp_shal_list = getArr(all_list, 49)
                    gib_ghal_list = getArr(all_list, 56)
                    gib_shal_list = getArr(all_list, 63)
                    
                    

                    # gongsi_list = workSheet.range(f'B{basicCount+2}:H{basicCount+2}')
                    # mnp_ghal_list = workSheet.range(f'B{basicCount+6}:H{basicCount+6}')
                    # mnp_shal_list = workSheet.range(f'B{basicCount+7}:H{basicCount+7}')
                    # gib_ghal_list = workSheet.range(f'B{basicCount+8}:H{basicCount+8}')
                    # gib_shal_list = workSheet.range(f'B{basicCount+9}:H{basicCount+9}')
                    
                    # pg.alert(capa_list)
                    
                    # pg.alert(fPrice_list)
                    # pg.alert(gongsi_list)
                    # pg.alert(mnp_ghal_list)
                    # pg.alert(mnp_shal_list)
                    # pg.alert(gib_ghal_list)
                    # pg.alert(gib_shal_list)
                    
                    # basicCount = basicCount + 10
                    # break
                    
                    # getNowCapa = workSheet.acell(f'{chr(capaAsc)}{basicCount}').value
                    # getNowfPrice = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # for i in range(5):
                    #     for k in range(7):
                    #         getGongsi = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # if getNowCapa is None:
                    #     break
        
    
    # for i in range(10):
    #     if i == 0:
    #         continue
    #     tempList = workSheet.acell(f'B{i}').value
    #     pg.alert(tempList)
    # print('나ㅣㅓ이러니야러ㅣㅑㄴ어리ㅑ넝ㄹ')
    
   

    # wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    # ws = wb.Worksheets['sk_sheet']
    
    # chkVal = ws.cells(5,2).Value
    # pg.alert(chkVal)

    # ws.Range(ws.Cells(5,2),ws.Cells(13,8)).Copy()  
    # img = ImageGrab.grabclipboard()
    # imgFile = os.path.join(os.getcwd(),'test.jpg')
    # img.save(imgFile)
    
    
    # excel.Quit()
    
    
def getArr(setList, setNum, ok=''):
    temp_list = setList[setNum:setNum+7]
    temp_arr = []
    for val in temp_list:
        if not val.value:
            if ok:
                continue
            else:
                temp_arr.append(0)
        else:
            try:
                setVal = int(val.value)
            except:
                setVal = val.value
            temp_arr.append(setVal)
    return temp_arr
        
        