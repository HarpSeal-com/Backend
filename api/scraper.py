import requests
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import json
from time import sleep, time
from random import randint, randrange, choice
import asyncio
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
        self.links = []  # Stack structure

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
        with open('api/stores.json', 'r') as f:
            retailers = json.load(f)
            validRetailers = {}
            
            for key, value in retailers.items():
                if self.category in value["products"] or value["products"] == "all":
                    validRetailers[key] = value

            return validRetailers

    def findPageAmazon(self, retailer) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--sdisable-dev-shm-usage")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-extensions")

        driver = uc.Chrome(options=options)
        timeout = 15

        #-------AMAZON-------#
        #--------------------#

        #Seach XPath: //*[@id="twotabsearchtextbox"]
        url = retailer['url']
        url = url.replace("-placeholder-", f"{self.productName}")
        driver.get(url)

        count = 1
        elementXPath = f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]'
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))

        content = driver.page_source
        soup = bs4(content, 'lxml')

        # Use bs4 to get product links
        productList = []
        try:
            products = soup.find_all("a", class_="a-link-normal")
        except Exception as e:
            products = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

        temp = 0 
        for product in products:
            if temp == 0:
                temp += 1
                continue
            if ((self.productName in product.text) or (self.productName.lower() in product.text.lower()) or (
            "+".join(self.productName.split(" ")) in product.text) and (
            ("case" not in product.text.lower())
            and ("protector" not in product.text.lower()) and ("cover" not in product.text.lower()))
            and ("screen" not in product.text.lower()) and ("film" not in product.text.lower())):

                productList.append(product.get('href'))

        # Use bs4 to get product prices after selenium gets page link
        productsList = []
        for product in productList:
            try:
                driver.get(f"https://www.amazon.co.uk{product}")
            except Exception as e:
                driver.quit()
                driver = webdriver.Chrome(options=options)
                driver.get(f"https://www.amazon.co.uk{product}")

            content = driver.page_source
            soup = bs4(content, 'lxml')
            
            price = soup.find("span", class_="a-offscreen").text
            try:
                price = float(price.replace("£", ""))
                if price > 50.50:
                    productsList.append({'Link': f"https://www.amazon.co.uk{product}", 'Retailer': retailer, 'Price': price})
                else:
                    continue
            except ValueError:
                pass
            except Exception as e:
                print(e)

        for product in productsList:
            if self.links:
                if product['Price'] < self.links[0]['Price']:
                    self.links.pop()
                    self.links.append(product)
            else:
                self.links.append(product)            
            
    #--------------------#
    #--------------------#


    def findPageCurrys(self, retailer):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--sdisable-dev-shm-usage")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-extensions")


        driver = uc.Chrome(options=options)
        timeout = 15

        #-------Currys-------#
        #--------------------#
        url = retailer['url']
        productNameArr = self.productName.split(" ")
        newUrl = f"{url}{productNameArr[0]}%20{'%20'.join(productNameArr[1:])}"
        driver.get(newUrl)

        #element_present = EC.presence_of_element_located((By.CLASS_NAME, 'container search-results has-products'))
        #WebDriverWait(driver, timeout).until(element_present)

        content = driver.page_source
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(content)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        soup = bs4(content, 'lxml')

        # Use bs4 to get product links
        productList = []
        try:
            products = soup.find_all("a", class_="link text-truncate pdpLink")
            products = [product.get('href') for product in products]
        except Exception as e:
            products = soup.find_all("a", class_="link click-beacon")
            # replace each element with its href
            products = [product.get('href') for product in products]

        for product in products:
            if ((self.productName in product) or (self.productName.lower() in product) or (
                "+".join(self.productName.split(" ")) in product)) and (
                ("case" not in product)
                and ("protector" not in product) and ("cover" not in product)
                and ("screen" not in product) and ("film" not in product)):

                productList.append(product)

        # Use bs4 to get product prices after selenium gets page link
        productsList = []
        for product in productList:
            try:
                driver.get(f"https://www.currys.co.uk/{product}")
            except Exception as e:
                driver.quit()
                driver = webdriver.Chrome(options=options)
                driver.get(f"https://www.currys.co.uk/{product}")

            content = driver.page_source
            soup = bs4(content, 'lxml')
            
            try:
                price = soup.find("span", class_="value").text[1:]
                price = float(price)
                if price > 50.50:
                    productsList.append({'Link': f"https://www.currys.co.uk/{product}", 'Retailer': retailer, 'Price': price})
                else:
                    continue
            except Exception as e:
                print("Currys could not find price")
                continue

        for product in productsList:
            if self.links:
                if product['Price'] < self.links[0]['Price']:
                    self.links.pop()
                    self.links.append(product)
            else:
                self.links.append(product)            

    #--------------------#
    #--------------------#
    
    def findPageArgos(self, retailer):
            pass
    

    def findPageJohnLewis(self, retailer):
            pass
    
    
    def findPageVery(self, retailer):
            pass
    

    def getPublic(self):
        retailers = self.__validRetailers()

        self.findPageCurrys(retailers['Currys'])

        lowestPriceLink = self.links[0]['Link']
        lowestPriceRetailer = self.links[0]['Retailer']
        lowestPrice = self.links[0]['Price']
        return {'Link': lowestPriceLink, 'Retailer': lowestPriceRetailer, 'Price': lowestPrice}

