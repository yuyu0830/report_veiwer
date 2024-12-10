from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By

def html_reset():
    html = driver.page_source
    return bs(html, 'html.parser')

#ID, 비밀번호 입력
ID = ''
PWD = ''

#변수 선언
count = 0
all_see = True
subject = [[], [], []] #대분류, 전체, 과목
index = []
status = []
selector = ['.term_info', 'div.m-box2:nth-child(2) li', 'div.m-box2:nth-child(2) em']
selector2 = ['span.wb-week', '.wb-on > div > div.wb-status', '.wb-off > div > div.wb-status']
class_num = [[], [], []]
temp_list = [[], [], []]

#드라이버
webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')
driver = webdriver.Chrome(executable_path='chromedriver', options=webdriver_options)
driver.implicitly_wait(time_to_wait=5)
driver.get('https://lms.kit.ac.kr/ilos/main/member/login_form.acl')
i = input()
driver.find_element(By.ID, 'usr_id').send_keys(ID)
driver.find_element(By.ID, 'usr_pwd').send_keys(PWD)
driver.find_element(By.XPATH, '//*[@id="login_btn"]').click()

soup = html_reset()

for i in range(3): #과목 개수 입력
    temp = soup.select(selector[i])
    for j in temp:
        subject[i].append(j.text.replace(' ','').replace('\n', ''))
        
for i in subject[0]: #대분류 위치
    index.append(subject[1].index(i))
index.append(len(subject[1]))

#과목별 강의 수, 들은 여부 구하기
for i in range(len(subject[1]) - 1):
    if i not in index:
        link = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[%d]/em' % (i + 1)
        if driver.find_element(By.XPATH, link).get_attribute('class') == 'sub_open':
            driver.find_element(By.XPATH, link).click()
            soup = html_reset()
            for j in range(3):
                temp_list[j] = soup.select(selector2[j])
            if type(temp_list[0]) != type(None):
                for j in range(3):
                    for k in range(len(temp_list[j])):
                        class_num[j].append(temp_list[j][k].get_text())
            if class_num[0] != []:
                for j in range(len(class_num[1])):
                    if class_num[1][j][1] == class_num[1][j][3]:
                        class_num[1][j] = 1
                    else:
                        class_num[1][j] = 0
                for j in range(len(class_num[2])):
                    if class_num[2][j][1] == class_num[2][j][3]:
                        class_num[2][j] = 1
                    else:
                        class_num[2][j] = 0
            driver.find_element(By.XPATH, '//*[@id="submitList_div"]/div[1]').click()
            html = driver.page_source
            soup = bs(html, 'html.parser')
            report = soup.select_one('span#total_nosubmit').get_text()
            status.append([class_num[0], class_num[1], class_num[2], report])
            temp_list = [[], [], []]
            class_num = [[], [], []]
            report = ''
            driver.back()
        else:
            status.append([[], [], [], '0'])

#출력
for i in range(len(subject[1]) - 1):
    if i in index:
        print("%s" % subject[0][count])
        count += 1
    else:
        print("  %s" % subject[2][i - count])
        if status[i - count][0] == []:
            print("    영상 없음")
        else:
            for j in range(len(status[i - count][1])):
                if status[i - count][1][j] == 0:
                    print("    %4s차 영상 미시청" % status[i - count][0][j])
                    all_see = False
            if all_see == True:
                print("    시청 완료")
            for j in range(len(status[i - count][2])):
                print("    %4s차 영상 미개봉" % status[i - count][0][j + len(status[i - count][1])])
        if status[i - count][3] != '0':
            print("    미제출 과제 있음")
        else:
            print("    과제 제출 완료")
    all_see = True
