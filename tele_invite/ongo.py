from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    
    
    
    
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
        if profileStatus is not None or profileStatus != '인증XX':
            options = Options()
            user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
            service = Service(ChromeDriverManager().install())
            options.add_argument(f"user-data-dir={user_data}")
            options.add_argument(f'--profile-directory=Profile {profileNum}')
            driver = webdriver.Chrome(service=service, chrome_options=options)
            driver.get('https://web.telegram.org/z/')
            wait_float(2.5,3.2)
            
            pg.alert('대기~~~')
            
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
            
            hamBtnWrap = driver.find_element(by=By.CSS_SELECTOR, value='.translucent.round.has-ripple')
            pg.alert(hamBtnWrap)
            hamBtn = hamBtnWrap.find_element(by=By.CSS_SELECTOR, value='.ripple-container')
            hamBtn.click()
            pg.alert()
        
        
            
            
    
    
    
    # auth-qr-form
    
    
    
    sideBarMenu = searchElement('.menuitem',driver)
    for barMenu in sideBarMenu:
        if 'Contacts' in barMenu.text:
            barMenu.click()
    
    
    floatBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
    floatBtn.click()
    
    pg.alert('대기~~~')
    
    
    
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
    