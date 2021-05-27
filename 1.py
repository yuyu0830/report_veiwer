from bs4 import BeautifulSoup as bs
from selenium import webdriver

driver_location = '/Users/kitcomputer/Downloads/chromedriver'
#화면 없이 코드
webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

#변수 설정
ID = '20210472'
PWD = 'bloger1541'

#코드 내 사용 변수 설정
headless = 0  #0 화면 있음, 1 화면 없음
subject = [] #과목들
a = '' #임시
b = ''
n = [] #임시
n1 = []
g = ''
#화면, 드라이버 설정
if headless == 1:
    driver = webdriver.Chrome(driver_location, options=webdriver_options)
else:
    driver = webdriver.Chrome(driver_location)

#사이트 목록
login = 'https://lms.kit.ac.kr/ilos/main/member/login_form.acl'

#로그인 페이지
driver.get(login)
driver.find_element_by_name('usr_id').send_keys(ID)
driver.find_element_by_name('usr_pwd').send_keys(PWD)
driver.find_element_by_xpath('//*[@id="login_btn"]').click()

#메인 페이지
driver.find_element_by_xpath('//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[2]/em').click() #수강과목

#수강과목 페이지
driver.find_element_by_xpath('//*[@id="subject-span"]').click()
html = driver.page_source
soup = bs(html, 'html.parser')

#과목 수 구하기
subject_num = soup.select('.dlBox > dd span:nth-child(1)') #과목 수
for i in range(len(subject_num)):
    a = subject_num[i].text.replace(' ', '')
    subject.append([a.replace('\n', ''), False])
driver.find_element_by_xpath('//*[@id="subjectForm"]/div[1]/div/img').click() #과목 끝

#과목별 강의 수, 들은 여부 구하기
for i in range(len(subject_num) - 1):
    class_num = soup.select('.wb-status') #강의 수
    for j in range(len(class_num)):
        a = class_num[j].text.replace(' ', '')
        if a[0] == a[2]:
            b = True
        else:
            b = False
        n1.append([a, b])
    n.append(n1)
    n1 = []
    print(n)
    driver.find_element_by_xpath('//*[@id="subject-span"]').click()
    driver.find_element_by_xpath('//*[@id="dlBox"]/dd[{}]'.format(i+2)).click()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    
for i in range(len(n)):
    print(n[i])
