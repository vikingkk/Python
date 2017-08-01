# -*- coding: utf-8 -*-
import requests
import pandas as pd
from dateutil.parser import parse
from selenium import webdriver
import time
from bs4 import BeautifulSoup
# 在Facebook Graph API Exploer取得token

serachtime =0
token = 'your token'
fanpage_id = '1703467299932229'

# 建立一個空的list

information_list = []
likes_pages =[]
# 目標頁面

res = requests.get('https://graph.facebook.com/v2.8/{}/posts?limit=100&access_token={}'.format(fanpage_id, token))
page = 1

# API最多一次呼叫100筆資料，因此使用while迴圈去翻頁取得所有的文章
# 最多一次呼叫100筆貼文

print('web open!')
driver = webdriver.Firefox()
#Selenium version = 2.53 ; Firefox version = 46
driver.get('https://www.facebook.com')

print('web open!')

time.sleep(1)
user = driver.find_element_by_css_selector('#email')
user.send_keys('your_mail')
password = driver.find_element_by_css_selector('#pass')
password.send_keys('your_password')
login = driver.find_element_by_css_selector('#u_0_r')
login.click()

while 'paging' in res.json():
    for index, information in enumerate(res.json()['data']):
        print('正在爬取第{}頁，第{}篇文章'.format(page, index + 1))

        # 判斷是否為發文，是則開始蒐集按讚ID

        if 'message' in information:
            res_post = requests.get(
                'https://graph.facebook.com/v2.8/{}/likes?limit=1000&access_token={}'.format(information['id'], token))
            # 此篇文內的按讚人數
            # 判斷按讚人數是否超過1000人，若超過則需要翻頁擷取；當沒有人按讚時，按讚人名與ID皆為NO

            try:
                if 'next' not in res_post.json()['paging']:
                    for likes in res_post.json()['data']:
                        information_list.append(
                             likes['id'])
                                # get the like id
                    for comments in res_post.json()['data']:
                        information_list.append(
                            comments['id']
                             )
                        # get the comments id
                elif 'next' in res_post.json()['paging']:
                    while 'paging' in res_post.json():
                        for likes in res_post.json()['data']:
                            information_list.append(
                                 likes['id'])
                        for comments in res_post.json()['data']:
                            information_list.append(
                                comments['id']
                                 )
                        if 'next' in res_post.json()['paging']:
                            res_post = requests.get(res_post.json()['paging']['next'])
                        else:
                            break
            except:
                print('except!')
                #information_list.append(
                 #   [information['id'], information['message'], parse(information['created_time']).date(), "NO", "NO"])
    if 'next' in res.json()['paging']:
        res = requests.get(res.json()['paging']['next'])
        page += 1
    else:
        break

print('collect all massage and like id!')

df = pd.DataFrame(information_list)
df.to_csv('MassageAndLikeList.csv', index=False, encoding='utf-8')


for element in information_list:
    serachtime=serachtime+1
    if(serachtime==100):
        break
    # load element for collect like pages
    likes_pages.append([element])
    driver.get(
        'https://www.facebook.com/{}'.format(element))

    if "profile" in driver.current_url:
        driver.get(
            '{}&sk=likes'.format(driver.current_url))
    else:
        driver.get(
            '{}/likes'.format(driver.current_url))

    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource, "html.parser")
    findul = soup.find_all('ul', 'uiList _153e _5k35 _620 _509- _4ki')

    for d in findul:
        # out of the loop if no likes page
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True
            

        pageSource = driver.page_source  # 取得網頁原始碼
        soup = BeautifulSoup(pageSource, "html.parser")
        divs = soup.find_all('div', 'fsl fwb fcb')
        for d in divs:

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                likes_pages.append([href])
                #print(href, title)

likesdf = pd.DataFrame(likes_pages)
likesdf.to_csv('LikesPagesList.csv', index=False, encoding='utf-8')

#page = ulnumber
 #           ulnumber = 1  # reset likes page
 #           driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
 #           time.sleep(1)
 #           scrolltimes = scrolltimes + 1

 #           pageSource = driver.page_source  # 取得網頁原始碼
 #           soup = BeautifulSoup(pageSource, "html.parser")
  #          findul = soup.find_all('ul', 'uiList _153e _5k35 _620 _509- _4ki')
  #          for d in findul:
  #              ulnumber = ulnumber + 1
