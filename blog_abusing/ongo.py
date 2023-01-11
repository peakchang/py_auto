from func import *

###


def goScript(getDict):
    
    
    blog_list_file = load_workbook('./etc/blog_list.xlsx')
    blog_list = blog_list_file.active
    allCount = 1
    preIp = ''
    while True:
        allCount += 1
        
        
        # 아이피 변경
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
        
        while True:
            wait_float(1.5,2.9)
            getInfo = requests.get("https://adpeak.kr/nwork/getnid").json()
            if getInfo:
                break
        
        getUa = getInfo['n_ua']
        getId = getInfo['n_id']
        getPwd = getInfo['n_pwd']
        
        with open('./etc/useragent/useragent_all.txt', 'r') as r:
            uaList = r.readlines()
            
        uaInfo = uaList[int(getUa)]
        options = Options()
        service = Service(ChromeDriverManager().install())
        options.add_argument(f'user-agent={uaInfo}')
        driver = webdriver.Chrome(service=service, chrome_options=options)
        driver.get('https://www.naver.com')
        
        
        
        errchk = naverLogin_mobile(getId, getPwd, driver)
        if errchk is not None:
            allCount = allCount - 1
            continue
        
        mainToPost(driver,blog_list_file,allCount)
        pg.alert('대기요~~~~~')
        
        
        pg.moveTo(300,500)
        focus_window('블로그')
        scrollRanVal = random.randrange(10,20)
        gongamRanVal = random.randrange(5,18)
        scrapRanVal = random.randrange(5,18)
        for i in range(scrollRanVal):
            wait_float(2.2,3.1)
            scrollVal = random.randrange(100,300)
            pg.scroll(-scrollVal)
            if i == gongamRanVal:
                wait_float(0.5,1.2)
                gongamBtn = searchElement('.u_likeit_list_module._reactionModule', driver)
                for btn in gongamBtn:
                    try:
                        btn.click()
                        break
                    except:
                        pass
                    
            if i == scrapRanVal:
                wait_float(0.5,1.2)
                scrapBtn = searchElement('.naver-splugin.btn_share', driver)
                for btn in scrapBtn:
                    try:
                        pg.scroll(400)
                        btn.click()
                        break
                    except:
                        pass
                wait_float(0.5,1.2)
                scrap_more = searchElement('.spi_swipe_area', driver)
                blogScrapBtn = scrap_more[0].find_element(by=By.CSS_SELECTOR, value='.spim_be')
                blogScrapBtn.click()
                wait_float(0.5,1.2)
                searchElement('.post_wr_og', driver)
                # searchElement('.set_close.on', driver)
                btn_ok = searchElement('.btn_ok', driver)
                btn_ok[0].click()
                cancleBtn = searchElement('#_confirmLayercancel', driver)
                cancleBtn[0].click()
        goToBlog = searchElement('.Nicon_service', driver)
        goToBlog[0].click()
        goToNaver = searchElement('.icon_logo_naver__vBku4', driver)
        goToNaver[0].click()
        wait_float(2.2,3.5)
        
                