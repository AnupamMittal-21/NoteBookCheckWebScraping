import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By


class MobileDataScraper(webdriver.Chrome):

    def __init__(self, driver_path, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown

        load_dotenv('data.env')

        #  Setting a path of a chrome driver from local directory
        driver_path_name = os.environ.get("DRIVER_PATH")
        os.environ['PATH'] += driver_path_name
        options = webdriver.ChromeOptions()
        user_path_name = os.environ.get("USER_PATH")
        options.add_argument(user_path_name)
        super(MobileDataScraper, self).__init__(options=options)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def getUrl(self, url):
        self.get(url)

    def scrapLinks(self):
        # Scraping the links of the mobiles
        links = self.find_elements(By.CSS_SELECTOR, "a.introa_large.introa_review")
        links = [link.get_attribute("href") for link in links]
        return links
