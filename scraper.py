from selenium import webdriver
import time
import pandas as pd
import sqlite3

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--start-maximized")


url = "https://www.hangseng.com/en-hk/e-valuation/address-search/"
driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 1024)
driver.get(url)


path = '//span[@class = "select2-selection select2-selection--single"]'

areas_li = []
districts_li = []
estates_li = []

element = driver.find_elements_by_xpath('//span[@class="rvp_subtitle"]')
driver.execute_script("arguments[0].scrollIntoView()", element[1])


driver.find_elements_by_xpath(path)[0].click()
areas = [i.text for i in driver.find_elements_by_xpath('//li[@class="select2-results__option"]')]

for i in range(len(areas)):

    if i is not 0:
        driver.find_elements_by_xpath(path)[0].click()

    # print(f"Area: {areas[i]}")
    driver.find_elements_by_xpath('//li[@class="select2-results__option"]')[i].click()
    time.sleep(3)
    driver.find_elements_by_xpath(path)[1].click()
    districts = [i.text for i in driver.find_elements_by_xpath('//li[@class="select2-results__option"]')]
    #print(f"Districts under {areas[i]}: ")

    for j in range(len(districts)):
        #print(districts[j])

        if j is not 0:
            driver.find_elements_by_xpath(path)[1].click()

        driver.find_elements_by_xpath('//li[@class="select2-results__option"]')[j].click()
        time.sleep(3)
        driver.find_elements_by_xpath(path)[2].click()
        estates = [i.text for i in driver.find_elements_by_xpath('//li[@class="select2-results__option"]')]
        #print(f"Estates under {districts[j]}: ")

        for k in range(len(estates)):
            #print(estates[k])
            areas_li.append(areas[i])
            districts_li.append(districts[j])
            estates_li.append(estates[k])

            print(areas[i] + ', ' + districts[j] + ', ' + estates[k])

df = pd.DataFrame()
df["Area"] = areas_li
df["District"] = districts_li
df["Estate"] = estates_li


print('Data successfully scraped')

conn = sqlite3.connect('data.sqlite')
df.to_sql('data', conn, if_exists='replace')

print('Db successfully constructed and saved')

time.sleep(5)
driver.close()
conn.close()
