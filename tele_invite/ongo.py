from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    
    pg.alert('작업을 시작합니다!')
    
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList.active
    
    dbList = load_workbook('./db_list.xlsx')
    dbSheet = dbList.active
    chkInnerUserText = ['전까지','어제','일주일','최근','오늘']
        
    noMoreDb = ''
    while True:
        authCount = 1
        while True:
            authCount += 1
            authChk = authSheet.cell(authCount, 6).value
            if authChk is None:
                break
        
        endChk = authSheet.cell(authCount, 1).value
        if endChk is None:
            pg.alert('작업이 완료 되었습니다.')
            break
        elif noMoreDb == 'on':
            pg.alert('DB가 소진 되었습니다. 작업을 종료합니다')
            break
        
        today = datetime.today()
        todayStr = today.strftime("%y/%m/%d")
        authSheet.cell(authCount, 6).value = f"{todayStr} 작업 완료"
        authList.save('./auth_list.xlsx')
        profileNum = authSheet.cell(authCount,1).value
        workType = authSheet.cell(authCount,5).value
        if profileNum is None:
            break
        
        profileStatus = authSheet.cell(authCount,3).value
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
            driver.set_window_size(1600, 800)
            driver.set_window_position(0,0)
            
            fore = pg.getActiveWindow()
            print(fore.title)   # 활성화된 창의 제목 정보
            print(fore.size)    # 활성화된 창의 사이즈
            print(fore.left, fore.top, fore.right, fore.bottom) # 좌표정보
            
            wait_float(2.5,3.2)
            
            # 아이디가 짤렸는지 안짤렸는디 최초 검증!!
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
            
            # 만약 현재 영어 버전일경우 한글 버전으로 변경!!
            
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
                        if "Language" in item.text:
                            item.click()
                    wait_float(0.5,0.9)
                    listRadio = searchWaitElement('.settings-language .Radio', driver)
                    listRadio[0].click()
                
                    goToMain(driver, fore)
                    wait_float(1.5,2.5)
            
            
            if getDict['add_addr_val']:
                # DB 카운트 ID값 미 기재된 라인 count 찾기!!
                dbCount = 0
                while True:
                    dbCount += 1
                    dbId = dbSheet.cell(dbCount,1).value
                    if dbId is None:
                        break
                # 준비 완료!! 사람 추가 반복하자!!
                for i in range(9):
                    goToMain(driver, fore)
                    notMb = ''
                    finChk = ''
                    dbLine = dbCount + i
                    getPhNum = dbSheet.cell(dbLine,4).value
                    if getPhNum is None:
                        noMoreDb = 'on'
                        break
                    
                    getPhNum = re.sub(r'[^0-9]', '', getPhNum)
                    if getPhNum[0:1] != '0':
                        getPhNum = f"0{getPhNum}"
                    addPhAddr = f"+82{getPhNum[1:]}"
                    
                    dbSheet.cell(dbLine,1).value = profileNum
                    dbList.save('./db_list.xlsx')
                    
                    # 연락처 추가하기! 모달창 키고 번호 입력!
                    while True:
                        print('연락처 추가하기! 모달창 키고 번호 입력!')
                        focus_window('Telegram')
                        wait_float(1.2,1.9)
                        
                        try:
                            wait_float(0.9,1.5)
                            menuList = showTeleMenu(driver)
                            menuList[2].click()
                        except:
                            wait_float(0.5,1.2)
                            pg.click(fore.left+500,fore.top+300)
                            wait_float(0.5,1.2)
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
                            break
                        except:
                            continue
                    
                    #친추 완료! 모달창 떠있으면 가입한 회원 아님 / 안떠있으면 체크!
                    while True:
                        wait_float(2.7,3.5)
                        print('친추 완료! 모달창 떠있으면 가입한 회원 아님 / 안떠있으면 체크!')
                        try:
                            notMb = driver.find_element(by=By.CSS_SELECTOR, value='.NewContactModal__new-contact')
                            if notMb:
                                break
                        except:
                            pass
                        
                        try:
                            findMb = driver.find_element(by=By.CSS_SELECTOR, value='.MiddleHeader')
                            if findMb:
                                break
                        except:
                            pass
                        
                    if notMb:
                        wait_float(1.2,1.9)
                        dbSheet.cell(dbLine,5).value = 'V'
                        dbList.save('./db_list.xlsx')
                        pg.click(fore.left+500,fore.top+300)
                        continue
                    
                    
                    refreshCount = 0
                    while True:
                        refreshCount += 1
                        wait_float(1.2,1.9)
                        if refreshCount == 3:
                            refreshCount = 0
                            pg.press('F5')
                        userStatus = searchWaitElement('.MiddleHeader .user-status', driver)
                        userStatusText = re.sub(r'[\s]', '', userStatus[0].text)
                        if userStatusText:
                            break
                    
                    for chkText in chkInnerUserText:
                        if chkText in userStatusText:
                            wait_float(1.2,1.9)
                            dbSheet.cell(dbLine,7).value = 'V'
                            dbList.save('./db_list.xlsx')
                            finChk = 'ok'
                            continue
                    
                    if finChk == '':
                        wait_float(1.2,1.9)
                        chkCompare = compareDate(userStatusText)
                        if chkCompare:
                            dbSheet.cell(dbLine,7).value = 'V'
                            dbList.save('./db_list.xlsx')
                        else:
                            
                            dbSheet.cell(dbLine,6).value = 'V'
                            dbList.save('./db_list.xlsx')
                            
                            # 연락처 삭제 준비, 삭제 아이콘 나오게
                            while True:
                                print("연락처 삭제 준비, 삭제 아이콘 나오게")
                                wait_float(0.5,0.9)
                                try:
                                    # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon-delete')))
                                    delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.icon-delete')
                                    if delIcon:
                                        break
                                except:
                                    pass
                                
                                try:
                                    # tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                                    tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                                    tools.click()
                                except:
                                    pass
                                
                                try:
                                    # openInfo = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.MiddleHeader .fullName')))
                                    openInfo = driver.find_element(by=By.CSS_SELECTOR, value='.MiddleHeader .fullName')
                                    openInfo.click()
                                except:
                                    pass
                            
                            # 연락처 삭제 모달창 띄우기
                            while True:
                                print("연락처 삭제 모달창 띄우기")
                                wait_float(0.5,0.9)
                                try:
                                    # modal = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal')))
                                    modal = driver.find_element(by=By.CSS_SELECTOR, value='.Modal')
                                    if modal:
                                        break
                                except:
                                    pass
                                
                                try:
                                    # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.destructive')))
                                    delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.destructive')
                                    delIcon.click()
                                except:
                                    pass
                                
                            # 연락처 삭제 완료
                            while True:
                                print("연락처 삭제 완료")
                                wait_float(0.5,0.9)
                                try:
                                    # manageText = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RightHeader .Transition__slide--active')))
                                    manageText = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
                                    if manageText.text == '회원 정보':
                                        break
                                except:
                                    pass
                                
                                try:
                                    # delManageBtn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal .confirm-dialog-button.default.danger.text')))
                                    delManageBtn = driver.find_element(by=By.CSS_SELECTOR, value='.Modal .confirm-dialog-button.default.danger.text')
                                    delManageBtn.click()
                                except:
                                    pass
                                
                            
            ################## 아이디 추가 작업 끝 그룹에 추가 시작!!
            
            if getDict['join_group_val']:
                getChatRoomName = authSheet.cell(authCount,4).value.strip()
                saveGroupType = ""
                
                # 그룹 유형 체크 (최초 1회만)
                
                    
                if workType == '관리자추가':
                    while True:
                        # 그룹 클릭 (그룹명 찾아서 클릭 / 채팅방 클릭)
                        while True:
                            print("그룹 클릭 (그룹명 찾아서 클릭 / 채팅방 클릭)")
                            try:
                                nowChatRoom = driver.find_element(by=By.CSS_SELECTOR, value='.MiddleHeader .ChatInfo .fullName')
                                if getChatRoomName in nowChatRoom.text:
                                    break
                            except:
                                pass
                            
                            try:
                                wait_float(0.9,1.2)
                                chatList = searchWaitElement('.chat-list .ListItem', driver)
                                for chatRoom in chatList:
                                    wait_float(0.2,0.5)
                                    if getChatRoomName in chatRoom.text:
                                        wait_float(0.5,0.9)
                                        chatRoom.click()
                                        break
                            except:
                                pass
                        wait_float(0.5,0.9)
                        
                        # 상단 그룹이름 클릭(우측 그룹 정보 나올때까지)
                        while True:
                            print('그룹 관리 열기')
                            try:
                                wait_float(0.9,1.2)
                                # ChatInfo = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.chat-info-wrapper .ChatInfo')))
                                ChatInfo = driver.find_element(by=By.CSS_SELECTOR, value='.chat-info-wrapper .ChatInfo')
                                ChatInfo.click()
                                
                            except:
                                pass
                            
                            try:
                                wait_float(0.9,1.2)
                                # ProfilePhoto = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ProfilePhoto')))
                                ProfilePhoto = driver.find_element(by=By.CSS_SELECTOR, value='.ProfilePhoto')
                                
                                if ProfilePhoto:
                                    break
                            except:
                                pg.press('F5')
                                pass
                            
                        # 그룹 정보 우상단 연필 클릭
                        while True:
                            print('그룹 툴 열기')
                            try:
                                wait_float(0.9,1.2)
                                tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                                # tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                                tools.click()
                            except:
                                pass
                            
                            try:
                                wait_float(0.9,1.2)
                                AvatarEditable = driver.find_element(by=By.CSS_SELECTOR, value='.AvatarEditable')
                                # AvatarEditable = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.AvatarEditable')))
                                if AvatarEditable:
                                    break
                            except:
                                pass

                        wait_float(0.5,0.9)
                        
                        groupMenu = searchWaitElement('.Management .ListItem', driver)
                        # 그룹 > 수정 > 관리자 클릭
                        while True:
                            
                            print("그룹 > 수정 > 관리자 클릭")
                            
                            try:
                                wait_float(0.9,1.2)
                                tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                                # tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                                tools.click()
                            except:
                                pass
                            
                            try:
                                wait_float(0.9,1.2)
                                groupMenu = searchWaitElement('.Management .ListItem', driver)
                                for menu in groupMenu:
                                    if "관리자" in menu.text:
                                        menu.click()
                                        
                                wait_float(0.9,1.2)
                                managerAddBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
                                managerAddBtnText = managerAddBtn.get_attribute('title')
                                if "추가" in managerAddBtnText:
                                    managerAddBtn.click()
                                    break
                            except:
                                pass
                        
                        
                        
                        # 관리자 추가 > 010 검색 > 010 번호 가진사람 클릭
                        while True:
                            wait_float(0.5,0.9)
                            print("관리자 추가 > 010 검색 > 010 번호 가진사람 클릭")
                            findUser = ''
                            try:
                                wait_float(0.5,0.9)
                                searchAddMgInput = searchWaitElement('.Management__filter .form-control', driver)
                                getVal = searchAddMgInput[0].get_attribute('value')
                                if getVal:
                                    pass
                                else:
                                    searchAddMgInput[0].send_keys("010")
                                
                                wait_float(2.1,2.9)
                                searchUserNameList = driver.find_elements(by=By.CSS_SELECTOR, value='.Management .picker-list .ListItem .ChatInfo .fullName')
                                for userName in searchUserNameList:
                                    if userName.text[0:3] == '010' or userName.text[0:2] == '10':
                                        userName.click()
                                        setUserName = re.sub(r'[^0-9]', '', userName.text)
                                        findUser = 'on'
                                        break
                                # pg.alert(findUser)
                                wait_float(0.5,0.9)
                                
                                if findUser == 'on' and setUserName:
                                    menegerOkBtn = searchWaitElement('.Management .FloatingActionButton', driver)
                                    if menegerOkBtn[0]:
                                        break
                                elif findUser == '':
                                    break
                            except:
                                pass
                            
                            try:
                                nothingFound = driver.find_element(by=By.CSS_SELECTOR, value='.Management .NothingFound')
                                if nothingFound:
                                    findUser = ''
                                    break
                            except:
                                pass
                                 
                            
                        if findUser == '':
                            print('더이상 찾을 회원이 없음')
                            break
                            
                            
                        
                        # 추가된 사람 관리자 승격
                        while True:
                            print("추가된 사람 관리자 승격")
                            wait_float(0.5,0.9)
                            try:
                                # manageText = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RightHeader .Transition__slide--active')))
                                manageText = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
                                if manageText.text == '관리자':
                                    break
                            except:
                                pass
                            
                            try:
                                # menegerOkBtn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Management .FloatingActionButton')))
                                menegerOkBtn = driver.find_element(by=By.CSS_SELECTOR, value='.Management .FloatingActionButton')
                                menegerOkBtn.click()
                                wait_float(1.5,2.5)
                            except:
                                pass
                        
                        # 관리자 승격된 사람 클릭 관리자 권한 삭제 준비
                        while True:
                            print("관리자 승격된 사람 클릭 관리자 권한 삭제 준비")
                            wait_float(0.5,0.9)
                            try:
                                # driver.find_element(by=By.CSS_SELECTOR, value='.destructive')
                                # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon-delete')))
                                delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.destructive')
                                if delIcon:
                                    break
                            except:
                                pass
                            
                            try:
                                managerList = searchWaitElement('.Management .ListItem .fullName', driver)
                                for manager in managerList:
                                    getManagerName = re.sub(r'[^0-9]', '', manager.text)
                                    if getManagerName == setUserName:
                                        manager.click()
                            except:
                                pass
                            
                        # 관리자 권한 삭제 모달창 띄우기
                        while True:
                            print("관리자 권한 삭제 모달창 띄우기")
                            wait_float(0.5,0.9)
                            try:
                                # modal = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal')))
                                modal = driver.find_element(by=By.CSS_SELECTOR, value='.Modal')
                                if modal:
                                    break
                            except:
                                pass
                            
                            try:
                                # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.destructive')))
                                delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.destructive')
                                delIcon.click()
                            except:
                                pass
                            # icon-delete
                        
                        
                        # 모달창에서 관리자 권한 삭제 완료
                        while True:
                            print("모달창에서 관리자 권한 삭제 완료")
                            wait_float(0.5,0.9)
                            try:
                                # manageText = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RightHeader .Transition__slide--active')))
                                manageText = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
                                if manageText.text == '관리자':
                                    break
                            except:
                                pass
                            
                            try:
                                # delManageBtn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal .confirm-dialog-button.default.danger.text')))
                                delManageBtn = driver.find_element(by=By.CSS_SELECTOR, value='.Modal .confirm-dialog-button.default.danger.text')
                                delManageBtn.click()
                            except:
                                pass
                            
                            
                            
                        # 그룹 설정 메인 갈때까지 뒤로가기 클릭
                        while True:
                            print("그룹 설정 메인 갈때까지 뒤로가기 클릭")
                            wait_float(0.5,0.9)
                            try:
                                closeBtn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.close-button')))
                                getBtnText = closeBtn.get_attribute('title')
                                if getBtnText == '닫기':
                                    memberList = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content.members-list')))
                                    if memberList:
                                        break
                                else:
                                    closeBtn.click()
                            except:
                                pass
                        
                        # 연락처 삭제 준비, 회원 클릭 (헤더에 "회원" 이라고 나타나게)
                        while True:
                            print("연락처 삭제 준비, 회원 클릭 (헤더에 회원 이라고 나타나게)")
                            wait_float(0.5,0.9)
                            try:
                                # userInfo = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RightHeader .Transition__slide--active')))
                                userInfo = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
                                if '회원' in userInfo.text:
                                    break
                            except:
                                pass
                            
                            try:
                                memberList = searchWaitElement('.content.members-list .ListItem .fullName', driver)
                                for mamber in memberList:
                                    getmemberName = re.sub(r'[^0-9]', '', mamber.text)
                                    if getmemberName == setUserName:
                                        mamber.click()
                            except:
                                pass
                        
                        # 연락처 삭제 준비, 삭제 아이콘 나오게
                        while True:
                            print("연락처 삭제 준비, 삭제 아이콘 나오게")
                            wait_float(0.5,0.9)
                            try:
                                # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon-delete')))
                                delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.icon-delete')
                                if delIcon:
                                    break
                            except:
                                pass
                            
                            try:
                                # tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                                tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                                tools.click()
                            except:
                                pass
                        
                        # 연락처 삭제 모달창 띄우기
                        while True:
                            print("연락처 삭제 모달창 띄우기")
                            wait_float(0.5,0.9)
                            try:
                                # modal = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal')))
                                modal = driver.find_element(by=By.CSS_SELECTOR, value='.Modal')
                                if modal:
                                    break
                            except:
                                pass
                            
                            try:
                                # delIcon = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.destructive')))
                                delIcon = driver.find_element(by=By.CSS_SELECTOR, value='.destructive')
                                delIcon.click()
                            except:
                                pass
                            
                        # 연락처 삭제 완료
                        while True:
                            print("연락처 삭제 완료")
                            wait_float(0.5,0.9)
                            try:
                                # manageText = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RightHeader .Transition__slide--active')))
                                manageText = driver.find_element(by=By.CSS_SELECTOR, value='.RightHeader .Transition__slide--active')
                                if manageText.text == '회원 정보':
                                    break
                            except:
                                pass
                            
                            try:
                                # delManageBtn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Modal .confirm-dialog-button.default.danger.text')))
                                delManageBtn = driver.find_element(by=By.CSS_SELECTOR, value='.Modal .confirm-dialog-button.default.danger.text')
                                delManageBtn.click()
                            except:
                                pass
                        
                        
                        # 엑셀에 삭제된 연락처 진짜 이름 추가                        
                        reCount = 0
                        realUserWork = ''
                        chkDb = ''
                        while True:
                            reCount += 1
                            wait_float(0.5,1.2)
                            if reCount > 3:
                                reCount = 0
                                pg.press('F5')
                                wait_float(0.5,1.2)
                            
                            getRealNameArea = searchWaitElement('.MiddleHeader .info .fullName', driver)
                            wait_float(0.3,0.9)
                            for getRealName in getRealNameArea:
                                if getRealName.text:
                                    getReal = re.sub(r'[^\uAC00-\uD7A30-9a-zA-Z\s]', '', getRealName.text)
                                    if getReal == setUserName or getReal == '':
                                        continue
                                    else:
                                        chkDbCount = 0
                                        while True:
                                            chkDbCount += 1
                                            if dbSheet.cell(chkDbCount,4).value is not None:
                                                chkDb = re.sub(r'[^0-9]', '', dbSheet.cell(chkDbCount,4).value)
                                            if chkDb == setUserName:
                                                break
                                        wait_float(0.3,0.9)
                                        dbSheet.cell(chkDbCount,2).value = getReal
                                        dbList.save('./db_list.xlsx')
                                        realUserWork = 'on'
                            
                            if realUserWork == 'on':
                                break
                else:
                    pg.alert('관리자 추가 말고 딴거!!!')
                
                    
            wait_float(0.5,1.2)
            driver.quit()
            wait_float(0.5,1.2)
                    
                
                
                
            
            # RightColumn
    sys.exit(0)
            
            
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
def authListChk():
    
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList.active
    
    authCount = 1
    while True:
        authCount += 1
        profileNum = authSheet.cell(authCount,1).value
        if profileNum is None:
            pg.alert('완료되었습니다!!')
            break
        
        profileStatus = authSheet.cell(authCount,3).value
        if profileStatus is None or "X" in profileStatus:
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
    
    
    
    
    
    
    
    
    
    
    

def inviteManager():
    
    pcUser = getpass.getuser()
    authList = load_workbook('./auth_list.xlsx')
    authSheet = authList.active
    
    authCount = 0
    while True:
        authCount += 1
        searchMaster = authSheet.cell(authCount, 2).value
        if "마스터" in searchMaster:
            break
    
    
    getMasterProfile = authSheet.cell(authCount, 1).value
    
    
    while True:
        authCount += 1
        if authSheet.cell(authCount, 6).value is None:
            authCount = authCount - 1
            break
        
    while True:
        authCount += 1
        getManagerNum = authSheet.cell(authCount, 2).value
        getChatRoomName = authSheet.cell(authCount, 4).value
        if getManagerNum is None:
            pg.alert('전부 추가 완료 되었습니다.')
            break
        getManagerPhNumSplit = getManagerNum.split('/')[0].split(' ')
        getManagerNationNum = getManagerPhNumSplit[0]
        getManagerPhNum = ''.join(getManagerPhNumSplit[1:])
        
        options = Options()
        user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
        service = Service(ChromeDriverManager().install())
        options.add_argument(f"user-data-dir={user_data}")
        options.add_argument(f'--profile-directory=Profile {getMasterProfile}')
        driver = webdriver.Chrome(service=service, chrome_options=options)
        driver.get('https://web.telegram.org/z/')
        driver.set_window_size(1600, 800)
        driver.set_window_position(0,0)
        fore = pg.getActiveWindow()
        
        
        wait_float(1.2,1.9)
        # 만약 현재 영어 버전일경우 한글 버전으로 변경!!
        menuList = showTeleMenu(driver)
        if '메시지' not in menuList[0].text:
            menuList[3].click()
            wait_float(0.5,0.9)
            listItem = searchWaitElement('.settings-main-menu .ListItem', driver)
            listItem[7].click()
            wait_float(0.5,0.9)
            listRadio = searchWaitElement('.settings-language .Radio', driver)
            listRadio[0].click()
            goToMain(driver, fore)
            wait_float(1.5,2.5)
        else:
            pg.press('F5')
            pass
        
        
        
        print('연락처 추가하기! 모달창 키고 번호 입력!')
        focus_window('Telegram')
        wait_float(1.2,1.9)
        
        try:
            wait_float(0.9,1.2)
            menuList = showTeleMenu(driver)
            menuList[2].click()
        except:
            pass
        
        try:
            wait_float(0.9,1.2)
            addAddressBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
            addAddressBtn.click()
        except:
            pg.click(fore.left+500,fore.top+300)
            authCount = authCount - 1
            wait_float(0.9,1.2)
            continue
        
        try:
            wait_float(0.9,1.2)
            inputList = driver.find_elements(by=By.CSS_SELECTOR, value='.NewContactModal__new-contact-fieldset .form-control')
            inputList[0].click()
            inputList[0].send_keys(getManagerNationNum + getManagerPhNum)
            wait_float(0.9,1.2)
            inputList[1].send_keys(getManagerPhNum)
            okBtn = driver.find_elements(by=By.CSS_SELECTOR, value='.confirm-dialog-button')
            okBtn[1].click()
            wait_float(0.5,0.9)
        except:
            continue
        
        
        goToMain(driver, fore)

        # 그룹 클릭 (그룹명 찾아서 클릭 / 채팅방 클릭)
        while True:
            print("그룹 클릭 (그룹명 찾아서 클릭 / 채팅방 클릭)")
            try:
                nowChatRoom = driver.find_element(by=By.CSS_SELECTOR, value='.MiddleHeader .ChatInfo .fullName')
                if getChatRoomName in nowChatRoom.text:
                    break
            except:
                pass
            
            try:
                wait_float(0.9,1.2)
                chatList = searchWaitElement('.chat-list .ListItem', driver)
                for chatRoom in chatList:
                    wait_float(0.2,0.5)
                    if getChatRoomName in chatRoom.text:
                        wait_float(0.5,0.9)
                        chatRoom.click()
                        break
            except:
                pass

        # 상단 그룹이름 클릭(우측 그룹 정보 나올때까지)
        while True:
            print('그룹 관리 열기')
            try:
                wait_float(0.9,1.2)
                # ChatInfo = driver.find_element(by=By.CSS_SELECTOR, value='.chat-info-wrapper .ChatInfo')
                ChatInfo = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.chat-info-wrapper .ChatInfo')))
                ChatInfo.click()
                
            except:
                pass
            
            try:
                wait_float(0.9,1.2)
                # ProfilePhoto = driver.find_element(by=By.CSS_SELECTOR, value='.ProfilePhoto')
                ProfilePhoto = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ProfilePhoto')))
                if ProfilePhoto:
                    break
            except:
                pass
        
        # 그룹 정보 우상단 연필 클릭
        while True:
            print('그룹 툴 열기')
            try:
                wait_float(0.9,1.2)
                # tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                tools.click()
            except:
                pass
            
            try:
                wait_float(0.9,1.2)
                # AvatarEditable = driver.find_element(by=By.CSS_SELECTOR, value='.AvatarEditable')
                AvatarEditable = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.AvatarEditable')))
                if AvatarEditable:
                    break
            except:
                pass
        

        wait_float(0.5,0.9)
        
        groupMenu = searchWaitElement('.Management .ListItem', driver)
        # 그룹 > 수정 > 관리자 클릭
        while True:
            print("그룹 > 수정 > 관리자 클릭")
            
            try:
                wait_float(0.9,1.2)
                # tools = driver.find_element(by=By.CSS_SELECTOR, value='.tools')
                tools = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tools')))
                tools.click()
            except:
                pass
            
            try:
                wait_float(0.9,1.2)
                groupMenu = searchWaitElement('.Management .ListItem', driver)
                for menu in groupMenu:
                    if "관리자" in menu.text:
                        menu.click()
                        
                wait_float(0.9,1.2)
                managerAddBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
                managerAddBtnText = managerAddBtn.get_attribute('title')
                if "추가" in managerAddBtnText:
                    managerAddBtn.click()
                    break
            except:
                pass
        
        
        while True:
            wait_float(0.5,0.9)
            print("관리자 추가 > 010 검색 > 010 번호 가진사람 클릭")
            findUser = ''
            try:
                wait_float(0.5,0.9)
                searchAddMgInput = searchWaitElement('.Management__filter .form-control', driver)
                getVal = searchAddMgInput[0].get_attribute('value')
                if getVal:
                    pass
                else:
                    searchAddMgInput[0].send_keys("010")
                    
                wait_float(2.1,2.9)
                searchUserNameList = driver.find_elements(by=By.CSS_SELECTOR, value='.Management .picker-list .ListItem .ChatInfo .fullName')
                for userName in searchUserNameList:
                    if userName.text == getManagerPhNum:
                        userName.click()
            except:
                pass
            
            try:
                wait_float(0.9,1.2)
                menegerOkBtn = searchWaitElement('.Management .FloatingActionButton', driver)
                menegerOkBtn[0].click()
                authSheet.cell(authCount, 6).value = '관리자 추가 완료'
                authList.save('./auth_list.xlsx')
                break
            except:
                pass
                
        wait_float(1.9,2.8)
        driver.quit()
        wait_float(0.5,0.9)
        
        
        
    sys.exit(0)