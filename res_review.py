from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import *
import pandas as pd
import re
import time

opt = Options()
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
opt.add_argument("user-agent={}".format(ua))
opt.add_argument("--blink-settings=imagesEnabled=false")
# opt.add_argument('--headless')
driver = webdriver.Chrome("chromedriver.exe", chrome_options=opt)

home_page_url = "https://ifoodie.tw/explore/"
page_url = '/list?page='

res_15_in_page_list = []
res_name_list = []

city_key = ['台北市', '基隆市', '新竹市', '嘉義市', '宜蘭縣', '新竹縣',
            '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣',
            '花蓮縣', '臺東縣', '花蓮縣', '澎湖縣', '臺北市', '新北市',
            '桃園市', '臺中市', '臺南市', '高雄市', '金門縣']

test_city_key = ['台北市']

date_reg_exp = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}')

user_id_list = []
po_time_id_list = []
po_message_list = []


def deco_time(func):
    def time_count():
        time_start = time.time()
        func()
        time_end = time.time()
        message = (time_end - time_start) * 1000
        print("func {fun_name} ,time use {time}".format(fun_name=func, time=message))


# 生成1~68頁的網址清單 每頁有15間餐廳
def page_set():
    for city in city_key:
    # for city in test_city_key:
        # for page in range(1, 2):
        for page in range(1, 69):
            # 結合網址 + 頁數
            # res_page = res_taipei_homepage_key + str(page)  # 台北
            res_page = home_page_url + city + page_url + str(page)  # 全台各地區 每區68頁
            # 開啟網址
            driver.get(res_page)
            # 找尋餐廳超連結
            res_web_class = driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-3440511973 title'] a[href]")
            # 解析class內容 將餐廳超連結加入list
            for res_text in res_web_class:
                res_href = res_text.get_attribute('href')
                res_15_in_page_list.append(res_href)
        # 刪除第一筆餐廳資料>>>廣告
        del res_15_in_page_list[0]


def res_review_info():
    for res_url in res_15_in_page_list:
        # 開啟網址
        driver.get(res_url)
        # 再入更多按鈕確認
        try:
            res_page_more_btn = driver.find_element(By.CSS_SELECTOR,
                                                    'button[class="jss76 jss50 jss52 jss55 btn-more-checkin"]')
            try:
                # 如果載入更多存在 持續點擊
                while res_page_more_btn:
                    res_page_more_btn.click()
                    time.sleep(1)

            except Exception as e:
                # 載入更多不再的話 找出/po文者id/po文時間/評論內容
                po_id_class = driver.find_elements(By.CSS_SELECTOR,
                                                   "div[class='jsx-1937851871 username-outer'] a[class='jsx-1937851871 username']")
                po_time_class = driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-1937851871 date")
                po_message = driver.find_elements(By.CSS_SELECTOR,
                                                  "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")

                # 濾出class內容文字

                # 濾出po文者id 加入清單
                for poster_name in po_id_class:
                    name = poster_name.text
                    user_id_list.append(name)
                # 濾出po文者時間 加入清單
                for poster_time in po_time_class:
                    post_time = poster_time.text
                    # 正則表達式 過濾掉其他文字 並加入清單
                    post_time_re = re.findall(date_reg_exp, post_time)
                    for post_time_after_re in post_time_re:
                        po_time_id_list.append(post_time_after_re)
                # 濾出 訊息內容 加入清單
                for message_info in po_message:
                    message = message_info.text
                    po_message_list.append(message)
                    # 停止條件
                    if len(po_message_list) == len(po_time_id_list):
                        break

        except Exception as e:

            po_id_class = driver.find_elements(By.CSS_SELECTOR,
                                               "div[class='jsx-1937851871 username-outer'] a[class='jsx-1937851871 username']")
            po_time_class = driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-1937851871 date")
            po_message = driver.find_elements(By.CSS_SELECTOR,
                                              "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")

            for poster_name in po_id_class:
                name = poster_name.text
                user_id_list.append(name)

            for poster_time in po_time_class:
                post_time = poster_time.text
                post_time_re = re.findall(date_reg_exp, post_time)
                for post_time_after_re in post_time_re:
                    po_time_id_list.append(post_time_after_re)
            for message_info in po_message:
                message = message_info.text
                po_message_list.append(message)
                if len(po_message_list) == len(po_time_id_list):
                    break


def write_to_csv():

    all_info = {
        "po文者ID": user_id_list,
        "po文時間": po_time_id_list,
        "評論內容": po_message_list,
    }
    df1 = pd.DataFrame.from_dict(all_info)
    df1.to_csv('愛食客_發文者_發文時間_評論內容.csv', encoding='utf_8_sig', index=False)


page_set()
res_review_info()
write_to_csv()


