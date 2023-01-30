import random
import threading
import time
from datetime import datetime, timedelta, date
import sys
import os
from pathlib import Path
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


def changeToKorean(driver, fore):
    while True:
        menuList = showTeleMenu(driver)
        if '메시지' in menuList[0].text:
            goToMain(driver, fore)
            break
        else:
            menuList[3].click()
            wait_float(0.5,0.9)
            listItem = searchWaitElement('.settings-main-menu .ListItem', driver)
            for item in listItem:
                if "Language" in item.text or "언어" in item.text:
                    item.click()
            wait_float(0.5,0.9)
            listRadio = searchWaitElement('.settings-language .Radio', driver)
            listRadio[0].click()
            while True:
                wait_float(0.5,1.2)
                try:
                    backBtnWrap = driver.find_elements(by=By.CSS_SELECTOR, value='#Settings > div')
                    backBtn = backBtnWrap[1].find_element(by=By.CSS_SELECTOR, value='.translucent')
                    backBtn.click()
                except:
                    pass
                
                try:
                    hamBtn = driver.find_element(by=By.CSS_SELECTOR, value='.LeftMainHeader .DropdownMenu')
                    if hamBtn:
                        wait_float(1.9,2.5)
                        pg.press('F5')
                        wait_float(1.2,1.9)
                        break
                except:
                    pass

def searchTextAndClick(compareText, clickEle, driver):
    while True:
        try:
            wait_float(0.9,1.5)
            manageText = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
            if manageText.text == compareText:
                break
        except:
            pass
        
        try:
            wait_float(0.9,1.5)
            delManageBtn = driver.find_element(by=By.CSS_SELECTOR, value=clickEle)
            delManageBtn.click()
        except:
            pass

def addAddr(driver,fore,addPhAddr,getPhNum):
    while True:
        # print('연락처 추가하기! 모달창 키고 번호 입력!')
        focus_window('Telegram')
        
        try:
            wait_float(1.2,1.9)
            menuList = showTeleMenu(driver)
            menuList[2].click()
        except:
            wait_float(0.5,1.2)
            pg.click(fore.left+500,fore.top+300)
            wait_float(0.5,1.2)
            continue
        
        try:
            wait_float(0.9,1.2)
            addrWrapList = driver.find_elements(by=By.CSS_SELECTOR, value='#LeftColumn-main .Transition.zoom-fade>div')
            addrList = addrWrapList[1].find_elements(by=By.CSS_SELECTOR, value='.ListItem')
            if len(addrList) >= 6:
                maxAddrFull = 'on'
                return maxAddrFull
        except:
            continue
            
        
        try:
            wait_float(0.9,1.5)
            addAddressBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
            wait_float(0.5,1.2)
            addAddressBtn.click()
        except:
            wait_float(0.5,1.2)
            pg.click(fore.left+500,fore.top+300)
            wait_float(0.5,1.2)
            continue
        
        try:
            wait_float(1.2,1.9)
            inputList = driver.find_elements(by=By.CSS_SELECTOR, value='.NewContactModal__new-contact-fieldset .form-control')
            inputList[0].click()
            inputList[0].send_keys(addPhAddr)
            wait_float(1.2,1.9)
            inputList[1].send_keys(getPhNum)
            wait_float(0.5,1.2)
            okBtn = driver.find_elements(by=By.CSS_SELECTOR, value='.confirm-dialog-button')
            okBtn[1].click()
            return
        except:
            continue


def changePhNum(getPhNum):
    getPhNum = re.sub(r'[^0-9]', '', str(getPhNum))
    if getPhNum[0:1] != '0':
        getPhNum = f"0{getPhNum}"
    addPhAddr = f"+82{getPhNum[1:]}"
    return addPhAddr

def searchAndClick(searchEle, clickEle, driver, addCode=0, addEle=''):
    while True:
        try:
            wait_float(0.9,1.5)
            click_ele = driver.find_elements(by=By.CSS_SELECTOR, value=clickEle)
            click_ele[0].click()
        except:
            pass
        
        try:
            wait_float(0.9,1.5)
            search_ele = driver.find_element(by=By.CSS_SELECTOR, value=searchEle)
            if search_ele:
                break
        except:
            pass
        
        if addCode:
            try:
                add_ele = driver.find_element(by=By.CSS_SELECTOR, value=addEle)
                add_ele.click()
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

def goToMain(driver,fore):
    setCount = 0
    while True:
        # print('메인으로!!!!!!')
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
    focus_window('Telegram')
    while True:
        # print(ele + ' 찾는중임!!!')
        try:
            element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, ele)))
            if element:
                selected_element = driver.find_elements(by=By.CSS_SELECTOR, value=ele)
                break
        except:
            wait_float(1.5, 2.2)
            pass
    
    return selected_element



def wrongUserWork(driver,fore,setUserName):
    goToMain(driver,fore)
    while True:
        try:
            wait_float(1.2,1.9)
            addrWrapList = driver.find_elements(by=By.CSS_SELECTOR, value='#LeftColumn-main .Transition.zoom-fade>div')
            if len(addrWrapList) < 2:
                raise Exception('연락처를 선택 안함')
            else:
                break
        except:
            pass
        
        try:
            wait_float(1.2,1.9)
            menuList = showTeleMenu(driver)
            menuList[2].click()
        except:
            wait_float(0.5,1.2)
            pg.click(fore.left+500,fore.top+300)
            wait_float(0.5,1.2)
            continue
        
    while True:
        try:
            getName = driver.find_element(by=By.CSS_SELECTOR, value='.MiddleHeader .ChatInfo .fullName')
            getUserName = re.sub(r'[^0-9]', '', getName.text)
            if getUserName == setUserName:
                break
        except:
            pass
        
        try:
            addrWrapList = driver.find_elements(by=By.CSS_SELECTOR, value='#LeftColumn-main .Transition.zoom-fade>div')
            addrList = addrWrapList[1].find_elements(by=By.CSS_SELECTOR, value='.ListItem')
            for addr in addrList:
                getUserName = re.sub(r'[^0-9]', '', addr.text)
                if setUserName in getUserName:
                    addr.click()
                    break
        except:
            pass
        
    # print("연락처 삭제 준비, 삭제 아이콘 나오게")
    searchAndClick('.icon-delete', '.tools button', driver)

    # 연락처 삭제 모달창 띄우기
    # print("연락처 삭제 모달창 띄우기")
    searchAndClick('.Modal', '.destructive', driver)
        
    # 연락처 삭제 완료
    searchTextAndClick('회원 정보', '.Modal .confirm-dialog-button.default.danger.text', driver)
    goToMain(driver,fore)



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
        # pg.alert(text=f"{win_list}")
    # 윈도우 타이틀에 Chrome 이 포함된 모든 윈도우 수집, 리스트로 리턴
    win = gw.getWindowsWithTitle(winName)[0]
    win.activate()  # 윈도우 활성화
