import requests
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import json
from time import sleep, time
from random import randint, randrange, choice
import lxml
import sentry_sdk

from bs4 import BeautifulSoup as bs4

from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


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

    def findPage(self, retailer):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=options)

        timeout = 10

        #-------AMAZON-------#
        #--------------------#
        retailer = retailer['Amazon']
        if retailer:
            #Seach XPath: //*[@id="twotabsearchtextbox"]
            driver.get(retailer['url'])
            searchBox = driver.find_element("xpath", '//*[@id="twotabsearchtextbox"]')
            searchBox.clear()
            searchBox.send_keys(self.productName)
            searchBox.send_keys(Keys.ENTER)

            count = 3
            loader = 0
            elementXPath = f"/ html / body / div[1] / div[1] / div[1] / div[1] / div / span[1] / div[1] / div[{count}]"

            while loader < 1:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))
                loader = 1

            #Temporary List that hold a simple dictionary link:price
            #At the end will be used to return the lowest price link
            productList = []

            while count != 7:
                #Click on specific product link XPath
                try:
                    productLinkXpath = f'/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a'
                    productLink = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{productLinkXpath}')))
                    productLinkHref = productLink.get_attribute('href')
                    productLinkHref = productLinkHref[0:].replace(" ", "")
                    productList.append(productLinkHref)
                except:
                    pass
                count += 1


            #Loop through the temporary list of links and get the price
            tempList = []
            r = bs4(driver.page_source, 'lxml')

            priceClassName = 'a-price-whole'
            decimalClassName = 'a-price-fraction'
            whole = r.find('span', {'class': priceClassName}).text
            decimal = r.find('span', {'class': decimalClassName}).text
            price = f"{whole}{decimal}"

            #return {'Link': driver.current_url, 'Retailer': 'Amazon', 'Price': price}

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



