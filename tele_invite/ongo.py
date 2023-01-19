from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    pg.alert('왜 시작 안해????')
    
    
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList['auth_id_list']
    
    authCount = 1
    
    while True:
        authCount += 1
        profileNum = authSheet.cell(authCount,1).value
        if profileNum is None:
            break
        
        profileStatus = authSheet.cell(authCount,3).value
        pg.alert(profileStatus)
        if profileStatus is None:
            continue
        if "X" not in profileStatus and "x" not in profileStatus:
            options = Options()
            user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
            service = Service(ChromeDriverManager().install())
            options.add_argument(f"user-data-dir={user_data}")
            options.add_argument(f'--profile-directory=Profile {profileNum}')
            driver = webdriver.Chrome(service=service, chrome_options=options)
            driver.get('https://web.telegram.org/z/')
            pg.alert('대기~~~')
            
            wait_float(2.5,3.2)
            
            notAuth = ''
            okAuth = ''
            while True:
                try:
                    okAuth = driver.find_element(by=By.CSS_SELECTOR, value='#MiddleColumn')
                    if okAuth:
                        break
                except:
                    pass
                
                try:
                    notAuth = driver.find_element(by=By.CSS_SELECTOR, value='#auth-qr-form')
                    if notAuth:
                        break
                except:
                    pass
            if notAuth != '':
                pg.alert('인증이 안되어있옹')
                authSheet.cell(authCount,3).value = '인증XX'
                authList.save('./auth_list.xlsx')
                driver.quit()
                continue
            
            
            menuList = showTeleMenu(driver)
            wait_float(1.2,1.9)
            if '메시지' not in menuList[0].text:
                menuList[3].click()
                wait_float(1.2,1.9)
                listItem = searchWaitElement('.settings-main-menu .ListItem', driver)
                listItem[7].click()
                wait_float(1.2,1.9)
                listRadio = searchWaitElement('.settings-language .Radio', driver)
                listRadio[0].click()
                clickBackBtn(driver)
                clickBackBtn(driver)
                
                wait_float(2.5,3.5)
                pg.press('F5')
            else:
                pass
            
            # 연락처 추가로 이동하기!!!
            while True:
                try:
                    wait_float(0.9,1.7)
                    menuList[2].click()
                    wait_float(0.9,1.7)
                    driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
                    break
                except:
                    menuList = showTeleMenu(driver)
            
            # 연락처 추가 이동 완료!! 사람 추가 반복하자!!
            
            for i in range(9):
                while True:
                    try:
                        addAddressBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
                        addAddressBtn.click()
                        wait_float(1.5,2.2)
                        inputList = driver.find_elements(by=By.CSS_SELECTOR, value='.NewContactModal__new-contact-fieldset .form-control')
                        inputList[0].click()
                        break
                    except:
                        pg.click(400,300)
                        wait_float(1.2,2.2)
                        pass          
                
                pg.alert('대기!!!!')
                
        
        
        
            
        
        pg.alert('다음 작업 합시다~~~~')
            
            
            
            
            
    
    
    
def authListChk():
    
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList['auth_id_list']
    
    authCount = 1
    while True:
        authCount += 1
        profileNum = authSheet.cell(authCount,1).value
        if profileNum is None:
            break
        
        profileStatus = authSheet.cell(authCount,3).value
        if profileStatus == '인증XX' or profileStatus is None:
            options = Options()
            user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
            service = Service(ChromeDriverManager().install())
            options.add_argument(f"user-data-dir={user_data}")
            options.add_argument(f'--profile-directory=Profile {profileNum}')
            driver = webdriver.Chrome(service=service, chrome_options=options)
            driver.get('https://web.telegram.org/z/')
            wait_float(2.5,3.2)
            chkAuth = pg.confirm('인증 완료 후 yes 버튼을 클릭해주세요! 확인만 하신다면 no 버튼을 클릭해주세요!',buttons=['yes','no'])
            if chkAuth == 'yes':
                authSheet.cell(authCount,3).value = '인증완료'
                authList.save('./auth_list.xlsx')
            driver.quit()
    
    pg.alert('인증 작업이 완료 되었습니다. 엑셀 파일을 확인 해주세요!')
    
def delAuthList():
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList['auth_id_list']
    
    authCount = 1
    while True:
        authCount += 1
        profileNum = authSheet.cell(authCount,1).value
        if profileNum is None:
            break
        profileStatus = authSheet.cell(authCount,3).value
        if profileStatus == '인증XX' or profileStatus is None:
            defTargetProfileFolder = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default\\Profile {profileNum}'
            
            if os.path.isdir(defTargetProfileFolder):
                shutil.rmtree(defTargetProfileFolder)
            authSheet.cell(authCount,3).value = ''
            authList.save('./auth_list.xlsx')
            
    pg.alert('인증 목록 정리가 완료 되었습니다. 다시 인증을 진행 해주세요!')
    