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
    def __init__(self, productName, category):
        self.productName = productName
        self.category = category
        self.lowestPrices = []  # Stack structure
        self.lowestPriceLink = ''
        self.lowestPriceRetailer = ''
        self.lowestPrice = 0

        # Create session object
        session = requests.Session()
        # Create an HTTP adapter that uses a pool of proxy IPs
        adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50)
        session.mount('https://', adapter)

        # User-Agent strings pool
        user_agent = UserAgent()
        self.headers = {'User-Agent': user_agent.random,
                   'Origin': 'https://www.google.com', 'Referer': 'https://www.google.com'}

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

        #-------AMAZON-------#
        #--------------------#
        if retailer['name'] == "Amazon":
            page = session.get(retailer['url'], headers=self.headers)

            for cookie in page.cookies:
                driver.add_cookie({
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': '/',
                    'domain': cookie.domain,
                })

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

            #Temporary List that hold a simple dictionary link:price
            #At the end will be used to return the lowest price link
            tempList = []

            while count != 15:
                #Click on specific product link XPath: /html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[4]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a
                productLink = driver.find_element_by_xpath(f'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a')
                productLink.click()
                priceXPath = '/html/body/div[2]/div[2]/div[6]/div[4]/div[5]/div[14]/div[1]/div/table/tbody/tr[2]/td[2]/span[1]'
                price = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))
                try:
                    price = price.innerText
                except:
                    price = price.text

                if len(tempList) == 0:
                    tempList.append({'link': driver.current_url, 'price': price})
                else:
                    if tempList[0]['price'] > price:
                        tempList.pop()
                        tempList.append({'link': driver.current_url, 'price': price})
                count += 1

            if len(self.lowestPrices) == 0:
                self.lowestPrices.append(tempList[0])
            else:
                if self.lowestPrices[0]['price'] > tempList[0]['price']:
                    self.lowestPrices.pop()
                    self.lowestPrices.append(tempList[0])
        #--------------------#
        #--------------------#


        #-------Currys-------#
        #--------------------#
        elif retailer['name'] == "Currys":
            pass
        #--------------------#
        #--------------------#


        #-------Argos-------#
        #--------------------#
        elif retailer['name'] == "Argos":
            pass
        #--------------------#
        #--------------------#

        #-------John Lewis-------#
        #------------------------#
        elif retailer['name'] == "John Lewis":
            pass
        #------------------------#
        #------------------------#

        #-------Apple-------#
        #-------------------#
        elif retailer['name'] == "Apple":
            pass
        #-------------------#
        #-------------------#

        #-------Samsung-------#
        #---------------------#
        elif retailer['name'] == "Samsung":
            pass
        #---------------------#
        #---------------------#

        #-------Dell-------#
        #------------------#
        elif retailer['name'] == "Dell":
            pass
        #------------------#
        #------------------#

        #-------Asus-------#
        #------------------#
        elif retailer['name'] == "Asus":
            pass
        #------------------#
        #------------------#

        #-------Very-------#
        #------------------#
        elif retailer['name'] == "Very":
            pass
        #------------------#
        #------------------#

        #-------Microsoft Store-------#
        #------------------------------#
        elif retailer['name'] == "Microsoft Store":
            pass
        #------------------------------#
        #------------------------------#

    def __sortPrices(self, retailer):
        retailers = self.__validRetailers()
        for retailer in retailers:
            self.__findPage(retailer)
            
    def getPublic(self):
        return {'Link': self.lowestPriceLink, 'Retailer': self.lowestPriceRetailer, 'Price': self.lowestPrice}



