import os
from dotenv import load_dotenv
from crawler.obj.driver import Driver
from crawler.infra.sql import create_table, recreate_table
load_dotenv()

if __name__ == "__main__":
    # recreate_table()
    sunmoon_driver = Driver()
    sunmoon_driver.login_to_sunmoon()
    sunmoon_driver.move_page()
    sunmoon_driver.get_bus_info()
    sunmoon_driver.compare_with_db()
    sunmoon_driver.save_bus_info_to_db()
