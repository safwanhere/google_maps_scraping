from bs4 import BeautifulSoup
import time
import pandas as pd
from utils import Utils
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

obj = Utils()

class MapScraper:
    def __init__(self, tries, file_name):
        self.driver = None
        self.flag = True
        self.tries = tries
        self.output_file_name = f'{file_name}.csv'
        self.unique = []

        columns =['Restaurant Name', 'Address', 'Phone Number', 'Website', 'Rating', 
                  'Reviews', 'Opening Hours', 'Expense', 'Category','Details']
        self.df = pd.DataFrame(columns = columns)

    def config_driver(self):
        chrome_options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager(version="114.0.5735.90").install())
        driver = webdriver.Chrome(service = service, options=chrome_options)
        self.driver = driver

    def search_location(self, url, location):
        self.driver.get(url)
        # Search for the location
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

    def load_locations(self, xpath):
        tries = 0
        self.panel = []
        while self.flag: # loop will run to load all the locations
            self.wait = WebDriverWait(self.driver, 10)
            scrollable_div = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)
            var = len(self.panel)
            self.panel = self.driver.find_elements(By.CLASS_NAME, "hfpxzc")
            
            if "You've reached the end of the list" in self.driver.page_source:
                self.flag = False

            if len(self.panel) == var:
                tries += 1
                if tries > self.tries:
                    print("There might be some issue with Network as page was stuck with loading!")
                    break
            else:
                tries = 0
            
            print(len(self.panel))

    def get_business_info(self):
        for location in self.panel:
            try:
                self.driver.execute_script("arguments[0].click();", location)
                time.sleep(2)

                start_time = time.time()
                source = self.driver.page_source
                soup = BeautifulSoup(source, 'html.parser')
                name = Utils.parse_name(soup)
                
                if name not in self.unique and name:
                    self.unique.append(name)
                    rating, reviews = Utils.parse_rating_and_reviews(soup)
                    expense = Utils.parse_expense(soup)
                    address = Utils.parse_address(soup)
                    category = Utils.parse_category(soup)
                    website, phone = Utils.parse_contact_info(soup)
                    detail = Utils.get_detail(soup)
                    hours = Utils.parse_time(soup)

                    record = {
                        "Restaurant Name" : name,
                        "Address": address,
                        "Phone Number": phone,
                        "Website": website,
                        "Rating": rating,
                        "Reviews": reviews,
                        'Opening Hours': hours,
                        "Expense": expense,
                        "Category": category,
                        "Details" : detail
                        }
                    
                    end_time = time.time()
                    print(end_time - start_time)
                    
                    print(record)
                    print("--------------")
                    self.df = Utils.append_records(self.df, record)

                    Utils.save_data(self.df, self.output_file_name)

            except Exception as err:
                print(err)
        
        print("Scraped data has been saved in a CSV file!")
        self.driver.quit()
