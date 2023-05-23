# This file opens a connection to storyweaver and downloads the name of all the available languages on the website.
from bs4 import BeautifulSoup
import requests
import time
import json

# selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

options = FirefoxOptions()
options.add_argument('--headless')

URL = "https://storyweaver.org.in/stories"
file_populated = False
trial_number = 0

OUTPUT_PATH = "../../../data/raw/pratham-books-storyweaver/"

while not file_populated:
    trial_number += 1
    print("Instantiating driver #", trial_number)
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    time.sleep(5)
    res = driver.page_source

    soup = BeautifulSoup(res, "html.parser")
    mydivs = soup.find_all("a", class_='pb-link')
    element_index = -1
    for i in range(len(mydivs)):
        if "languages" in mydivs[i].text.lower():
            element_index = i
            break

    if element_index > 0:
        driver.find_elements(by=By.TAG_NAME, value="a")[element_index].click()
        time.sleep(1)
        res = driver.page_source
        soup = BeautifulSoup(res, "html.parser")
        mydivs = soup.find_all("div", class_='pb-checkbox')
        f = open(OUTPUT_PATH + "languages.txt","w")
        for div in mydivs:
            if 'Acholi' in div.text:
                file_populated = True
                print("Success")
            f.write(div.text + "\n")
        f.close()
    driver.close()
    print("Closing driver #", trial_number)
