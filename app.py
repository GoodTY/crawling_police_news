# https://jxxngho.tistory.com/102

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# 크롬 웹드라이버 실행 경로
path = 'chromedriver.exe'

# 크롤링할 주소
target_url = "https://news.naver.com/"

# 열 리스트
press_company = [] #신문사 이름
press_ranking = [] # 기사 순위
press_title = [] # 기사 제목
press_date = [] # 기사 발행일

# 크롬 드라이버 사용
service = Service(executable_path=path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

# 드라이버에게 크롤링할 대상 알려주기
driver.get(target_url)

driver.implicitly_wait(2) # 2초 안에 웹페이지를 load하면 바로 넘어가거나, 2초를 기다림

# 랭킹뉴스 클릭
driver.find_element(By.XPATH,'/html/body/section/header/div[2]/div/div/div/div/div/ul/li[8]/a/span').click()

journalism = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[4]/div[2]') # 언론사별 랭킹뉴스 box
journalism_list = journalism.find_elements(By.CLASS_NAME,'rankingnews_box') # 각 언론사별 box

url_news = []
for head in journalism_list:
    tag_name = head.find_element(By.TAG_NAME,'a') # a태그 찾아서
    href = tag_name.get_attribute('href') # 그 안에 href속성, 중앙일보, 서울경제 등 데이터 들어있음
    # print(href)
    url_news.append(href)

for head in journalism_list:
    tag_name = head.find_element(By.TAG_NAME,'a') # a태그 찾아서
    # print(tag_name)
    href = tag_name.get_attribute('href') # 그 안에 href속성, 중앙일보, 서울경제 등 데이터 들어있음
    # print(href)
    url_news.append(href)

for url in url_news:
    driver.get(url)

    press_name = driver.find_element(By.XPATH,'/html/body/div[2]/div/section[1]/header/div[4]/div/div[2]/div[1]/div/h3')
    # print(press_name.text) # 언론사 이름 출력
    rank = driver.find_element(By.XPATH, '//*[@id="ct"]/div[2]/div[2]/ul') # 1~10 랭킹 xpath
    rank_url = rank.find_elements(By.CLASS_NAME,'as_thumb') # 뉴스 타이틀 

    url_top10=[] # 1~10위 
    for rank in rank_url:
     tag_name = rank.find_element(By.TAG_NAME,'a') # a태그 찾아서
     href = tag_name.get_attribute('href') # 그 안에 href속성
     url_top10.append(href) # 들어갈 링크 주소 10개 리스트에 저장
     press_company.append(press_name.text)

    for i in range(0,len(url_top10)): # 각 언론사별 1~10위 뉴스
        driver.get(url_top10[i]) # 저장한 링크 들어간다.
        news_title = driver.find_element(By.XPATH,'//*[@id="title_area"]/span')
        # print('{}등, {}'.format(i+1,news_title.text))
        press_ranking.append(i+1)
        press_title.append(news_title.text)

data = {"press_name" : press_company,"ranking" : press_ranking,"title" : press_title}
df = pd.DataFrame(data)
df.to_csv("./result_data/test.csv", encoding = "utf-8-sig")