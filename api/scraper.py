import requests
import json

from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep, time
from random import randint, randrange, choice
import sentry_sdk

from bs4 import BeautifulSoup as bs4

from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


class getProductLink:
    def __init__(self, productName, category):
        self.productName = productName
        self.category = category
        self.lowestPriceLink = ''
        self.lowestPriceRetailer = ''
        self.lowestPrice = 0

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
        self.__driver = webdriver.Chrome(options=options)

    def __validRetailers(self):
        with open('stores.json', 'r') as f:
            retailers = json.load(f)
            valid = [x for x in retailers if self.category in x['products'] or x['products'] == 'all']
            return valid

    def findPage(self, retailer):

        productNames = self.productName.split(" ")
        # Join product names by a +
        productNames = "+".join(productNames)

        #-------AMAZON-------#
        #--------------------#
        if retailer['Amazon']:
            pass

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



