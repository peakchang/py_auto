from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    
    # pcUser = getpass.getuser()
    
    options = Options()
    user_data = f'C:\\Users\\pcy\\AppData\\Local\\Google\\Chrome\\User Data\\default'
    service = Service(ChromeDriverManager().install())
    options.add_argument(f"user-data-dir={user_data}")
    options.add_argument(f'--profile-directory=Profile 2')
    driver = webdriver.Chrome(service=service, chrome_options=options)
    
    
    # driver.get('https://web.telegram.org/z/')
    driver.get('https://web.telegram.org/')
    
    pg.alert('대기~~~')
    
    # sideBar = searchElement('.animated-menu-icon .ripple-container',driver)
    # sideBar[0].click()
    
    hamBtnWrap = driver.find_element(by=By.CSS_SELECTOR, value='.translucent.round.has-ripple')
    pg.alert(hamBtnWrap)
    hamBtn = hamBtnWrap.find_element(by=By.CSS_SELECTOR, value='.ripple-container')
    hamBtn.click()
    
    pg.alert()
    
    
    
    sideBarMenu = searchElement('.menuitem',driver)
    for barMenu in sideBarMenu:
        if 'Contacts' in barMenu.text:
            barMenu.click()
    
    
    floatBtn = driver.find_element(by=By.CSS_SELECTOR, value='.FloatingActionButton.revealed')
    floatBtn.click()
    
    pg.alert('대기~~~')
    
    
    