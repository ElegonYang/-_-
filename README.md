# 目標網站:愛食客 
## 爬取全台灣的餐廳資訊 包含 名稱/地址/電話/評價星等/評論次數/評論內容
## 使用的環境是python 3.6版本等相關套件


</a> <a href="https://www.selenium.dev" target="_blank"> <img src="https://raw.githubusercontent.com/detain/svg-logos/780f25886640cef088af994181646db2f6b1a3f8/svg/selenium-logo.svg" alt="selenium" width="40" height="40"/>   </a>

^^他叫做selenium

這是一個瀏覽器自動化操作的工具 可用程式碼控制瀏覽器的運作以及擷取相關資訊  

其中 有兩個我們會用到的功能

**selenium.webdriver.chrome.options**  
**selenium.webdriver.common.by**  

**option**// 可以讓我們載入一些設定 比如說不會顯示視窗的"無頭模式"或是禁止顯示網頁內圖片的相關設定  
**by**    //可透過 xpath 或是 css選擇器對需要的資訊進行鎖定!  

20210922 update

selenium需要配合的是google chromedriver.exe 網路上搜尋即可找到!

20211008 update

全面改用class寫法 設置入口 讓可讀性upup!
