from string import ascii_letters, whitespace
import requests
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import json

from bs4 import BeautifulSoup as bs4

from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from random import choice, random
import time


# Create session object
session = requests.Session()
# Create an HTTP adapter that uses a pool of proxy IPs
adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50)
session.mount('https://', adapter)

# User-Agent strings pool
user_agent = UserAgent()


class getProductLink:
    # Create session object
    session = requests.Session()
    # Create an HTTP adapter that uses a pool of proxy IPs
    adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50)
    session.mount('https://', adapter)

    # User-Agent strings pool
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random,
               'Origin': 'https://www.google.com', 'Referer': 'https://www.google.com'}

    def __init__(self, productName, category):
        self.productName = productName
        self.category = category
        self.links = []

    def __validRetailers(self):
        with open('stores.json', 'r') as f:
            retailers = json.load(f)
            valid = [x for x in retailers if self.category in x['products'] or x['products'] == 'all']
            return valid

    def __findPage(self, retailer):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        timeout = 10

        if retailer['name'] == "Amazon":
            #Seach XPath: //*[@id="twotabsearchtextbox"]
            searchBox = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
            searchBox.clear()
            searchBox.send_keys(self.productName)
            searchBox.send_keys(Keys.ENTER)

            count = 1
            loader = 0
            elementXPath = f"/ html / body / div[1] / div[1] / div[1] / div[1] / div / span[1] / div[1] / div[{count}]"

            while count < 1:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))
                loader = 1

            while count != 15:
                #Click on specific product link XPath: /html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[4]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a
                productLink = driver.find_element_by_xpath(f'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a')
                productLink.click()
                priceXPath = '/html/body/div[2]/div[2]/div[6]/div[4]/div[5]/div[14]/div[1]/div/table/tbody/tr[2]/td[2]/span[1]'
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))




        elif retailer['name'] == "Currys":
            pass
        elif retailer['name'] == "Argos":
            pass
        elif retailer['name'] == "John Lewis":
            pass
        elif retailer['name'] == "Apple":
            pass
        elif retailer['name'] == "Samsung":
            pass
        elif retailer['name'] == "Dell":
            pass
        elif retailer['name'] == "Asus":
            pass
        elif retailer['name'] == "Very":
            pass
        elif retailer['name'] == "Microsoft Store":
            pass



    def __getLinks(self, retailer):
        retailers = self.__validRetailers()

