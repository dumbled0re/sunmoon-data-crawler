import os
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Driver():
    def __init__(self):
        self.baseurl = os.getenv('BASEURL')
        self.options = Options()

        # deploy to heroku
        # self.options.binary_location = '/usr/bin/google-chrome'
        # self.options.add_argument('--headless')
        # self.options.add_argument('--window-size=1280,1024')

        # debug
        self.driver = webdriver.Chrome(executable_path=os.getenv('DRIVER_PATH'), chrome_options=self.options)

    def login_to_sunmoon(self):
        self.driver.get(self.baseurl)
        id = self.driver.find_element_by_id('txtID')
        id.send_keys(os.getenv('ID'))

        pw = self.driver.find_element_by_id('txtPasswd')
        pw.send_keys(os.getenv('PW'))

        self.driver.find_element_by_id('rboPortal').click()
        self.driver.find_element_by_id('ContentPlaceHolder_Main_btnLogin').click()

    def move_page(self):
        self.driver.get("https://lily.sunmoon.ac.kr/Page/Story/Notice.aspx?ca=001")
        sleep(5)

    def get_bus_info(self):
        pass

    def save_bus_info_to_db(self):
        pass

    def update_bus_info():
        pass


