from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    
    
    if getDict['nlist'] == 1:
        pg.alert('아이디가 선택되지 않았습니다. 다시 실행해주세요')
        sys.exit(0)
    
    
    exLineNum = getDict['nlist']
    wb = load_workbook('./etc/nid.xlsx')
    ex = wb.active
    
    
    preIp = ''
    
    if getDict['ipval'] == 1:
        while True:
            getIP = changeIp()
            print(getIP)
            if getIP == '119.197.60.174':
                pg.alert('집 아이피 입니다!')
                continue
            if not preIp == getIP:
                preIp = getIP
                break
    
    
    options = Options()
    user_data = 'C:\\Users\\pcy\\AppData\\Local\\Google\\Chrome\\User Data\\default'
    service = Service(ChromeDriverManager().install())
    options.add_argument(f"user-data-dir={user_data}")
    # if getDict['profileVal'] == 1:
    #     
    options.add_argument(f'--profile-directory={ex.cell(exLineNum, 3).value}')
    driver = webdriver.Chrome(service=service, chrome_options=options)
    
    driver.get('https://www.naver.com')
    
    
    # if getDict['profileVal'] == 0:
    #     pg.alert('프로필 체크 대기~~~')
    
    # chrome://version
    
    
    loginBtn = searchElement('.sc_login',driver)
    loginBtn[0].click()
    
    searchElement('#id',driver)
    focus_window('chrome')
    wait_float(0.3,0.9)
    while True:
        
        pg.click(200,500)
        inputId = driver.find_element(by=By.CSS_SELECTOR, value="#id")
        inputId.click()
        wait_float(0.3,0.9)
        cb.copy(ex.cell(exLineNum, 1).value)
        wait_float(0.3,0.9)
        pg.hotkey('ctrl', 'a')
        wait_float(0.3,0.9)
        pg.hotkey('ctrl', 'v')
        inputId = driver.find_element(by=By.CSS_SELECTOR, value="#id")
        if inputId.get_attribute('value') != "":
            break
        
    while True:
        inputPw = driver.find_element(by=By.CSS_SELECTOR, value="#pw")
        inputPw.click()
        wait_float(0.3,0.9)
        cb.copy(ex.cell(exLineNum, 2).value)
        wait_float(0.3,0.9)
        pg.hotkey('ctrl', 'a')
        wait_float(0.3,0.9)
        pg.hotkey('ctrl', 'v')
        inputPw = driver.find_element(by=By.CSS_SELECTOR, value="#pw")
        if inputPw.get_attribute('value') != "":
            break
    
    btnLogin = searchElement('.btn_login',driver)
    btnLogin[0].click()
    
    while True:
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#query")))
            break
        except:
            driver.get('https://www.naver.com')
            
    
    if getDict['middleVal'] == 1:
        chkVal = pg.confirm(text='댓글순방을 진행하겠습니까?', buttons=['go','stop'])
        if chkVal == 'go':
            allowListVisit(driver)
        else:
            pass
    else:
        if getDict['gonggamVal'] == 1:
            allowListVisit(driver)
        else:
            pass
        
    writeBlog(driver,getDict['middleVal'])
    
    if getDict['middleVal'] == 1:
        chkVal = pg.confirm(text='글쓰기가 완료 되었습니다!! 댓글을 진행 하시겠습니까?', buttons=['go','stop'])
    else:
        if getDict['cafeVal'] == 1:
            chkVal = 'go'
        else:
            chkVal = ''


    if chkVal == 'go':
        blogReplyWork(driver)
    else:
        pass
    
    pg.alert('종료합니다!!')
    sys.exit(0)