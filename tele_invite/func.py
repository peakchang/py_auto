import random
import threading
import time
from datetime import datetime, timedelta, date
import sys
import os
from pathlib import Path
from typing import Optional
# from pyparsing import And
# import requests
# from bs4 import BeautifulSoup as bs
import json
import re
import pyautogui as pg
import pyperclip
import pygetwindow as gw
import clipboard as cb
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ppadb.client import Client as AdbClient
from tkinter import *
import tkinter
from tkinter import ttk
import requests
import winsound as ws
import glob
import asyncio
import socket
import getpass

import shutil
import winsound as sd









# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>함수 시작염

# 상품 들어가서 스크롤 내리고 나오기


def searchNextBtn(resultEle, clickEle, driver):
    while True:
        wait_float(1.2,1.9)
        try:
            modal = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, resultEle)))
            if modal:
                break
        except:
            pass
        
        try:
            delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, clickEle)))
            delIcon.click()
        except:
            pass

def compareDate(getDateText,minus_date):
    getDateText = re.sub(r'[\uAC00-\uD7A3a-zA-Z\s]', '', getDateText)[:-1].split('.')
    getDate = datetime(int(getDateText[0]), int(getDateText[1]), int(getDateText[2]))

    now = datetime.now()
    todayStr = f"{now.date().strftime('%Y-%m-%d')} 00:00:00:00"
    datetime_format = "%Y-%m-%d %H:%M:%S:%f"
    getToday = datetime.strptime(todayStr,datetime_format)
    getBrfoer4Day = getToday - timedelta(days=minus_date)
    
    return getDate > getBrfoer4Day
    
    

def changeIp():
    try:
        os.system('adb server start')
        client = AdbClient(host="127.0.0.1", port=5037)
        device = client.devices()  # 디바이스 1개
        ondevice = device[0]
        ondevice.shell("input keyevent KEYCODE_POWER")
        ondevice.shell("svc data disable")
        ondevice.shell("settings put global airplane_mode_on 1")
        ondevice.shell(
            "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true")

        ondevice.shell("svc data enable")
        ondevice.shell("settings put global airplane_mode_on 0")
        ondevice.shell(
            "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false")
        time.sleep(3)
        while True:
            try:
                wait_float(0.5, 0.9)
                getIp = requests.get("https://api.ip.pe.kr/json/").json()['ip']
                if getIp is not None:
                    break
            except:
                continue
    except:

        while True:
            try:
                wait_float(0.5, 0.9)
                getIp = requests.get("https://api.ip.pe.kr/json/").json()['ip']
                if getIp is not None:
                    break
            except:
                continue
    return getIp

# def clickBackBtn(driver):
#     preBtn = searchWaitElement('.left-header .Button.translucent', driver)
#     for btn in preBtn:
#         try:
#             btn.click()
#             wait_float(1.5,2.2)
#             return
#         except:
#             pass

def goToMain(driver,fore):
    setCount = 0
    while True:
        print('메인으로!!!!!!')
        wait_float(0.5,1.2)
        setCount += 1
        if setCount > 3:
            pg.click(fore.left+500,fore.top+300)
            wait_float(1.2,2.2)
            
        try:
            chkSuccessMain = driver.find_element(by=By.CSS_SELECTOR, value='.LeftMainHeader .Button.translucent')
            chkAttr = chkSuccessMain.get_attribute('title')
            
            if "메뉴" in chkAttr:
                focus_window('Telegram')
                pg.press('F5')
                return
        except:
            pass
        
        try:
            backBtn = driver.find_element(by=By.CSS_SELECTOR, value='.LeftMainHeader .Button.translucent')
            backBtn.click()
        except:
            pass
        
        

def showTeleMenu(driver):
    while True:
        wait_float(0.5,0.9)
        
        try:
            hamBtn = driver.find_element(by=By.CSS_SELECTOR, value='.LeftMainHeader .DropdownMenu')
            hamBtn.click()
            wait_float(0.9,1.2)
        except:
            pass
        
        try:
            menuOpenChk = hamBtn.find_element(by=By.CSS_SELECTOR, value='.active')
            if menuOpenChk:
                menuList = hamBtn.find_elements(by=By.CSS_SELECTOR, value='.menu-container.top .MenuItem')
                break
        except:
            pass
        
        
                
        
        
    return menuList


def searchWaitElement(ele,driver):
    while True:
        print(ele + ' 찾는중임!!!')
        try:
            element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, ele)))
            if element:
                selected_element = driver.find_elements(by=By.CSS_SELECTOR, value=ele)
                break
        except:
            wait_float(1.5, 2.2)
            pass
    
    return selected_element



def searchElement(ele,driver):
    wait_float(0.3, 0.7)
    re_count = 0
    element = ""
    while True:
        re_count += 1
        if re_count % 5 == 0:
            print(ele)
            print("새로고침!!!!")
            driver.refresh()
            focus_window('chrome')
            pg.press('F5')
        elif element != "":
            break
        try:
            element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, ele)))
        except:
            pass
        

    selected_element = driver.find_elements(by=By.CSS_SELECTOR, value=ele)
    wait_float(0.3, 0.7)
    return selected_element



def untilEleShow(clickEle, searchEle,driver):
    while True:
        try:
            clickEle.click()
            time.sleep(1)
        except:
            pass
        try:
            btnEle = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, searchEle)))
            if btnEle is not None:
                return
        except:
            continue


def untilEleGone(clickEle, searchEle,driver):
    while True:
        try:
            clickEle.click()
            time.sleep(1)
        except:
            pass
        
        try:
            btnEle = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, searchEle)))
            if btnEle is None:
                return
        except:
            return


def wait_float(start, end):
    wait_ran = random.uniform(start, end)
    time.sleep(wait_ran)


def exitApp(driver):
    pg.alert(text='프로그램을 종료합니다.', title='제목입니다.', button='OK')
    try:
        driver.quit()
    except:
        pass
    sys.exit(0)


def focus_window(winName):
    if winName == 'chkname':
        win_list = gw.getAllTitles()
        pg.alert(text=f"{win_list}")
    # 윈도우 타이틀에 Chrome 이 포함된 모든 윈도우 수집, 리스트로 리턴
    win = gw.getWindowsWithTitle(winName)[0]
    win.activate()  # 윈도우 활성화


BASE_DIR = Path(__file__).resolve().parent




async def getEmptyArr(setNum, exName):
    getArr = []
    asyncio.gather(*[busyFunc(i, getArr, exName) for i in range(1, setNum)])
    return getArr


async def busyFunc(i, getArr, exName):
    getTime = exName.cell(i, 4).value

    try:
        if getTime is None:
            getTime = datetime.now().date()
        if isinstance(getTime, datetime):
            getTime = getTime.date()
        compareTime = datetime.now() - timedelta(days=3)
        if exName.cell(i, 4).value is None or getTime <= compareTime.date():
            getArr.append(i)
    except:
        pass


def getExLength(exName):
    ExLength = 0
    while True:
        ExLength += 1
        if exName.cell(ExLength, 2).value is None:
            break
    return ExLength


def getUaNum():
    with open("./etc/useragent/useragent_all.txt", "r") as f:
        fArr = f.readlines()
        fCount = len(fArr)
        uaSet = random.randrange(0, fCount)
    return uaSet

def mainToCafe(driver):
    shs_item = searchElement('.shs_item',driver)
    for item in shs_item:
        chkCafe = item.find_element(
            by=By.CSS_SELECTOR, value='a').get_attribute('href')
        if 'cafe' in chkCafe:
            untilEleGone(item, '.shs_list')
            break
    
    myCafeGo = searchElement('.mycafe .btn_cafe_more')
    untilEleGone(myCafeGo[0], '.mycafe',driver)



    myCafeList = searchElement('.list_cafe__favorites li',driver)
    with open("./etc/cafe_info.txt", "r") as f:
        getCafeNameList = f.readlines()
        getCafeName = getCafeNameList[0]
        getCafeName = getCafeName.replace(" ", "")
    
    for onCafe in myCafeList:
        chkCafeTitle = onCafe.find_element(by=By.CSS_SELECTOR, value='.title').text
        chkCafeTitle = chkCafeTitle.replace(" ", "")

        if chkCafeTitle in getCafeName:
            untilEleGone(onCafe, '.list_cafe__favorites')
            break
        
    # 카페 진입 끝

# 


# subjectArr
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]
