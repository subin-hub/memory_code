###<<네이버 영화 크롤링>>

import time #속도 위한 
from selenium import webdriver
from model_actor import Actor #만들어놓은 클래스 선언
from model_movie import movie #movie 클래스 선언

driver = webdriver.Chrome()
driver.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200729')

#테이블 찾아서 xpath 복사하기
table = driver.find_element_by_xpath('//*[@id="old_content"]/table')
tbody = table.find_element_by_xpath('.//tbody')
trs = tbody.find_elements_by_xpath('.//tr')
urls=list()

#a태그 속 href 긁어오기 (각각의 영화를 클릭해서 상세페이지 들어가야함)
for tr in trs :
    tds = tr.find_elements_by_xpath('.//td')
    if len(tds) == 1 :
        continue 

    div=tds[1].find_element_by_xpath('.//div')
    a = div.find_element_by_xpath('.//a')
    href = a.get_attribute('href')
    urls.append(href)

#자동으로 url 반복 돌리기
#for url in urls:
#    driver.get(url)
#    time.sleep(5) #url 하고 5초 대기


driver.get(urls[30])
driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[2]/a').click() #배우 자동클릭

#영화정보
title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a')
nation = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[2]/a')
#print('제목 - ', title.text, '나라 - ' , nation.text)

#더보기 버튼 클릭
driver.find_element_by_xpath('//*[@id="actorMore"]').click()

# 구조 : 
#배우정보 가져오기 : ul > ul 안에 lis 가져오기
lis  = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div/div[2]/ul/li')

act_list = list()

#반복문으로 lis 가져오기
for li in lis :
    actname = li.find_element_by_xpath('.//div/a')
    ename = li.find_element_by_xpath('.//div/em')
    #밑에는 li안의 class 직접 찾아들어가는 것
    p_part = li.find_element_by_xpath('.//*[@class="p_part"]')
    pe_cmt = li.find_element_by_xpath('.//*[@class="pe_cmt"]')
    #print(actname.text,";", ename.text,";", p_part.text,";", pe_cmt.text,";")

    #인스턴스로 변환
    act = Actor(actname.text, ename.text, p_part.text, pe_cmt.text)
    act_list.append(act)

#print('제목 : {0}, 제작국가 : {1} '.format(title.text, nation.text))
#for act in act_list :
#    print('{0}:{1} ({2})'.format(act.p_part, act.actname, act.ename))

mov = movie(title.text, nation.text, act_list)
