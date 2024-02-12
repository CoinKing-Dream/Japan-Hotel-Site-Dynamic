from bs4 import BeautifulSoup
import requests
import os, os.path, csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re

def main():
    
    print(f'Start ---> {datetime.now().strftime("%H:%M:%S")}')
    
    product_dataset = {
        'No.':[],
        '取得日':[],
        '会社名': [],
        '会社所在地': [],
        '施設名称': [],
        '施設所在地（勤務地)': [],
        'URL': [],
        '抽出元URL': [],
    }

    my_dataset = pd.DataFrame(product_dataset)
        
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"]) 
        # options.add_argument('--headless=new')
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()

        wait = WebDriverWait(browser, 30)
        
        starturl = "https://www.hotelkyujin.com/"
        print(f"Start ---> {datetime.now().time()}")

        browser.get(starturl)
    except Exception as e:
        print({e})
    
    browser.implicitly_wait(100)
    
    try:
        detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="topSearch"]/div/form/div[2]/div/button/div/div[1]/span[3]')))
        detail_button.click()
    except Exception as e:
        print({e})
    
    no = 0
    current_date = datetime.now().strftime('%Y/%m/%d')
    item_no = 0
    prev_data_url = ""
    
        
    while True:
        
        item_no = item_no + 1
        
        try:
            post_sections = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/section[2]/div/div[2]/div[{item_no}]')))
            browser.execute_script("arguments[0].scrollIntoView();", post_sections)
            
            if post_sections.get_attribute("class").strip() != "search-results-item jobs-card":
                continue
            
            btn = post_sections.find_element(By.XPATH, ".//article/header/a")
            data_url = btn.get_attribute("href")
            
            response = requests.get(data_url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = soup.find("article").find_all("section")[1].find("table").find_all("tr")
        except Exception as e:
            print({e})
        
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # new_height = browser.execute_script("return document.body.scrollHeight")
        
        # if new_height == last_height:
        #     break
        
        # last_height = new_height
        # print(last_height)
        
        no = no + 1
        
        temp_data = data[1].find("td").get_text().strip()
        clean_data = re.sub(r'\s+', ' ', str(temp_data))
        currnet_company_location = re.sub(r'<br>|</br>', '', clean_data).strip()
        currnet_company_location = re.sub(r'〒\s\d+-\d+\s', '', currnet_company_location).strip()
        
        temp_data = data[3].find("td").get_text().strip()
        clean_data = re.sub(r'\s+', ' ', str(temp_data))
        current_facility_location = re.sub(r'<br>|</br>', '', clean_data).strip()
        current_facility_location = re.sub(r'〒\s\d+-\d+\s', '', current_facility_location).strip()
        # time.sleep(500)
        current_company_name = data[0].find("td").get_text().strip()
        current_facility_name = data[2].find("td").get_text().strip()
        currnet_URL = data[10].find("td").get_text().strip()
                
        my_dataset.at[no - 1, 'No.'] =                int(no)
        my_dataset.at[no - 1, '取得日'] =              current_date
        my_dataset.at[no - 1, '会社名'] =              current_company_name
        my_dataset.at[no - 1, '会社所在地'] =          currnet_company_location
        my_dataset.at[no - 1, '施設名称'] =            current_facility_name
        my_dataset.at[no - 1, '施設所在地（勤務地)'] =  current_facility_location
        my_dataset.at[no - 1, 'URL'] =                currnet_URL
        my_dataset.at[no - 1, '抽出元URL'] =           data_url
        
        if prev_data_url == data_url:
            break
        
        prev_data_url = data_url
        
        
        my_dataset.to_csv(f'result.csv', index=False)
   
# Start scraping
if __name__ == "__main__":
    main()
    print(f'End ---> {datetime.now().strftime("%H:%M:%S")}')
