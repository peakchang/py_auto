from func import *


# chrome://version/ 에서 '프로필경로' 복사, 난 왜 디폴트만 되지?? 뭔... 딴건 필요 없쓰....


def goScript(getDict):
    
    
    
    pcUser = getpass.getuser()
    
    options = Options()
    user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
    service = Service(ChromeDriverManager().install())
    options.add_argument(f"user-data-dir={user_data}")
    options.add_argument(f'--profile-directory=Profile 1')
    driver = webdriver.Chrome(service=service, chrome_options=options)
    
    driver.get('https://web.telegram.org/k/')
    
    pg.alert('대기~~~')
    
    sideBar = searchElement('.sidebar-tools-button.is-visible',driver)
    sideBar[0].click()
    
    userUpdate = driver.find_element(by=By.CSS_SELECTOR, value='.tgico-user')
    userUpdate.click()
    
    
    
    pg.alert('대기~~~')
    
    
    