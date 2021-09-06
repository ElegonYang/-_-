from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import *
import pandas as pd

opt = Options()
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
opt.add_argument("user-agent={}".format(ua))
no_image_mode = {'profile.default_content_setting_values': {'images': 2}}
opt.add_argument('--headless')
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

res_level_list = []
res_review_count_list = []


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


def res_star_review_count():
    for res_url in res_15_in_page_list:
        driver.get(res_url)
        # 餐廳星等 class
        res_level_class = driver.find_elements(By.CSS_SELECTOR,
                                               "div[class='jsx-307016528 count-outer'] div[class='jsx-1207467136 text']")
        # 餐廳評論數 class
        res_review_count_class = driver.find_elements(By.CSS_SELECTOR,
                                                      "a[class='jsx-307016528'] span[class='jsx-307016528 count']")
        # 無評價/星等 設置
        if not res_level_class:
            res_level_list.append("查無評價")
        if not res_review_count_class:
            res_review_count_list.append('無評論')
        # 濾出餐廳星等 加入清單
        for level_text in res_level_class:
            level = level_text.text
            res_level_list.append(level)
        # 濾出餐廳評論數 加入清單
        for review_text in res_review_count_class:
            review = review_text.text
            res_review_count_list.append(review)


def write_to_csv():
    all_info = {"餐廳星等": res_level_list, "餐廳評價數": res_review_count_list}

    df1 = pd.DataFrame.from_dict(all_info, dtype=object)
    df1.to_csv('愛食客_星等_評論數.csv', encoding='utf_8_sig', index=False)


page_set()
res_star_review_count()
write_to_csv()