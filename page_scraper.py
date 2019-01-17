import selenium

# Using Chrome to access web
from selenium import webdriver

import time
import pandas as pd
import html5lib

driver = webdriver.Chrome()

time.sleep(2)

# Open the website
driver.get('http://timetable.ncirl.ie/SWS/1819/default.aspx')

# select department dropdown
driver.find_element_by_xpath("//select[@name='dlFilter2']/option[text()='School of Computing']").click()

id_tWildcard = driver.find_element_by_id('tWildcard')
id_tWildcard.send_keys('Msc in Data Analytics')
id_bWildcard = driver.find_element_by_id('bWildcard')
id_bWildcard.click();
time.sleep(2)

driver.find_element_by_xpath("//select[@name='dlObject']/option[text()='MSc in Data Analytics 1 Sept 2018 (MSCDAD_A) - Group A - Technical Stream']").click()

#driver.find_element_by_xpath("//select[@name='lbWeeks']/option[text()='This Week']").click()
driver.find_element_by_xpath("//select[@name='lbWeeks']/option[text()='Programmes Commencing September 2018 - Semester 2']").click()

id_bGetTimetable = driver.find_element_by_id('bGetTimetable')
id_bGetTimetable.click()

windows = driver.window_handles
time.sleep(3)
driver.switch_to.window(windows[1])

tbl = driver.find_element_by_xpath("//html/body/table[2]").get_attribute('outerHTML')

driver.close()
driver.quit()

#print(tbl)
df = pd.read_html(tbl)
df = df[0]
print(df)
df = df.drop([1], axis=1)
df = df.set_index([0])
df.columns = df.iloc[0]
df = df.iloc[1:]

df =  df.dropna(axis=0, how='all')
print(df)

if df.empty:
    print('DataFrame is empty!')

