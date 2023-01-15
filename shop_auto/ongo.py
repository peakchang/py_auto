from func import *


def goScript(getDict):
    
    global driver
    preIp = ""
    
    # 전체 반복 시작 전 지쇼 링크 열고 전체 행 갯수 체크
    jisho_wb = openpyxl.load_workbook('./etc/jisho_link.xlsx')
    link_excel = jisho_wb.active

    while True:
        startTime = time.time()
        # 아이피 체크 (기존 아이피와 같으면 다시, 아니면 break)
        if getDict['ipval'] == 1:
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            while True:
                getIP = changeIpSpeed(driver)
                print(getIP)
                if not preIp == getIP:
                    preIp = getIP
                    break
        
        # 작업할 배열 순서 정하기
        exCount = 1
        while True:
            if link_excel.cell(exCount, 1).value is None:
                break
            exCount += 1
        pg.alert(exCount)
        workArr = list(range(1,exCount))
        random.shuffle(workArr)
        pg.alert(workArr)
        
        
        
        # 설정 끝~ 접속하기
        ua_data = linecache.getline('./etc/useragent/useragent_all.txt', random.randrange(1, 14)).strip()
        options = Options()
        user_agent = ua_data
        options.add_argument('user-agent=' + user_agent)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(chrome_options=options, service=service)

        driver.get('https://www.naver.com')

        time.sleep(2)
        focus_window('NAVER')
        
        
        mainToJisho(driver)
        
        pg.alert('대기대기대기요~~~')

        for workVal in workArr:
            
            print('에러 예상 111111')
            searchKeyword = link_excel.cell(workVal, 2).value
            
            #검색기록 삭제 만들기!!!!!! .recentHistory_list_word__EJZeH // .recentHistory_btn_del__greg5
            searchJisho(searchKeyword, driver)
            
            print('에러 예상 222222')
            nShopCategory = searchElement(".mainFilter_option__c4_Lq", driver)
            
            try:
                UseLessBtn = driver.find_element(by=By.CSS_SELECTOR, value='.basicFilter_btn_close__qftDk svg')
                UseLessBtn.click()
            except:
                pass
            setTong = link_excel.cell(workVal, 1).value
            if setTong is not None:
                chkin_tong = ""
                for category in nShopCategory:
                    category_name = category.text.replace('+', '')
                    if category_name[0:2] == setTong:
                        chkin_tong = "on"
                        print('여기서 나는 에러가 맞는걸까요?????')
                        # untilEleShow(category, ".selected_btn_del__0mIMB")
                        untilEleShow(category, ".mainFilter_option__c4_Lq",driver)

                if chkin_tong == "":
                    addKeyword = link_excel.cell(workVal, 1).value
                    if addKeyword == "SK":
                        addKeyword = "SKT"
                    searchRan = random.randrange(0, 2)
                    if searchRan == 0:
                        searchKeyword = searchKeyword + " " + addKeyword
                    else:
                        searchKeyword = addKeyword + " " + searchKeyword
                    searchJisho(searchKeyword, driver)
            print('에러 예상 444444')
                    
            # 상위 4개 중 1개 클릭
            
            # 여기서 6개까지 찾고 / 그중에 있으면 그냥 한번만, 없으면 원래대로
            
            
            pg.alert('여기까지는 어디까지지?? 검색 마무리 같은디?!?!?')
            highWork = ""
            item_list = driver.find_elements("xpath", "//*[contains(@class, 'product_list_item')]")
            print('상위 작업 체크 시작!!')
            chkCount = 0
            for highCount in range(6):
                chkCount += 1
                getHighHref = item_list[highCount].find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href')
                searchMid = link_excel.cell(workVal, 3).value
                if str(searchMid) in getHighHref:
                    highWork = "on"
                    driver.execute_script("arguments[0].scrollIntoView();", item_list[highCount])
                    item_list[highCount].click()
                    maxRange = random.randrange(7, 10)
                    onProductScroll(maxRange)
                        
                    break
            print('에러 예상 555555')
            print('상위 작업 체크 끝~~~~!!')
                
            # 상위에 있는거 찾는거 끝
            if highWork == "":
                item_list = driver.find_elements("xpath", "//*[contains(@class, 'product_list_item')]")
                topProduct_val = random.randrange(0, 4)
                wait_float(0.5, 1.7)
                driver.execute_script("arguments[0].scrollIntoView();", item_list[topProduct_val])
                untilEleGone(item_list[topProduct_val], ".product_list_item")

                wait_float(2, 5)

                maxRange = random.randrange(2, 4)
                onProductScroll(maxRange)

                truncBreak = ""
                truncCount = 1
                while True:
                    truncCount += 1
                    
                    resetCount = 0
                    while True:
                        resetCount += 1
                        if resetCount > 20:
                            driver.refresh()
                            wait_float(2, 4)
                            resetCount = 0
                        
                        item_list = driver.find_elements("xpath", "//*[contains(@class, 'product_list_item')]")

                        if len(item_list) < 35:
                            pg.hotkey('end')
                            wait_float(2, 4)
                        else:
                            break
                        
                    chkCount = 0
                    for item in item_list:
                        chkCount += 1
                        getHref = item.find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href')
                        searchMid = link_excel.cell(workVal, 3).value
                        wait_float(0.1, 0.3)
                        if str(searchMid) in getHref:
                            truncBreak = "on"
                            # action.move_to_element(item).perform()
                            driver.execute_script("arguments[0].scrollIntoView();", item)
                            item.click()
                            maxRange = random.randrange(4, 6)
                            onProductScroll(maxRange)
                            break
                        
                        

                    if truncBreak == "on":
                        break

                    pageBtn = driver.find_elements(by=By.CSS_SELECTOR, value='.paginator_list_paging__VxWMC > a')
                    for btn in pageBtn:
                        if int(btn.text) == truncCount:
                            btn.click()
                            break

        # 끝내고 allCount 값 ++
        driver.quit()
            
        # 아래 내용 웹훅 넣기
        endTime = time.time() - startTime
        
        webhook_url = "https://adpeak.kr/chk_jisho/"
        data = {'on_time' : endTime}
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type' : 'application/json'}, verify=False)
        
        

def ongo_searchItem():
    URL = "https://openapi.naver.com/v1/search/shop"
    headers = {"X-Naver-Client-Id": get_secret(
        'NAVER_API_ID'), "X-Naver-Client-Secret": get_secret('NAVER_API_SECRET')}
    # 전체 반복 시작 전 지쇼 링크 열고 전체 행 갯수 체크
    jisho_wb = openpyxl.load_workbook('./etc/jisho_link.xlsx')
    link_excel = jisho_wb.active
    setVal = "wait"
    linkCount = 1

    while setVal != None:
        linkCount += 1
        setVal = link_excel.cell(linkCount, 2).value

    print(linkCount)

    for i in range(1, linkCount):
        keyword = link_excel.cell(i, 2).value
        tong = link_excel.cell(i, 1).value
        productId = link_excel.cell(i, 3).value

        keyword = keyword.strip()

        if tong is not None:
            tong = tong.strip()
            if tong == "SK":
                tong = "SKT"
            elif tong == "LG":
                tong = "LG U+"

        productId = str(productId)

        allCount = 0
        itemCount = 0
        chk_loop = ""
        while chk_loop == "":
            try:
                params = {'query': keyword, 'start': allCount *
                          100 + 1, 'display': '100'}
                res = requests.get(URL, headers=headers, params=params).json()
                for item in res['items']:
                    if tong is not None:
                        if item['category3'] == tong:
                            itemCount += 1
                    else:
                        itemCount += 1
                    if item['productId'] == productId:
                        chk_loop = "ok"
                        link_excel.cell(i, 8).value = itemCount
                        jisho_wb.save('./etc/jisho_link.xlsx')
                        break
                allCount += 1
            except:
                link_excel.cell(i, 8).value = "측정불가"
                jisho_wb.save('./etc/jisho_link.xlsx')
                break
    pg.alert(text="순위 검색이 완료 되었습니다.")
    


def gabi_chk():
    
    gabi_wb = openpyxl.load_workbook('./etc/chk_gabi.xlsx')
    gabi_ex = gabi_wb.active


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    chkCount = 0
    while True:
        findProduct = ''
        chkCount += 1
        linkNum = gabi_ex.cell(chkCount, 3).value
        if linkNum is None:
            pg.alert('완료 했습니다.')
            sys.exit(0)
        
        driver.get(f'https://search.shopping.naver.com/catalog/{linkNum}')
        
        optBox = searchElement('.filter_condition_group__h8Gss', driver)
        radioList = optBox[0].find_elements(by=By.CSS_SELECTOR, value='.filter_label__3GLbR')
        for radio in radioList:
            if '기기변경' in radio.text:
                radio.click()
        
        wait_float(0.9,1.5)
        productList = searchElement('.productByMall_mall_area__4i3v_', driver)
        for product in productList:
            if '더싼폰' in product.text:
                gabi_ex.cell(chkCount, 6).value = '있음'
                findProduct = 'ok'
                break
        if findProduct == '':
            gabi_ex.cell(chkCount, 6).value = '없음!!!!!'
        gabi_wb.save('./etc/chk_gabi.xlsx')