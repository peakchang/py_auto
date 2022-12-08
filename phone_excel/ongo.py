
import random
import threading
import math
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
    
    if getDict['getTong'] == 0:
        setTong = 'SK'
    elif getDict['getTong'] == 1:
        setTong = 'KT'
    else:
        setTong = 'LG'
        
    
    
    
    # 스프레드 시트 열기
    json_file_name = 'ecstatic-magpie-310310-5c58a2ab08ef.json'
    gc = gspread.service_account(filename=json_file_name)
    
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1gWxGWnVPMBN6qDrHglE75Qn5j2Fq9sixEX14mW8qsMo/edit?usp=sharing')
    workSheet = doc.worksheet(setTong)
    
    # 엑셀파일 열기
    excel = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    excel.visible = False
    
    wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    ws = wb.Worksheets['onSheet']
    
    if not getDict['getLine']:
        basicCount = 0
    else:
        basicCount = int(getDict['getLine'])
    
    yogInfoList = workSheet.range(f'B1:H3')
    yogNameList = getArr(yogInfoList, 0)
    yogFeeList = getArr(yogInfoList, 7)
    yogDataList = getArr(yogInfoList, 14)
    
    yogShalList = []
    for i, val in enumerate(yogFeeList):
        sHalVal = math.ceil(val * 0.25) * -1
        yogShalList.append(sHalVal)
        
    setBasicTable(ws, yogNameList, 12, 2)
    setBasicTable(ws, yogFeeList, 13, 3)
    setBasicTable(ws, yogDataList, 16, 6)
    setBasicTable(ws, yogShalList, 14)
    
    while True:
        basicCount += 1
        tempVal = workSheet.acell(f'A{basicCount}').value
        if tempVal == 'STOP':
            excel.Quit()
            pg.alert('작업이 완료 되었습니다!')
            break
        if tempVal is not None:
            if '갤럭시' in tempVal or '아이폰' in tempVal:
                deviceName = tempVal
                
                if setTong == 'SK':
                    all_list = workSheet.range(f'B{basicCount}:H{basicCount+9}')
                    capa_list = getArr(all_list, 0, 'ok')
                    fPrice_list = getArr(all_list, 7, 'ok')
                    gongsi_list = getArr(all_list, 14)
                    
                    mnp_ghal_list = getArr(all_list, 42)
                    mnp_shal_list = getArr(all_list, 49)
                    
                    gib_ghal_list = getArr(all_list, 56)
                    gib_shal_list = getArr(all_list, 63)
                else:
                    all_list = workSheet.range(f'B{basicCount}:H{basicCount+8}')
                    capa_list = getArr(all_list, 0, 'ok')
                    fPrice_list = getArr(all_list, 7, 'ok')
                    gongsi_list = getArr(all_list, 14)
                    
                    mnp_ghal_list = getArr(all_list, 35)
                    mnp_shal_list = getArr(all_list, 42)
                    
                    gib_ghal_list = getArr(all_list, 49)
                    gib_shal_list = getArr(all_list, 56)
                
                
                for idx, capa in enumerate(capa_list):
                    ws.cells(5,2).Value = f'SK {deviceName} {capa}'
                    ws.cells(5,12).Value = f'SK {deviceName} {capa}'
                    ws.cells(7,4).Value = fPrice_list[idx]
                    ws.cells(7,15).Value = fPrice_list[idx]
                    setCount = 7
                    for idg, basicFee in enumerate(yogFeeList):
                        ws.cells(5,4).Value = "번호이동 공시지원금 요금제표"
                        ws.cells(setCount+idg,5).Value = gongsi_list[idg]
                        setMnpgHalwon = fPrice_list[idx] - gongsi_list[idg] - mnp_ghal_list[idg]
                        setMnpgMonthHal = math.ceil(setMnpgHalwon / 24)
                        ws.cells(setCount+idg,7).Value = setMnpgHalwon
                        ws.cells(setCount+idg,8).Value = setMnpgMonthHal
                        ws.cells(setCount+idg,9).Value = basicFee + setMnpgMonthHal
                        
                        
                        ws.Range(ws.Cells(5,2),ws.Cells(13,9)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong} {deviceName} {capa} 번호이동 공시지원금 요금제표.png')
                        img.save(imgFile)
                        
                        ws.cells(5,14).Value = "번호이동 선택약정 요금제표"
                        setMnpsHalwon = fPrice_list[idx] - mnp_shal_list[idg]
                        setMnpsMonthHal = math.ceil(setMnpsHalwon / 24)
                        
                        ws.cells(setCount+idg,17).Value = setMnpsHalwon
                        ws.cells(setCount+idg,18).Value = setMnpsMonthHal
                        ws.cells(setCount+idg,19).Value = basicFee + yogShalList[idg] + setMnpsMonthHal
                        
                        ws.Range(ws.Cells(5,12),ws.Cells(13,19)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong} {deviceName} {capa} 번호이동 선택약정 요금제표.png')
                        img.save(imgFile)
                        
                        
                    for idg, basicFee in enumerate(yogFeeList):
                        ws.cells(5,4).Value = "기기변경 공시지원금 요금제표"
                        ws.cells(setCount+idg,5).Value = gongsi_list[idg]
                        setgHalwon = fPrice_list[idx] - gongsi_list[idg] - gib_ghal_list[idg]
                        setgMonthHal = math.ceil(setgHalwon / 24)
                        ws.cells(setCount+idg,7).Value = setgHalwon
                        ws.cells(setCount+idg,8).Value = setgMonthHal
                        ws.cells(setCount+idg,9).Value = basicFee + setgMonthHal
                        
                        
                        ws.Range(ws.Cells(5,2),ws.Cells(13,9)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong} {deviceName} {capa} 기기변경 공시지원금 요금제표.png')
                        img.save(imgFile)
                        
                        ws.cells(5,14).Value = "기기변경 선택약정 요금제표"
                        setsHalwon = fPrice_list[idx] - gib_shal_list[idg]
                        setsMonthHal = math.ceil(setsHalwon / 24)
                        
                        ws.cells(setCount+idg,17).Value = setsHalwon
                        ws.cells(setCount+idg,18).Value = setsMonthHal
                        ws.cells(setCount+idg,19).Value = basicFee + yogShalList[idg] + setsMonthHal
                        
                        ws.Range(ws.Cells(5,12),ws.Cells(13,19)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong} {deviceName} {capa} 기기변경 선택약정 요금제표.png')
                        img.save(imgFile)
                        
                    
                    
                    
                    
                    


                    
                    
                    # basicCount = basicCount + 10
                    # break
                    
                    # getNowCapa = workSheet.acell(f'{chr(capaAsc)}{basicCount}').value
                    # getNowfPrice = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # for i in range(5):
                    #     for k in range(7):
                    #         getGongsi = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # if getNowCapa is None:
                    #     break
        

    
   

    # wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    # ws = wb.Worksheets['sk_sheet']
    
    # chkVal = ws.cells(5,2).Value

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
        
def setBasicTable(ex, list, scount, gcount = ''):
    startCount = 7
    for i, val in enumerate(list):
        ex.cells(startCount+i,scount).Value = val
        if gcount:
            ex.cells(startCount+i,gcount).Value = val
        