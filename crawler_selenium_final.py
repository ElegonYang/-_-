from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv


class Selenium:
    # 初始頁面網址
    front_page_url = 'https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list?page='

    # 入口
    def do_step(self):
        # 載入selenium設定 －> 抓取所有餐廳網址 -> 進入單一餐廳頁面找相關資訊 -> 寫入文件
        driver = self._selenium_option()
        all_shop_links = self._get_all_shops_link(driver)
        self._res_page_return(driver, all_shop_links)
        self.test_git()

    @staticmethod
    def _selenium_option():
        # selenium相關設定  headers/不圖取網頁圖片
        opt = Options()
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opt.add_argument("user-agent={}".format(ua))
        opt.add_argument("--blink-settings=imagesEnabled=false")
        # opt.add_argument('--headless')
        driver = webdriver.Chrome("./chromedriver", chrome_options=opt)

        return driver

    @classmethod
    def _get_all_shops_link(cls, driver):
        # 抓取全部餐廳網址
        all_shop_links = []
        # range 為頁數 台北地區共68頁 每頁14間餐廳
        for page in range(1, 2):
            restaurant_page = cls.front_page_url + str(page)
            driver.get(restaurant_page)
            # 抓取餐廳超連結
            restaurant_href_class = driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-3440511973 title'] a[href]")
            # 解析超連結網址
            for res_url in restaurant_href_class:
                res_url_text = res_url.get_attribute('href')
                all_shop_links.append(res_url_text)
        # 刪除list中第一項網址（廣告）
        all_shop_links.pop(0)
        # 回傳全部餐廳網址list
        return all_shop_links

    def _res_page_return(self, driver, all_shop_links):
        # 進入餐廳單一網址後 利用選擇器找出所要資訊並解析（餐廳名/電話/星等/地址/評論內容)
        for solo_res_link in all_shop_links:

            res_name = self._return_res_name(driver, solo_res_link)
            res_tel = self._return_res_tel(driver, solo_res_link)
            res_level = self._return_res_star_level(driver, solo_res_link)
            res_address = self._return_res_address(driver, solo_res_link)
            res_reviews = self._more_btn_check(driver, solo_res_link)
            self._all_result_to_csv(res_name, res_level, res_tel, res_address, res_reviews)

    @staticmethod
    def _return_res_name(driver, solo_res_link):
        # 餐廳名
        driver.get(solo_res_link)
        res_name_class = driver.find_element(By.CSS_SELECTOR, "div[class='jsx-307016528 title-outer'] h1[class='jsx-307016528 title' ] a[class='jsx-307016528']")
        res_name = res_name_class.text

        return res_name

    @staticmethod
    def _return_res_tel(driver, solo_res_link):
        # 餐廳電話存在判斷
        driver.get(solo_res_link)

        try:

            res_tel_class = driver.find_element(By.CSS_SELECTOR, "span[class='jsx-1692663080 detail'] a[class='jsx-1692663080']")
            res_tel = res_tel_class.text

            return res_tel

        except Exception as e:

            return "無電話"

    @staticmethod
    def _return_res_star_level(driver, solo_res_link):
        # 餐聽評價存在判斷
        driver.get(solo_res_link)

        try:
            res_level_class = driver.find_element(By.CSS_SELECTOR, "div[class='jsx-307016528 count-outer'] div[class='jsx-1207467136 text']")
            res_level = res_level_class.text
            return res_level

        except Exception as e:
            return "無評價"

    @staticmethod
    def _return_res_address(driver, solo_res_link):
        # 餐廳地址判斷
        driver.get(solo_res_link)

        try:
            res_address_class = driver.find_element(By.CSS_SELECTOR, "span[class='jsx-1692663080 detail']")
            res_address = res_address_class.text

            return res_address

        except Exception as e:

            return '查無地址'

    @staticmethod
    def _more_btn_check(driver, solo_res_link):
        # 動態載入按鈕確認
        reviews = []
        driver.get(solo_res_link)

        try:
            more_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="jss76 jss50 jss52 jss55 btn-more-checkin"]')

            while more_btn:
                more_btn.click()
                time.sleep(1)

            review_class = driver.find_elements(By.CSS_SELECTOR,
                                                "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")
            for _review in review_class:
                review = _review.text
                reviews.append(review)

            return reviews

        except Exception as e:

            review_class = driver.find_elements(By.CSS_SELECTOR, "div[class='jsx-1937851871 message'] div[class='jsx-1937851871']")

            for _review in review_class:
                review = _review.text
                reviews.append(review)

            return reviews

    @staticmethod
    def _all_result_to_csv(res_name, level, tel, address, reviews):
        # 寫入CSV
        with open('result.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([res_name, level, tel, address, reviews])

    @staticmethod
    def test_git():
        return "test git"


go = Selenium()

if __name__ == '__main__':

    go.do_step()
