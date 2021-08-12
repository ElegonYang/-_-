import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import parse
from bs4 import BeautifulSoup
from pprint import *
import csv
import pandas as pd
import time
import regex as re

start = time.time()

all_page_url = []
res_tel_data = []
res_page_url = []
res_name_data = []
res_level_data = []
res_review_count_data = []
res_address_data = []
res_area_data = []
user_id_list = []
po_time_id_list = []
po_message_list = []

ori_url_head = "https://ifoodie.tw"
ori_url = 'https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list?page='
reviews_url_keyword = "#reviews"
date_reg_exp = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 Safari/537.36 '
}


# 生成頁數對應網址
def url_set():
    for i in range(1, 68):
        url = ori_url + str(i)
        all_page_url.append(url)


# 取出網址 解析response
def get_response__res__name__level__address():
    for url in all_page_url:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        # 用選擇器選出 店名\星等\評論數\地址
        shop_name_class = soup.select("div[class='jsx-3081451459 item-list'] a[class='jsx-1475985536 title-text']")
        res_address_class = soup.select(
            "div[class ='jsx-1475985536 info-rows'] div[class ='jsx-1475985536 address-row']")
        # 將店名加入 店名list
        for name in shop_name_class:
            res_name_data.append(name.text)
        # 將店址加入 店址list
        for address in res_address_class:
            res_address_data.append(address.text)
    # 店址 前六個字篩選 "XX市XX區"
    for address_info in res_address_data:
        new_area = address_info[0:6]
        res_area_data.append(new_area)


def get_res_url():
    for url in all_page_url:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        res_web_url_get_class = soup.select('a[class="jsx-1475985536 title-text"]')

        for class_info in res_web_url_get_class:
            res_web_link = class_info.get('href')
            res_url = ori_url_head + res_web_link
            res_page_url.append(res_url)


def tel():
    for res_url in res_page_url:
        response = requests.get(res_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        res_level = soup.select("div[class='jsx-307016528 title-outer'] div[class='jsx-1207467136 text']")
        res_tel = soup.select(
            "div[class='jsx-1692663080 phone-wrapper'] span[class='jsx-1692663080 detail'] a[class='jsx-1692663080']")

        if not res_tel:
            res_tel_data.append("None")
        else:
            for tel_number in res_tel:
                number = tel_number.text
                res_tel_data.append(number)

        if not res_level:
            res_level_data.append("None")
        else:
            for res_level in res_level:
                level = res_level.text
                res_level_data.append(level)


def get_review_class():

    google_driver = webdriver.Chrome("chromedriver.exe")

    for res_url in res_page_url:
        res_review_page_url = res_url + reviews_url_keyword

        google_driver.get(res_review_page_url)

        response = requests.get(res_review_page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            target_button = google_driver.find_elements(By.CSS_SELECTOR,
                                                        'button[class="jss76 jss50 jss52 jss55 btn-more-checkin"]')

            try:
                while target_button:
                    target_button.click()
                    time.sleep(5)

            except Exception as e:
                pass

            poster_id_class = google_driver.find_elements(By.CSS_SELECTOR,
                                                          "div[class='jsx-1937851871 username-outer'] a[class='jsx-1937851871 username']")
            poster_time_class = google_driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-1937851871 date")
            # poster_message = google_driver.find_elements(By.CSS_SELECTOR,
            #                                       "div[class='jsx-1937851871 message']")

            poster_message = google_driver.find_elements(By.CSS_SELECTOR,
                                                         "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")

            for poster_name in poster_id_class:
                name = poster_name.text
                user_id_list.append(name)

            for poster_time in poster_time_class:
                post_time = poster_time.text
                post_time_re = re.findall(date_reg_exp, post_time)
                for post_time_after_re in post_time_re:
                    po_time_id_list.append(post_time_after_re)
            for message_info in poster_message:
                message = message_info.text
                po_message_list.append(message)
                if len(po_message_list) == len(po_time_id_list):
                    break


        except Exception as e:

            poster_id_class = google_driver.find_elements(By.CSS_SELECTOR,
                                                          "div[class='jsx-1937851871 username-outer'] a[class='jsx-1937851871 username']")
            poster_time_class = google_driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-1937851871 date")

            poster_message = google_driver.find_elements(By.CSS_SELECTOR,
                                                         "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")

            for poster_name in poster_id_class:
                name = poster_name.text
                user_id_list.append(name)
            for poster_time in poster_time_class:
                post_time = poster_time.text
                post_time_re = re.findall(date_reg_exp, post_time)
                for post_time_after_re in post_time_re:
                    po_time_id_list.append(post_time_after_re)
            for message_info in poster_message:
                message = message_info.text
                po_message_list.append(message)
                if len(po_message_list) == len(po_time_id_list):
                    break

def write_to_csv():
    dict_name_1 = {
        "PO文者ID": user_id_list,
        "PO文時間": po_time_id_list,
        "內容": po_message_list,
    }

    dict_name_2 = {
        "餐廳名稱": res_name_data,
        "星級": res_level_data,
        "評論數": res_review_count_data,
        "區域": res_area_data,
        "地址": res_address_data,
        "電話": res_tel_data,
    }

    df1 = pd.DataFrame.from_dict(dict_name_1)
    df2 = pd.DataFrame.from_dict(dict_name_2)
    df1.to_csv('crawler_result_review_ID_time.csv', encoding='utf_8_sig', )
    df2.to_csv('crawler_result.csv', encoding='utf_8_sig', )


url_set()
get_response__res__name__level__address()
get_res_url()
tel()
get_review_class()
write_to_csv()

print("餐廳數量 ↓")
print(len(res_page_url))
print("電話量 ↓")
print(len(res_tel_data))
print("星等數量 ↓")
print(len(res_level_data))
print("評論數 ↓")
print(len(res_review_count_data))

end = time.time()
time = str(end - start)

print("耗時:" + time + "秒")
