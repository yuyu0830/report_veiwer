from bs4 import BeautifulSoup as bs
from selenium import webdriver

driver_location = '' #드라이버 위치
#\ 대신 /(슬래시), C:\User\~~~ 일 경우 /User/~~ 부터
#예시 ) /Users/yuyu0/Downloads/chromedriver

#화면 없이 코드
webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

#변수 설정
ID = ''
PWD = ''

#코드 내 사용 변수 설정
headless = 1  #0 화면 있음, 1 화면 없음
subject = [] #과목들
subject_temp = [] #과목 임시
subject_all = [] #전과목 + 과목묶음
cal = 0
cal2 = 0
status = [] #영상 듣기 현황
status_temp = [] #현황 임시
report = [] #과제 제출 현황
report_temp = [] #과제 임시 
term = [] #과목 묶음
term_index = [] #과목 임시
temp = [] #임시
class_num1 = ''
class_num2 = ''
report_num = ''
temp_text1 = ''
temp_text2 = ''
temp_text3 = 0
unopen = []

#화면, 드라이버 설정
if headless == 1:
    driver = webdriver.Chrome(driver_location, options=webdriver_options)
else:
    driver = webdriver.Chrome(driver_location)
driver.implicitly_wait(time_to_wait=5)

#사이트 목록
login = 'https://lms.kit.ac.kr/ilos/main/member/login_form.acl'

#로그인 페이지
driver.get(login)
driver.find_element_by_name('usr_id').send_keys(ID)
driver.find_element_by_name('usr_pwd').send_keys(PWD)
driver.find_element_by_xpath('//*[@id="login_btn"]').click()

#메인 페이지
html = driver.page_source
soup = bs(html, 'html.parser')


#과목 수 구하기
temp = soup.select('.term_info') #과목 묶음 개수
for i in range(len(temp)):
    term.append(temp[i].text)

temp = soup.select('div.m-box2:nth-child(2) > ol > li')
for i in range(len(temp)): #임시 리스트 정리
    temp_text1 = temp[i].text.replace(' ','')
    if temp_text1 != '':
        subject_all.append(temp_text1.replace('\n', ''))

temp = soup.select('.sub_open') #수강과목 개수
for i in range(len(temp)):
    temp_text1 = temp[i].text.replace(' ','')
    subject_temp.append(temp_text1.replace('\n', ''))

temp = []
if len(term) != 1: #과목 묶음별로 과목 나누기
    for i in term:
        term_index.append(subject_all.index(i))
    term_index.append(len(subject_all))
    for i in range(len(term_index) - 1):
        for j in range(term_index[i] - i, term_index[i+1] - (1 + i)):
            temp.append([subject_temp[j], 0])
        subject.append(temp)
        temp = []
else:
    for i in range(len(subject_temp)):
        temp.append([subject_temp[i], 0])
    subject.append(temp)

temp = []
del term_index
del subject_temp
del subject_all

cal2 = 2
#과목별 강의 수, 들은 여부 구하기
for i in range(len(term)): #과목묶음으로 묶기
    for j in range(len(subject[i])): #과목으로 묶기
        driver.find_element_by_xpath('//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[{}]/em'.format(cal2)).click()
        html = driver.page_source
        soup = bs(html, 'html.parser')
        class_num1 = soup.select('span.wb-week')
        class_num2 = soup.select('.wb-on > div > div.wb-status')
        class_num3 = soup.select('.wb-off > div > div.wb-status')
        report_num = soup.select('div#submitList_div .site-font-color')
        for l in range(len(class_num1)): #강의 개수만큼 반복
            if cal < len(class_num2):
                temp_text1 = class_num1[l].text.replace(' ', '')
                temp_text2 = class_num2[l].text.replace(' ', '')
                if temp_text2[0] == temp_text2[2]:
                    temp_text3 = 0 #시청
                else:
                    temp_text3 = 1 #미시청
                temp.append([temp_text1, temp_text2, temp_text3])
                cal += 1
            elif cal >= len(class_num2):
                temp_text1 = class_num1[l].text.replace(' ', '')
                temp_text2 = class_num3[l - cal].text.replace(' ', '')
                temp_text3 = 2 #미공개
                temp.append([temp_text1, temp_text2, temp_text3])
                cal += 1
        if len(report_num) >= 2:
            report_temp.append([int(report_num[0].text), int(report_num[1].text.replace('%', ''))])
        else:
            report_temp.append([0, 0])
        cal = 0
        status_temp.append(temp)
        temp = []
        cal2 += 1
        driver.back()
    report.append(report_temp)
    status.append(status_temp)
    report_temp = []
    status_temp = []
    cal2 += 1

del status_temp
cal = 0
for i in range(len(status)):
    print("\n{}".format(term[i]))
    for j in range(len(status[i])):
        print("\n과목 : {}".format(subject[i][j][0]))
        print("    시청 여부")
        for k in range(len(status[i][j])):
            if status[i][j][k][2] == 1:
                print("        {}차 시청 미완료".format(status[i][j][k][0]))
                cal += 1
            elif status[i][j][k][2] == 2:
                print("        {}차 미개봉".format(status[i][j][k][0]))
                cal += 1
        if cal == 0:
            print("      과목 시청 완료")
        else:
            cal = 0
        print("    과제 여부")
        if report[i][j][0] != 0:
            if report[i][j][1] != 100:
                print("        과제 미제출")
            else:
                print("        과제 제출 완료")
        else:
            print("        과제 없음")
