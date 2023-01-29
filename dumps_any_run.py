import selenium.webdriver
from selenium import webdriver
from bs4 import BeautifulSoup, GuessedAtParserWarning
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import time


class Downloader:

    def __init__(self):
        self._driver = webdriver.Firefox()
        self._driver.set_page_load_timeout(15)

    @staticmethod
    def open_main_page(driver: selenium.webdriver.Firefox):
        try:
            driver.get('https://app.any.run/submissions/')
        except TimeoutException as e:
            print(e)
        except GuessedAtParserWarning as e:
            print(e)

    @staticmethod
    def registration(driver: selenium.webdriver.Firefox):
        button1 = driver.find_element(By.XPATH, value="//li[@title='Sign In']")
        button1.click()
        login = input("Пожалуйста, введите логин от any run - ")
        driver.find_element(by=By.ID, value='at-field-username_and_email').send_keys(login)
        password = input('Пожалйста, введите пароль от any run - ')
        driver.find_element(by=By.ID, value='at-field-password').send_keys(password)
        button_sign = driver.find_element(by=By.CSS_SELECTOR, value='button.at-btn')
        button_sign.click()

    @staticmethod
    def get_links(driver: selenium.webdriver.Firefox):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        divs = soup.find_all("div", {"class": "history-table--content__row"})
        links = []
        for div in divs:
            tag = div.a.extract()
            links.append({
                "link": tag.get('href')
            })
        return links

    @staticmethod
    def download_pcaps(driver: selenium.webdriver.Firefox, links):
        for i in range(len(links)):
            try:
                driver.get('https://app.any.run' + links[i]['link'])
            except TimeoutException as e:
                print(e)
            except GuessedAtParserWarning as e:
                print(e)
            button_pcap = driver.find_element(by=By.ID, value='pcapLi')
            button_pcap.click()
            time.sleep(3)

    def run(self):
        self.open_main_page(driver=self._driver)
        self.registration(driver=self._driver)
        links = self.get_links(driver=self._driver)
        self.download_pcaps(driver=self._driver, links=links)
