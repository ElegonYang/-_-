from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import *
import pandas as pd

opt = Options()
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
opt.add_argument("user-agent={}".format(ua))
no_image_mode = {'profile.default_content_setting_values': {'images': 2}}
opt.add_experimental_option('prefs', no_image_mode)
opt.add_argument('--headless')
driver = webdriver.Chrome("chromedriver.exe", chrome_options=opt)

city_key = ["台北市", '基隆市', '新竹市', '嘉義市', '宜蘭縣', '新竹縣', '苗栗縣',
            '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '花蓮縣', '臺東縣',
            '花蓮縣', '澎湖縣', '臺北市', '新北市', '桃園市', '臺中市', '臺南市',
            '高雄市']

test_city_key = ['台北市']

home_page_url = "https://ifoodie.tw/explore/"
page_url = '/list?page='

res_tel_list = []
res_15_in_page_list = []


def page_set():
    for city in city_key:
    # for city in test_city_key:
        # for page in range(1, 2):
        for page in range(1, 68):
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


def res_tel_get():
    for res_url in res_15_in_page_list:
        driver.get(res_url)
        res_tel_class = driver.find_elements(By.CSS_SELECTOR,
                                             "span[class='jsx-1692663080 detail'] a[class='jsx-1692663080']")

        if not res_tel_class:
            res_tel_list.append("無電話")
            # 濾出餐廳電話 加入清單
        for res_tel_text in res_tel_class:
            res_tel = res_tel_text.text
            res_tel_list.append(res_tel)


def write_to_csv():
    all_info = {"餐廳電話": res_tel_list}

    df1 = pd.DataFrame.from_dict(all_info, dtype=object)
    df1.to_csv('愛食客_餐廳電話.csv', encoding='utf_8_sig', index=False)


page_set()
res_tel_get()
write_to_csv()