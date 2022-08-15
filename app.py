import argparse
from dotenv import load_dotenv
from crawler.obj.driver import Driver
from crawler.infra.sql import create_table, recreate_table
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='SUN MOONからバス情報を収集するクローラー')
    parser.add_argument('phase', help='add or update', type=str)
    args = parser.parse_args()

    if args.phase == 'add':
        add()
    elif args.phase == 'update':
        update()
    else:
        print('please input [python app.py add] or [python app.py update]')

def add():
    recreate_table()
    sunmoon_driver = Driver()
    sunmoon_driver.login_to_sunmoon()
    sunmoon_driver.move_page()
    sunmoon_driver.get_bus_info()
    sunmoon_driver.compare_with_db()
    sunmoon_driver.save_bus_info_to_db()

def update():
    sunmoon_driver = Driver()
    sunmoon_driver.login_to_sunmoon()
    sunmoon_driver.move_page()
    sunmoon_driver.get_bus_info()
    sunmoon_driver.compare_with_db()
    sunmoon_driver.update_exist_bus_info()

if __name__ == "__main__":
    main()
