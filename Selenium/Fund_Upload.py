"""""
Mac os環境
1.抓取鉅亨網債券數據並下載(https://fund.cnyes.com/Fixedincome/search.aspx)
２.安裝以下package
pandas(pip install pandas) for data analysis
selenium(pip install selenium) for webdriver
bs4(pip install bs4) for 提取HTML或XML檔案中資料
lxml(pip install lxml) for BeautifulSoup 的解析器（Parser）
"""

import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://fund.cnyes.com/Fixedincome/search.aspx'

driver = webdriver.Chrome(executable_path='/Users/jocelyn/chromedriver')

driver.get(url)
#指定計價幣別(美元)
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DD_classCurrent"]').click()
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DD_classCurrent"]/option[7]').click()

#指定投資區域（全球市場）
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DropDownList1"]').click()
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DropDownList1"]/option[8]').click()

#指定基金組別（全球債券）
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DropDownList2"]').click()
driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_DropDownList2"]/option[4]').click()

#指定年化配息率（3% - 5%）
driver.find_element("xpath", '//*[@id="aspnetForm"]/div[4]/div[1]/select[1]').click()
driver.find_element("xpath", '//*[@id="aspnetForm"]/div[4]/div[1]/select[1]/option[5]').click() 
driver.find_element("xpath", '//*[@id="aspnetForm"]/div[4]/div[1]/select[2]').click()
driver.find_element("xpath", '//*[@id="aspnetForm"]/div[4]/div[1]/select[2]/option[2]').click()

# 指定配息頻率(每月)
driver.find_element("xpath", '//*[@id="div_type"]').click()
driver.find_element("xpath", '//*[@id="div_type"]/option[4]').click()

# 搜尋後下載
driver.find_element("xpath", '//*[@id="aspnetForm"]/div[4]/div[3]/button').click()

time.sleep(5)
 
# 一年績效排序
driver.find_element("xpath", '/html/body/div[2]/section[3]/div/div[4]/table[2]/thead/tr/th[3]/select').click()
driver.find_element("xpath", '/html/body/div[2]/section[3]/div/div[4]/table[2]/thead/tr/th[3]/select/option[5]').click()
time.sleep(5)
 
html_source = driver.page_source
driver.quit()

soup = BeautifulSoup(html_source, 'lxml')

fund_dict = {
    '基金名稱': [],
    '淨值': [],
    '一年績效': [],
    '配息日': [],
    '配息金額': [],
    '年化配息率': [],
    '連結': []
}
 
for tr in soup.select_one('tbody').select('tr'):  
         
        fund_dict['基金名稱'].append(tr.select('td')[0].text.strip())
        fund_dict['淨值'].append(tr.select('td')[1].text.strip().split('\n')[0])
        fund_dict['一年績效'].append(tr.select('td')[2].text.strip())
        fund_dict['配息日'].append(tr.select('td')[3].text.strip().split('\n')[-1].strip())
        fund_dict['配息金額'].append(tr.select('td')[4].text.strip().split('\n')[0].strip())
        fund_dict['年化配息率'].append(tr.select('td')[4].text.strip().split('\n')[-1].strip())
        fund_dict['連結'].append('https://fund.cnyes.com' + tr.select('td')[0].a['href'].strip().replace(' ', '%20'))
        time.sleep(8)

print(fund_dict)
df = pd.DataFrame(fund_dict)
df.set_index('基金名稱', inplace=True)
print(df)

date = datetime.today().strftime("%Y%m%d")
file_name = '{}_全球債券基金.csv'.format(date)
df.to_csv(file_name, encoding='utf_8_sig')