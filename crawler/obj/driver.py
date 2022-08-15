import os
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from crawler.utils.logger import logger
from crawler.utils.utils import SUNMOON_BUS
from crawler.obj.slack_notification import SlackNotification
from crawler.infra.sql import add_several_bus_records, update_several_bus_records, query_bus_records, query_all_bus_id


class Driver():
    __bus_info_list = []

    def __init__(self):
        self.baseurl = os.getenv('BASEURL')
        self.is_update = False
        self.options = Options()
        self.options.add_argument('--headless')

        # deploy to heroku
        # self.options.binary_location = '/usr/bin/google-chrome'
        # self.options.add_argument('--window-size=1280,1024')

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

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
            if re.search(r"셔틀버스", tds[2].text):
                bus_dict["title"] = tds[2].text
                logger.debug(f'タイトル: {bus_dict["title"]}')
                bus_dict["url"] = tds[2].find_element_by_tag_name("a").get_attribute("href")
                logger.debug(f'url: {bus_dict["url"]}')
                bus_dict["creation_date"] = tds[4].text
                logger.debug(f'作成日: {bus_dict["creation_date"]}')
        self.__bus_info_list.append(bus_dict)

    def compare_with_db(self):
        bus_records = query_bus_records()
        for bus_record in bus_records:
            prev_bus_record = bus_record.__dict__
            logger.debug(f"self.__bus_info_list: {self.__bus_info_list}")
            logger.debug(f"bus_record: {bus_record}")
            if self.__bus_info_list[0]["creation_date"] != prev_bus_record["creation_date"]:
                self.is_update = True

        if self.driver:
            # self.driver.close()
            self.driver.quit()
            logger.debug('ドライバーを停止しました')

    def save_bus_info_to_db(self):
        if self.__bus_info_list:
            add_several_bus_records(self.__bus_info_list)
            logger.debug("DBに新しいバス情報を保存しました")
            SlackNotification().send_message(f'シャトルバスの情報が追加されました。URLは"{self.__bus_info_list[0]["url"]}"です')
        else:
            logger.debug("新しいバス情報はありませんでした。")
            SlackNotification().send_message("新しいバス情報はありませんでした。")

    def update_exist_bus_info(self):
        if self.is_update:
            update_several_bus_records(self.__bus_info_list)
            logger.debug("DBに新しいバス情報を保存しました")
            SlackNotification().send_message(f'シャトルバスの情報が更新されました。URLは"{self.__bus_info_list[0]["url"]}"です')
        else:
            logger.debug("新しいバス情報はありませんでした。")
            SlackNotification().send_message("新しいバス情報はありませんでした。")
