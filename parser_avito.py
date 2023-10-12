from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
import csv
options = uc.ChromeOptions()
with open('settings.txt', 'r', encoding='utf-8') as f:
    user = f.readline()
options.add_argument(fr'--user-data-dir={user}')
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 1')
options.add_argument("--crash-dumps-dir=tmp")
driver = uc.Chrome(options=options)
driver.set_page_load_timeout(10)
driver.maximize_window()
action = ActionChains(driver)

city = ''

info = []
def get_info(link):
    try:
        address = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="address"] > span').text.strip()
    except:
        address = ''
    try:
        desc = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]').text
    except:
        desc = ''
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="price"]').get_attribute('content')
    except:
        price = ''
    try:
        fio = driver.find_element(By.CSS_SELECTOR, 'div[data-marker="seller-info/name"]').text
    except:
        fio = ''

    try:
        type_seller = driver.find_element(By.CSS_SELECTOR, 'div[data-marker="seller-info/label"]').text
        if 'Частное' not in type_seller:
            type_seller = 'Агенство'
    except:
        type_seller = ''

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-marker="item-view/item-params"] ul > li')))
    except:
        pass
    rows = driver.find_elements(By.CSS_SELECTOR, 'div[data-marker="item-view/item-params"] ul > li')
    count_rooms, s, s_kitchen, s_live, floor, floors, s_plot, s_house = '', '', '', '', '', '', '', ''
    for row in rows:
        if 'О квартире' in driver.find_element(By.CSS_SELECTOR, 'div[data-marker="item-view/item-params"] > span').text.strip():
            try:
                if 'Количество комнат' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    count_rooms = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                count_rooms = ''
            try:
                if 'Общая площадь' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    s = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                s = ''
            try:
                if 'Площадь кухни' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    s_kitchen = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                s_kitchen = ''
            try:
                if 'Жилая площадь' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    s_live = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                s_live = ''
            try:
                if 'Этаж' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    floor = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip().split()[0]
                    floors = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip().split()[-1]
            except:
                floor = ''
                floors = ''
        else:
            try:
                if 'Количество комнат' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    count_rooms = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                count_rooms = ''
            try:
                if 'Площадь участка' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    s_plot = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                s_plot = ''
            try:
                if 'Этажей' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    floors = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip().split()[-1]
            except:
                floors = ''
            try:
                if 'Площадь дома' in row.find_element(By.CSS_SELECTOR, 'span').text:
                    s_house = row.text.removeprefix(row.find_element(By.CSS_SELECTOR, 'span').text).strip()
            except:
                s_house = ''

    insert_csv([fio, type_seller, desc, city, price, s, s_live, s_kitchen, count_rooms, floor, floors, s_plot, s_house, address, link])


def insert_csv(information):
    with open(f'info.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            information
        )


def main():
    links = []
    with open('links.txt', 'r') as f:
        for i in f:
            links.append(i)

    with open(f'info.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Пользователь', 'Тип', 'Описание', 'Город', 'Цена', 'Общая площадь', 'Жилая площадь', 'Площадь кухни', 'Число комнат', 'Этаж', 'Кол-во этажей', 'Площадь участка', 'Площадь дома', 'Адрес', 'Ссылка']
        )

    for url in links:
        while True:
            try:
                driver.get(url)
                break
            except TimeoutException:
                break
            except:
                time.sleep(10)
        time.sleep(1)
        try:
            pages = driver.find_element(By.CSS_SELECTOR, 'ul[data-marker="pagination-button"]').text
            last_page = int(pages.split()[-1])
        except:
            last_page = 1
        global city
        try:
            city = driver.find_element(By.CSS_SELECTOR, 'div[data-marker="search-form/change-location"]').text.split(',')[0].strip()
        except:
            city = ''
        for i in range(1, last_page+1):
            while True:
                try:
                    driver.get(f'{url}&p={str(i)}')
                    break
                except TimeoutException:
                    break
                except:
                    time.sleep(10)
            urls = driver.find_elements(By.CSS_SELECTOR, 'a[data-marker="item-title"]')
            links_items = []
            for url1 in urls:
                link1 = url1.get_attribute('href')
                links_items.append(link1)
            for link in links_items:
                while True:
                    try:
                        driver.get(link)
                        break
                    except TimeoutException:
                        break
                    except:
                        time.sleep(10)
                time.sleep(2)
                get_info(link)



if __name__ == '__main__':
    main()