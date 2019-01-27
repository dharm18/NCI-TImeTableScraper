import selenium

# Using Chrome to access web
from selenium import webdriver

import time
import pandas as pd
import html5lib
from bs4 import BeautifulSoup

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

soup = BeautifulSoup(tbl, "html.parser")

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

# different approaches to parse 90's style page layout

for table in soup.find_all('table'):
    for subtable in table.find_all('table'):
        print(subtable)

data = []
headers = []

for index, row in enumerate(soup.find_all('tr')):
    if index == 0:
        # this is a header
        headers.append(row.find_all('td'))
        # data.append([])
    else:
        # this is not a header, therefore is data under the last header seen
        data.append(row.find_all('td'))
print(headers)
print(data)

headers_data = []
for index, head in enumerate(headers):
    print(index)
    print(head)
    for index, head_title in enumerate(head):
        print(head_title.text)
        headers_data.append(head_title.text)

timetable_data = []
t_data = []
for index, dt in enumerate(data):
    print(index)
    print(dt)
    for index1, dt_title in enumerate(dt):
        print(index1)
        print(dt_title.text)
        t_data.append(dt_title.text)

    timetable_data.append(t_data)
    t_data = []

