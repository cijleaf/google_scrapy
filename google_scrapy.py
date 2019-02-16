import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import csv


class Scraper(object):
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
        self.driver.get(
            'https://www.google.com/search?source=hp&ei=O21kXOawEYe-wAOJ75CwCw&q=Dmitry+Rybolovlev&btnK=Google+Search&oq=Dmitry+Rybolovlev')
        domain = 'intpolicydigest.org'
        name = 'Dmitry Rybolovlev'
        result = []
        index = 0
        time.sleep(3)

        while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            url_list = soup.find_all('cite', {'class': 'iUh30'})  # serial number list
            print("********************", len(url_list))
            for i in range(len(url_list)):
                if domain in url_list[i].text:
                    print(url_list[i].text)
                    result.append(url_list[i].text)
                    index = i
                    break

            if len(result) > 0:
                print(index)
                self.driver.get(result[-1])

                SCROLL_PAUSE_TIME = 4
                while True:

                    last_height = self.driver.execute_script("return document.body.scrollHeight")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(SCROLL_PAUSE_TIME)
                        new_height = self.driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        else:
                            last_height = new_height
                            continue
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                comments = soup.find_all('div', {'class': 'alm-single-post'})
                print("Comment:", type(comments), len(comments))

                with open('output.csv', mode='w') as csv_file:
                    fieldnames = ['name', 'domain', 'number_of_comments']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    writer.writeheader()
                    writer.writerow({'name': name, 'domain': domain, 'number_of_comments': len(comments)})

                break
            else:
                self.driver.find_element_by_xpath('//a[@id="pnnext"]').click()

        self.driver.quit()


if __name__ == "__main__":
    Scraper()
