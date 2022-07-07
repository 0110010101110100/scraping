#API loopy loop


# pip install selenium helium bs4 chromedriver-autoinstaller

import chromedriver_autoinstaller
from selenium import webdriver
from helium import *
from bs4 import BeautifulSoup as bs

website = 'https://federalreporter.nih.gov/projects/search/?searchId=0bb52e7dda404e9895dc325274ec689a&searchMode=Smart&resultType=projects&filters='

driver = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(driver)
set_driver(driver)

go_to(website)

sc = driver.page_source
sp = bs(sc, 'html.parser')

# Get total of pages
total = sp.find(class_='pagination-total').text
total = total.replace(',', '')
total = int(total)

# Switch pages
n = 1
while n <= total:
    print(f"Page {n}:")
    print('----------')
    
    write(n, into=S('//*[@id="pagination-top"]/div/label/input'))
    press(ENTER)

    #wait_until(Text('Loading, please wait...').exists)
    wait_until(lambda: not Text('Loading, please wait...').exists(), timeout_secs=60, interval_secs=0.1)

    # Get data
    sc = driver.page_source
    sp = bs(sc, 'html.parser')

    contents = sp.find_all(class_='content-row')
    for x in contents:
        print(f"Agency: {x.td.contents[0]}")
        print(f"Organization: {x.find('td', {'data-label':'Organization'}).text}")

        print()
    
    n += 1
    