import pandas as pd

# 讀取抓完的資料csv檔案
res_name = pd.read_csv(r'C:\Users\Student\Desktop\py\res_division\愛食客_餐廳名稱.csv', encoding='utf-8')
res_tel = pd.read_csv(r'C:\Users\Student\Desktop\py\res_division\愛食客_餐廳電話.csv', encoding='utf-8')
res_address_area = pd.read_csv(r'C:\Users\Student\Desktop\py\res_division\愛食客_餐廳地址_區域.csv', encoding='utf-8')
res_star_review_count = pd.read_csv(r'C:\Users\Student\Desktop\py\res_division\愛食客_星等_評論數.csv', encoding='utf-8')

# 生成合併檔案
final_file = [res_name, res_tel, res_address_area, res_star_review_count]
outfile = pd.concat(final_file, axis=1)
outfile.to_csv(r'C:\Users\Student\Desktop\py\res_division\res_all_info.csv', index=False, encoding='utf-8')
