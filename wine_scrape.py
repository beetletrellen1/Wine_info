import pandas as pd
import numpy as np
import requests
from selenium import webdriver
import time

# delete this for GITHUB submission
EMAIL = 'EMAIL'
PASSWORD = 'PASSWORD'

# Using Selenium to scrape winespectator.com
driver = webdriver.Chrome(executable_path='./chromedriver')
url = "https://www.winespectator.com/auth/login?returnpage=https://www.winespectator.com/wine/search"
driver.get(url)

email_field = driver.find_element_by_id('userid')

email_field.send_keys(EMAIL)

password_field = driver.find_element_by_id('passwd')

password_field.send_keys(PASSWORD)

login_btn = driver.find_element_by_id('target')
login_btn.click()

# saving to a list for future csv
wines = []
for page in range(1, 30000):
    search_url = "https://www.winespectator.com/wine/detail/source/search/note_id/{}".format(page)
    driver.get(search_url)
    # Empty dictionary to store data
    wine = {}
    # Winery/Vineyard
    wine['Winery']  = driver.find_elements_by_tag_name("h1")[1].text
    # Wine + Year. Kept year on the end of most because not all Wine names will hold the year
    wine['Wine']    = driver.find_elements_by_tag_name("h4")[0].text
    # Year pulled from wine name.  May produce part of words for wines that don't have years attached
    wine['Year']    = driver.find_elements_by_tag_name("h4")[0].text[-4:]
    # Wine Spectator's Score
    wine['Score']   = driver.find_element_by_tag_name("h5").text[7:]
    # R_Price = Region Price or the price sold for this specific wine
    wine['R_Price'] = driver.find_elements_by_xpath("//div[@class='paragraph']")[0].text[14:]
    # The country of origin
    wine['Country'] = driver.find_elements_by_xpath("//div[@class='paragraph']")[1].text[8:]
    # Region of origin
    wine['Region']  = driver.find_elements_by_xpath("//div[@class='paragraph']")[2].text[7:]
    # How the wine was released to the public
    wine['Issue']   = driver.find_elements_by_xpath("//div[@class='paragraph']")[3].text[6:]
    # Tasting Notes
    wine['Notes']   = driver.find_elements_by_xpath("//div[@class='paragraph']")[4].text
    # Add wine dictionary to the list
    wines.append(wine)
    time.sleep(2)
    # to check every 1001 iterations that it is working.
    if page % 1001 == 0:
        print("{}th url".format(page), search_url)
# Writing to a pandas data frame so that I can quickly and easily convert to csv and read it later.
wine_data = pd.DataFrame(wines)

wine_data.to_csv('wine_data.csv')

# Always good to close your work.
driver.close()
