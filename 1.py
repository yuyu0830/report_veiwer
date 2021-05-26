from bs4 import BeautifulSoup as bs
from selenium import webdriver

driver_location = '/Users/yuyu0/Downloads/chromedriver'
#화면 없이 코드
webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')
#변수 설정
ID = '20210472'
PWD = 'bloger1541'
headless = 0  #0 화면 있음, 1 화면 없음
if headless == 1:
    driver = webdriver.Chrome(driver_location, options=webdriver_options)
else:
    driver = webdriver.Chrome(driver_location)
#코드 내 사용 변수 설정
subject = [] #과목들
a = ''
#사이트 목록
url = 'https://lms.kit.ac.kr/ilos/st/course/submain_form.acl'
login = 'https://lms.kit.ac.kr/ilos/main/member/login_form.acl'
#로그인 페이지
driver.get(login)
driver.find_element_by_name('usr_id').send_keys(ID)
driver.find_element_by_name('usr_pwd').send_keys(PWD)
#로그인 버튼
driver.find_element_by_xpath('//*[@id="login_btn"]').click()

html = driver.page_source
soup = bs(html, 'html.parser')



subject_num = soup.select('div.m-box2 > ol > li > em') #과목 수
for title in subject_num:
    a = title.text.replace(' ', '')
    subject.append(a.replace('\n',''))

driver.find_element_by_xpath('//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[2]/em').click() #강의영상 화면

class_num = soup.select('div') #강의 수


print(subject)
    





##driver.find_element_by_xpath('//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[2]/em').click()

##//*[@id="login_btn"]
##//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[2]/em
##https://lms.kit.ac.kr/ilos/st/course/submain_form.acl
##https://lms.kit.ac.kr/ilos/main/member/login_form.acl

##C:\Users\KITVR06\Desktop\chromedriver_win32
