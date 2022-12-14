
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
import openpyxl

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
        
    # with open("./result_image/0result.txt", "w") as f:
    #     f.write("start~~~~\n")
    
    
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
    
    workCreate = openpyxl.load_workbook('create_link.xlsx')
    sheet = workCreate.get_sheet_by_name('Sheet1')
    
    
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
    
    if setTong == 'SK':
        createCount = 6
    elif setTong == 'KT':
        createCount = 15
    else:
        createCount = 24
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
                    
                    ws.cells(5,2).Value = f'{setTong} {deviceName} {capa}'
                    ws.cells(5,12).Value = f'{setTong} {deviceName} {capa}'
                    ws.cells(7,4).Value = fPrice_list[idx]
                    ws.cells(7,15).Value = fPrice_list[idx]
                    setCount = 7
                    for idg, basicFee in enumerate(yogFeeList):
                        ws.cells(5,5).Value = "번호이동 공시지원금 요금제표"
                        ws.cells(setCount+idg,5).Value = gongsi_list[idg]
                        setMnpgHalwon = fPrice_list[idx] - gongsi_list[idg] - mnp_ghal_list[idg]
                        if setMnpgHalwon < 0:
                            setMnpgHalwon = 0
                        setMnpgMonthHal = math.ceil(setMnpgHalwon / 24)
                        ws.cells(setCount+idg,7).Value = setMnpgHalwon
                        ws.cells(setCount+idg,8).Value = setMnpgMonthHal
                        ws.cells(setCount+idg,9).Value = basicFee + setMnpgMonthHal
                        
                        
                        ws.Range(ws.Cells(5,2),ws.Cells(13,9)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong}_{pre_val}_{capa}_mnp_gongsi.png')
                        img.save(imgFile)
                        
                        ws.cells(5,15).Value = "번호이동 선택약정 요금제표"
                        setMnpsHalwon = fPrice_list[idx] - mnp_shal_list[idg]
                        if setMnpsHalwon < 0:
                            setMnpsHalwon = 0
                        setMnpsMonthHal = math.ceil(setMnpsHalwon / 24)
                        
                        ws.cells(setCount+idg,17).Value = setMnpsHalwon
                        ws.cells(setCount+idg,18).Value = setMnpsMonthHal
                        ws.cells(setCount+idg,19).Value = basicFee + yogShalList[idg] + setMnpsMonthHal
                        
                        ws.Range(ws.Cells(5,12),ws.Cells(13,19)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong}_{pre_val}_{capa}_mnp_sunyak.png')
                        img.save(imgFile)
                        
                    for idg, basicFee in enumerate(yogFeeList):
                        ws.cells(5,5).Value = "기기변경 공시지원금 요금제표"
                        ws.cells(setCount+idg,5).Value = gongsi_list[idg]
                        setgHalwon = fPrice_list[idx] - gongsi_list[idg] - gib_ghal_list[idg]
                        if setgHalwon < 0:
                            setgHalwon = 0
                        setgMonthHal = math.ceil(setgHalwon / 24)
                        ws.cells(setCount+idg,7).Value = setgHalwon
                        ws.cells(setCount+idg,8).Value = setgMonthHal
                        ws.cells(setCount+idg,9).Value = basicFee + setgMonthHal
                        
                        
                        ws.Range(ws.Cells(5,2),ws.Cells(13,9)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong}_{pre_val}_{capa}_gib_gongsi.png')
                        img.save(imgFile)

                        
                        ws.cells(5,15).Value = "기기변경 선택약정 요금제표"
                        setsHalwon = fPrice_list[idx] - gib_shal_list[idg]
                        if setsHalwon < 0:
                            setsHalwon = 0
                        setsMonthHal = math.ceil(setsHalwon / 24)
                        
                        ws.cells(setCount+idg,17).Value = setsHalwon
                        ws.cells(setCount+idg,18).Value = setsMonthHal
                        ws.cells(setCount+idg,19).Value = basicFee + yogShalList[idg] + setsMonthHal
                        
                        ws.Range(ws.Cells(5,12),ws.Cells(13,19)).Copy()  
                        img = ImageGrab.grabclipboard()
                        imgFile = os.path.join(f'{os.getcwd()}/result_image',f'{setTong}_{pre_val}_{capa}_gib_sunyak.png')
                        img.save(imgFile)
                    
                    createCount += 1
                    with open("./result_image/0result.txt", "a") as f:
                        f.write(f'{setTong}_{pre_val}_{capa}_gib_gongsi.png,{setTong}_{pre_val}_{capa}_gib_sunyak.png,{setTong}_{pre_val}_{capa}_mnp_gongsi.png,{setTong}_{pre_val}_{capa}_mnp_sunyak.png\n')
                        
                        sheet.cell(2,createCount).value = f'{setTong}_{pre_val}_{capa}_gib_gongsi.png,{setTong}_{pre_val}_{capa}_gib_sunyak.png,{setTong}_{pre_val}_{capa}_mnp_gongsi.png,{setTong}_{pre_val}_{capa}_mnp_sunyak.png'
                        workCreate.save('create_link.xlsx')
                        
                        
                        f.write(f'{setTong}_{pre_val}_{capa}_gib_gongsi.png\n')
                        f.write(f'{setTong}_{pre_val}_{capa}_gib_sunyak.png\n')
                        f.write(f'{setTong}_{pre_val}_{capa}_mnp_gongsi.png\n')
                        f.write(f'{setTong}_{pre_val}_{capa}_mnp_sunyak.png\n\n')
                        
                    
                    
                    
                    


                    
                    
                    # basicCount = basicCount + 10
                    # break
                    
                    # getNowCapa = workSheet.acell(f'{chr(capaAsc)}{basicCount}').value
                    # getNowfPrice = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # for i in range(5):
                    #     for k in range(7):
                    #         getGongsi = workSheet.acell(f'{chr(capaAsc)}{basicCount+1}').value
                    
                    # if getNowCapa is None:
                    #     break
        pre_val = tempVal
        

    
   

    # wb = excel.Workbooks.Open(f'{os.getcwd()}/test_ex.xlsx')
    # ws = wb.Worksheets['sk_sheet']
    
    # chkVal = ws.cells(5,2).Value

    # ws.Range(ws.Cells(5,2),ws.Cells(13,8)).Copy()  
    # img = ImageGrab.grabclipboard()
    # imgFile = os.path.join(os.getcwd(),'test.jpg')
    # img.save(imgFile)
    
    
    # excel.Quit()
    
    
def make_link():
    # 엑셀파일 열기
    excel = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    excel.visible = False
    
    wb = excel.Workbooks.Open(f'{os.getcwd()}/create_link.xlsx')
    ws = wb.Worksheets['Sheet1']
    
    with open("./create_link.txt", "w") as f:
        f.write('생성시작\n\n')
    
    
    plusCount = 0
    while True:
        
        bc = 2+plusCount
        if ws.cells(bc,1).Value is None:
            break
        
        linkText = "http://ts-phone.com/test/update_get.php"
        it_id = f"?it_id={ws.cells(2+plusCount,2).Value}"
        linkText = linkText + it_id
        
        set_tong = f"&it_shop_memo={ws.cells(2+plusCount,3).Value}"
        linkText = linkText + set_tong
        
        set_theme = f"&it_skin={ws.cells(2+plusCount,4).Value}"
        linkText = linkText + set_theme
        # sk_item_list = f"?sk_item_list={ws.cells(2+plusCount,2)}"
        
        sc = 5
        for k in range(3):
            for i in range(9):
                nc = sc + i
                if ws.cells(bc,nc).Value is not None:
                    linkText = linkText + f"&{ws.cells(1,nc).Value}={ws.cells(bc,nc).Value}"
            sc = sc + 9
        pg.alert(linkText)
        
        with open("./create_link.txt", "a") as f:
            f.write(f'{linkText}\n\n')
        plusCount += 1
    
    
            
    pg.alert('종료합니다!!')
    excel.Quit()
    
    
def gogoScript(getDict):
    
    
    a = ["a/b/c","d","e"]
    string = ''.join(a)
    print(string)
    pg.alert(string)
    
    
    
    
    pg.alert('여기 맞지??')
    
    if getDict['getTong'] == 0:
        setTong = 'SK'
    elif getDict['getTong'] == 1:
        setTong = 'KT'
    else:
        setTong = 'LG'
        
    # with open("./result_image/0result.txt", "w") as f:
    #     f.write("start~~~~\n")
    
    
    # 스프레드 시트 열기
    json_file_name = 'ecstatic-magpie-310310-5c58a2ab08ef.json'
    gc = gspread.service_account(filename=json_file_name)
    
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1gWxGWnVPMBN6qDrHglE75Qn5j2Fq9sixEX14mW8qsMo/edit?usp=sharing')
    workSheet = doc.worksheet(setTong)
    
    if not getDict['getLine']:
        basicCount = 0
    else:
        basicCount = int(getDict['getLine'])
    
    # yogInfoList = workSheet.range(f'B1:H3')
    # yogNameList = getArr(yogInfoList, 0)
    # yogFeeList = getArr(yogInfoList, 7)
    # yogDataList = getArr(yogInfoList, 14)
    
    # yogShalList = []
    # for i, val in enumerate(yogFeeList):
    #     sHalVal = math.ceil(val * 0.25) * -1
    #     yogShalList.append(sHalVal)

    
    while True:
        basicCount += 1
        tempVal = workSheet.acell(f'A{basicCount}').value
        if tempVal == 'STOP':
            pg.alert('작업이 완료 되었습니다!')
            break
        if tempVal is not None:
            if '갤럭시' in tempVal or '아이폰' in tempVal:
                deviceName = tempVal
                
                all_list = workSheet.range(f'B{basicCount}:H{basicCount+9}')
                capa_list = getArr(all_list, 0, 'ok')
                fPrice_list = getArr(all_list, 7, 'ok')
                gongsi_list = getArr(all_list, 14)        
                mnp_ghal_list = getArr(all_list, 42)
                mnp_shal_list = getArr(all_list, 49)
                gib_ghal_list = getArr(all_list, 56)
                gib_shal_list = getArr(all_list, 63)
                
                for val in fPrice_list:
                    pg.alert(
                        f"{val}|{','.join(str(_) for _ in gongsi_list)}|{','.join(str(_) for _ in gib_ghal_list)}|{','.join(str(_) for _ in gib_shal_list)}|{','.join(str(_) for _ in mnp_ghal_list)}|{','.join(str(_) for _ in mnp_shal_list)}"
                    )
                
                pg.alert(capa_list)
                pg.alert(fPrice_list)
                pg.alert(gongsi_list)
                pg.alert(mnp_ghal_list)
                pg.alert(mnp_shal_list)
                pg.alert(gib_ghal_list)
                pg.alert(gib_shal_list)



def calculScript(getDict):
    
    pg.alert('여기 맞지??')

        
    goTongArr = getDict['goTong'].split(',')
    pg.alert(goTongArr)
    
    getLineArr = getDict['getLine'].split(',')
    pg.alert(getLineArr)
    try:
        int(getLineArr[0])
    except:
        pg.alert('라인을 입력해주세요! 종료합니다!')
        return
    
    
    # 스프레드 시트 열기
    json_file_name = 'ecstatic-magpie-310310-5c58a2ab08ef.json'
    gc = gspread.service_account(filename=json_file_name)
    
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1gWxGWnVPMBN6qDrHglE75Qn5j2Fq9sixEX14mW8qsMo/edit?usp=sharing')
    
    for idx, nowTong in enumerate(goTongArr):
        workSheet = doc.worksheet(nowTong)
        basicCount = int(getLineArr[idx])
        while True:
            basicCount += 1
            tempVal = workSheet.acell(f'A{basicCount}').value
            if tempVal is not None:
                if '갤럭시' in tempVal or '아이폰' in tempVal:
                    deviceName = tempVal
                    
                    if nowTong == 'SK':
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
                    
                    pg.alert(deviceName)
                    pg.alert(capa_list)
                    pg.alert(fPrice_list)
                    pg.alert(gongsi_list)
                    pg.alert(mnp_ghal_list)
                    pg.alert(mnp_shal_list)
                    pg.alert(gib_ghal_list)
                    pg.alert(gib_shal_list)
                    
                    break
    pg.alert('완료 되었습니다!')
    
    
    





    
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

def getArrToStr(setList, setNum, ok=''):
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
    
    temp_str = ','.join(str(_) for _ in temp_arr)
    return temp_str
        
def setBasicTable(ex, list, scount, gcount = ''):
    startCount = 7
    for i, val in enumerate(list):
        ex.cells(startCount+i,scount).Value = val
        if gcount:
            ex.cells(startCount+i,gcount).Value = val
        