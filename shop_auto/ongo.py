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
            if link_excel.cell(exCount, 2).value is None:
                break
            exCount += 1
        workArr = list(range(1,exCount))
        random.shuffle(workArr)
        
        # 설정 끝~ 접속하기
        ua_data = linecache.getline('./etc/useragent/useragent_all.txt', random.randrange(1, 14)).strip()
        options = Options()
        user_agent = ua_data
        options.add_argument('user-agent=' + user_agent)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(chrome_options=options, service=service)

        driver.get('https://shopping.naver.com/')

        time.sleep(2)
        focus_window('네이버쇼핑')

        for workVal in workArr:
            searchKeyword = link_excel.cell(workVal, 2).value
            
            #검색기록 삭제 만들기!!!!!! .recentHistory_list_word__EJZeH // .recentHistory_btn_del__greg5
            searchJisho(searchKeyword, driver)
            
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
                    if setTong in category_name:
                        chkin_tong = "on"
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
                    
            # 상위 4개 중 1개 클릭
            
            # 여기서 6개까지 찾고 / 그중에 있으면 그냥 한번만, 없으면 원래대로
            
            pg.alert('대기~~~')
            
            searchMidVal = str(link_excel.cell(workVal, 3).value).strip()
            maxPageCount = link_excel.cell(workVal, 4).value
            if maxPageCount is None:
                maxPageCount = 4
            else:
                maxPageCount = int(maxPageCount)
            
            whCount = 0
            getSearch = ''
            while whCount < maxPageCount:
                whCount += 1
                
                searchElement('.basicFilter_filter_button_area__A_l9Y',driver)
            
                while True:
                    item_list = driver.find_elements("xpath", "//*[contains(@class, 'product_list_item')]")
                    if len(item_list) > 30:
                        break
                    wait_float(0.5,1.2)
                    pg.press('end')
                    
                    
                for item in item_list:
                    getItemHref = item.find_element(by=By.CSS_SELECTOR, value='.product_info_main__piyRs').get_attribute('href')
                    # pg.alert(getItemHref)
                    # pg.alert(searchMidVal)
                    if searchMidVal in getItemHref:
                        whCount = maxPageCount
                        getSearch = 'on'
                        
                        driver.execute_script("arguments[0].scrollIntoView();", item)
                        item.click()
                        
                        onProductScroll(5,driver)
                        pg.alert('대기!!')
                
                if getSearch == '':
                    pageBtn = driver.find_elements(by=By.CSS_SELECTOR, value='.paginator_list_paging__VxWMC > a')
                    pageBtn[whCount].click()
                
            
            pg.alert('도는거 끝남여!')

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