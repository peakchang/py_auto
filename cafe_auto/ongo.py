from func import *



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
    
    # dirList = os.listdir(f"{os.getcwd()}\\etc\\content\\id_{writeCount}")
    
    
    # global driver
    
    # chromeVersionChkPath = 'C:\\Users\\pcy\\AppData\\Local\\Google\\Chrome\\User Data\\default'
    chromeVersionChkPath = 'C:\\Users\\드림모어\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    
    

    cafe_optimize_file = load_workbook('./etc/naver_optimiz.xlsx')
    cafe_optimize = cafe_optimize_file.active
    cafe_id_file = load_workbook('./etc/naver_id.xlsx')
    cafe_id = cafe_id_file.active

    allCount = 0
    writeCount = 0
    endOptimize = ''
    nowAction = ''
    preIp = ''
    rereChkVal = ''
    rereActionChk = ''
    chk_extesion = ['jpg', 'jpeg', 'JPG', 'png', 'PNG', 'gif']

    with open('./etc/cafe_info.txt', 'r') as f:
        cafeAllInfo = f.readlines()

    for i in range(0, len(cafeAllInfo)):
        cafeAllInfo[i] = cafeAllInfo[i].replace('\n', '')

    print(cafeAllInfo)
    
    cafeName = cafeAllInfo[1]
    boardListKor = cafeAllInfo[2].split(',')
    boardListNum = cafeAllInfo[3].split(',')

    while True:
        allCount += 1
        
        if getDict['ipval'] == 1:
            while True:
                getIP = changeIpSpeed()
                print(getIP)
                if getIP == '119.197.60.174':
                    pg.alert('집 아이피 입니다!')
                    continue
                if not preIp == getIP:
                    preIp = getIP
                    break

        # 4로 나누어서 나머지가 1이면 글쓰기 아니면 댓글 (댓글은 6번 총 23~24 클릭)
        print('아이피 변경 완료')
        nowActionNum = allCount % 4
        
        if nowActionNum == 1:
            nowAction = 'write'
            writeCount += 1
        else:
            nowAction = 'reply'
            nowWriteStatus = ""
            
        # nowAction = 'reply'
        
        print(f'일단 현재 작업은? {nowAction}')

        if endOptimize == '' and nowAction == 'write':
            if os.path.exists(f'./etc/content/opt/id_{writeCount}'):
                optimizeChkVal1 = cafe_optimize.cell(writeCount, 2).value
                optimizeChkVal2 = cafe_optimize.cell(writeCount, 4).value
                if optimizeChkVal1 is None or optimizeChkVal2 is not None:
                    endOptimize = 'on'
                    nowWriteStatus = 'basic'
                else:
                    nowWriteStatus = 'optimize'
            else:
                endOptimize = 'on'
                nowWriteStatus = 'basic'
        else:
            nowWriteStatus = 'basic'

        print(f'최적화 여부는?? {nowWriteStatus}')

        # 최적화 글쓰기 / 일반 글쓰기 / 댓글쓰기 각 정보 (크롬정보 / 아이디 / 비번 / 게시판 번호 등) 부여하기
        if nowWriteStatus == 'optimize' and nowAction == 'write':
            # 최적화 아이디 일때
            uaSet = cafe_optimize.cell(writeCount, 1).value
            if uaSet is None:
                uaSet = getUaNum()
                cafe_optimize.cell(writeCount, 1).value = uaSet
                cafe_optimize_file.save('./etc/naver_optimiz.xlsx')

            nId = cafe_optimize.cell(writeCount, 2).value
            nPwd = cafe_optimize.cell(writeCount, 3).value
            nBoardName = cafe_optimize.cell(writeCount, 6).value
            nBoardNum = cafe_optimize.cell(writeCount, 7).value

            cafe_optimize.cell(writeCount, 4).value = datetime.now()
            cafe_optimize_file.save('./etc/naver_optimiz.xlsx')
            
        elif nowWriteStatus == 'basic' or nowAction == 'reply':
            # 일반 글쓰기 or 댓글 쓰기 일때 (안써진거 or 쓴지 3일 지난거)
            # 먼저 엑셀에서 사용한지 3일이 지난 값 가지고 오기
            
            # rereChkVal = 'https://m.cafe.naver.com/gnlcks33/25458'
            if rereChkVal != '':
                chkCount = 0
                rereChkValSplit = rereChkVal.split('/')

                lastRereSplit = rereChkValSplit[-1].strip()
                
                while True:
                    chkCount += 1
                    chkNone = cafe_id.cell(chkCount, 1).value
                    if chkNone is None:
                        break
                    chkVal = cafe_id.cell(chkCount, 5).value
                    if chkVal is not None:
                        if lastRereSplit in chkVal:
                            rereActionChk = 'on'
                            break
                    
            if rereActionChk == 'on':
                uaSet = cafe_id.cell(chkCount, 1).value
                nId = cafe_id.cell(chkCount, 2).value
                nPwd = cafe_id.cell(chkCount, 3).value
                boardGetRan = random.randrange(0, 2)
                nBoardName = boardListKor[boardGetRan]
                
                cafe_id.cell(chkCount, 5).value = ''
                cafe_id_file.save('./etc/naver_id.xlsx')
                rereActionChk = ''
                
            else:
                rereActionChk = ''
                nidExLength = getExLength(cafe_id)
                chkArr = asyncio.run(getEmptyArr(nidExLength, cafe_id))
                getRanVal = random.randrange(0, len(chkArr))
                getRanWorkVal = chkArr[getRanVal]

                uaSet = cafe_id.cell(getRanWorkVal, 1).value
                if uaSet is None:
                    uaSet = getUaNum()
                    cafe_id.cell(getRanWorkVal, 1).value = uaSet
                    cafe_id_file.save('./etc/naver_id.xlsx')

                nId = cafe_id.cell(getRanWorkVal, 2).value
                nPwd = cafe_id.cell(getRanWorkVal, 3).value
                boardGetRan = random.randrange(0, 2)
                nBoardName = boardListKor[boardGetRan]
                nBoardNum = boardListNum[boardGetRan]
                
                cafe_id.cell(getRanWorkVal, 4).value = datetime.now()
                cafe_id_file.save('./etc/naver_id.xlsx')
                
        # 테스트겸 냅두자
        try:
            getVal = getRanWorkVal
        except:
            getVal = writeCount
            
        # pg.alert(text=f'{getVal}번째 있는 아이디로 {nowWriteStatus} {nowAction}작업, 크롬 정보 : {uaSet} / 아이디 : {nId} / 비번 : {nPwd} / 게시판 이름 {nBoardName}')
        print(f'{getVal}번째 있는 아이디로 {nowWriteStatus} {nowAction}작업, 크롬 정보 : {uaSet} / 아이디 : {nId} / 비번 : {nPwd} / 게시판 이름 {nBoardName}')

        print('정보 얻기 완료')

        if nowAction == 'write' and nowWriteStatus == 'basic':
            
            # 블로그 글따기 시작!!!
            # 엑셀로 랜덤 돌려서 제목 뽑기
            getSubjectRanVal = random.randrange(0,3)
            if getSubjectRanVal != 0:
                # 글 제목 따기!!
                options = Options()
                service = Service(ChromeDriverManager().install())
                options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1')
                driver = webdriver.Chrome(service=service, chrome_options=options)
                
                subjecArr = getSubjectArrToCafe(driver)
                
            if getSubjectRanVal == 0 or subjecArr == [] or subjecArr == '' or subjecArr is None:
                # 엑셀로 랜덤 돌려서 제목 뽑기
                cafe_ex_file = load_workbook('./etc/subject_list.xlsx')
                cafe_ex = cafe_ex_file.active
                subjectCountArr = []
                for i in range(1, 5):
                    k = 0
                    while True:
                        k += 1
                        chkVal = cafe_ex.cell(k, i).value
                        if chkVal is None:
                            subjectCountArr.append(k)
                            break

                subjecArr = []
                for i, subjectCount in enumerate(subjectCountArr):
                    if i == 1 or i == 2:
                        passNum = random.randrange(1, 3)
                        if passNum != 1:
                            continue
                    getConNum = random.randrange(1, subjectCount)
                    chkVal = cafe_ex.cell(getConNum, i+1).value
                    subjecArr.append(chkVal)
                    
                print('제목 생성 완료')
                # 엑셀로 랜덤 돌려서 제목 뽑기 끝 이제 아래 블로그 컨텐츠 생성 함수에 넣고 막글 뽑자!
            
            
            #블로그 글따기 실패시 (보안문자 뜨면 반복)
            while True:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)
                print('일반 - 블로그 글따기 시작~')
                blog_content = getBlogContentChrome(subjecArr,driver)
                if blog_content != 'error':
                    break                    
            print('블로그 글 따기 완료')
            subject = " ".join(subjecArr)
            with open("./etc/content/write_content.txt", "w") as f:
                f.write(subject)
                f.write('\n')
                f.write(blog_content)
            # 블로그 글따기 끝!!

            # 네이버 메인에서 카페 진입 시작!
            with open(f'./etc/useragent/useragent_all.txt') as f:
                ua_data = f.readlines()[uaSet]
                ua_data = ua_data.replace('\n', '')
            
            options = Options()
            user_agent = ua_data
            options.add_argument('user-agent=' + user_agent)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(chrome_options=options, service=service)

            driver.get('https://www.naver.com')

            errchk = naverLogin_mobile(nId, nPwd, driver)
            if errchk is not None:
                cafe_id.cell(getRanWorkVal, 4).value = errchk
                cafe_id_file.save('./etc/naver_id.xlsx')

                allCount = allCount - 1
                driver.close()
                continue
            
            driver.get(cafeName)
            
            cafe_join_btn(driver)
            getAddRemoveLinks = ''
            getAddRemoveLinks = cafe_write_mobile(nBoardName,chk_extesion,driver)
            
            if getAddRemoveLinks != '' or getAddRemoveLinks is not None:
                cafe_id.cell(getRanWorkVal, 5).value = getAddRemoveLinks[0]
                cafe_id_file.save('./etc/naver_id.xlsx')
                rereChkVal = getAddRemoveLinks[1]
                cafe_reply_mobile(driver)
            
            
            
            
            
            
            nowWriteStatus = ''


        if nowAction == 'write' and nowWriteStatus == 'optimize':
            options = Options()
            user_data = chromeVersionChkPath
            service = Service(ChromeDriverManager().install())
            options.add_argument(f"user-data-dir={user_data}")
            options.add_argument(f'--profile-directory={uaSet}')
            driver = webdriver.Chrome(service=service, chrome_options=options)
            driver.set_window_size(1180, 910)
            driver.set_window_position(0,0) 
            
            
            driver.get('https://www.naver.com')
            
            naverLogin_pc(nId,nPwd,driver)
            
            cafe_re_reply_pc(cafeAllInfo,driver)
            cafe_write_pc(cafeAllInfo,writeCount,driver)
            nowWriteStatus = ''
            rereChkVal = ''
            
            
            
            
            
            
            
            
            
        # ★★★★★★★★ 댓글 작성 시작!!
        if nowAction == 'reply':
            with open(f'./etc/useragent/useragent_all.txt') as f:
                ua_data = f.readlines()[uaSet]
            options = Options()
            user_agent = ua_data
            options.add_argument('user-agent=' + user_agent)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(chrome_options=options, service=service)
            driver.get('https://www.naver.com')
            
            errchk = naverLogin_mobile(nId, nPwd, driver)
            if errchk is not None:
                if nowWriteStatus == 'basic':
                    cafe_id.cell(getRanWorkVal, 4).value = errchk
                    cafe_id_file.save('./etc/naver_id.xlsx')
                elif nowWriteStatus == 'optimize':
                    cafe_optimize.cell(writeCount, 4).value = errchk
                    cafe_optimize_file.save('./etc/naver_optimiz.xlsx')
                allCount = allCount - 1
                driver.close()
                continue
            
            driver.get(cafeName)
            cafe_join_btn(driver)
            
            if rereChkVal != '':
                cafe_re_reply_mobile(driver,cafeName)
            
            driver.get(cafeName)
            cafe_reply_mobile(driver)
            # 카페 메인 진입 끝! 게시글 클릭 시작!
            nowWriteStatus = ''
            rereChkVal = ''
        

        driver.quit()


