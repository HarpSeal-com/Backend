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
        self.links = []  # Stack structure
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
        with open('api/stores.json', 'r') as f:
            retailers = json.load(f)
            validRetailers = []
            
            for key, value in retailers.items():
                if self.category in value["products"] or value["products"] == "all":
                    validRetailers.append({key: value})

            return validRetailers

    def findPage(self) -> None:
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

        driver = webdriver.Chrome(options=options)
        timeout = 10

        retailers = self.__validRetailers()

        #-------AMAZON-------#
        #--------------------#

        for retailer in retailers:

            if retailer.get('Amazon'):
                #Seach XPath: //*[@id="twotabsearchtextbox"]
                url = retailer['Amazon']['url']
                url = url.replace("-placeholder-", f"{self.productName}")
                driver.get(url)

                count = 1
                elementXPath = f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]'
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))
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
                        productsList.append({'Link': f"https://www.amazon.co.uk{product}", 'Retailer': retailer, 'Price': price})
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


            #-------Currys-------#
            #--------------------#
            elif retailer.get('Currys'):
                url = retailer['Currys']['url']
                productNameArr = self.productName.split(" ")
                url = f"{url}{productNameArr[0]}&20{'%20'.join(productNameArr[1:])}"
                driver.get(url)

                count = 1
                elementXPath = f'//*[@id="hash-10236204"]'
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, f'{elementXPath}')))

                content = driver.page_source
                soup = bs4(content, 'lxml')

                # Use bs4 to get product links
                productList = []
                try:
                    products = soup.find_all("a", class_="link text-truncate pdpLink")
                except Exception as e:
                    print("Currys could not find products")

                for product in products:
                    if (((self.productName in product.text) or (self.productName.lower() in product.text.lower()) or (
                        "+".join(self.productName.split(" ")) in product.text)) and (
                        ("case" not in product.text.lower())
                        and ("protector" not in product.text.lower()) and ("cover" not in product.text.lower()))
                        and ("screen" not in product.text.lower()) and ("film" not in product.text.lower())):

                        productList.append(product.get('href'))

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


            #-------Argos-------#
            #--------------------#
            elif retailer.get('Argos'):
                pass
            #--------------------#
            #--------------------#

            #-------John Lewis-------#
            #------------------------#
            elif retailer.get('John Lewis'):
                pass
            #------------------------#
            #------------------------#

            #-------Apple-------#
            #-------------------#
            elif retailer.get('Apple'):
                pass
            #-------------------#
            #-------------------#

            #-------Samsung-------#
            #---------------------#
            elif retailer.get('Samsung'):
                pass
            #---------------------#
            #---------------------#

            #-------Dell-------#
            #------------------#
            elif retailer.get('Dell'):
                pass
            #------------------#
            #------------------#

            #-------Asus-------#
            #------------------#
            elif retailer.get('Asus'):
                pass
            #------------------#
            #------------------#

            #-------Very-------#
            #------------------#
            elif retailer.get('Very'):
                pass
            #------------------#
            #------------------#

            #-------Microsoft Store-------#
            #------------------------------#
            elif retailer.get('Microsoft Store'):
                pass
            #------------------------------#
            #------------------------------#

    def __sortPrices(self, retailer):
        retailers = self.__validRetailers()
        for retailer in retailers:
            self.__findPage(retailer)

    def getPublic(self):
        self.findPage()
        try:
            lowestPriceLink = self.links[0]['Link']
            lowestPriceRetailer = self.links[0]['Retailer']
            lowestPrice = self.links[0]['Price']
            return {'Link': lowestPriceLink, 'Retailer': lowestPriceRetailer, 'Price': lowestPrice}
        except IndexError:
            raise IndexError
        pass



