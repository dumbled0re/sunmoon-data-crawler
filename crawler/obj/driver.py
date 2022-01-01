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
from crawler.utils import send_text_to_slack, SUNMOON_BUS
from crawler.infra.sql import add_several_company_records, update_several_company_records, query_all_bus_records, query_all_bus_id


class Driver():
    __bus_info_list = []

    def __init__(self):
        self.baseurl = os.getenv('BASEURL')
        self.options = Options()
        self.is_update = False

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
        sleep(2)

    def get_bus_info(self):
        bus_dict = dict.fromkeys(SUNMOON_BUS)

        showtops = self.driver.find_elements_by_class_name("showtop")
        for showtop in showtops:
            tds = showtop.find_elements_by_tag_name('td')
            if re.search(r"동계방학 셔틀버스", tds[2].text):
                bus_dict["title"] = tds[2].text
                print(f'タイトル: {bus_dict["title"]}')
                bus_dict["url"] = tds[2].find_element_by_tag_name("a").get_attribute("href")
                print(f'url: {bus_dict["url"]}')
                bus_dict["creation_date"] = tds[4].text
                print(f'作成日: {bus_dict["creation_date"]}')
        self.__bus_info_list.append(bus_dict)

    # DBにあるデータと比較して作成日が違かったらself.is_updateをTrueにする処理
    def compare_with_db(self):
        pass

    def save_bus_info_to_db(self):
        if self.__bus_info_list:
            add_several_company_records(self.__bus_info_list)
            print("DBにバス情報を保存しました")
            if self.is_update:
                send_text_to_slack(f'シャトルバスの情報が更新されました。URLは"{self.__bus_info_list[0]["url"]}"です')

    def update_bus_info(self):
        pass


