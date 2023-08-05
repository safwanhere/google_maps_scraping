import re
import pandas as pd

class Utils():
    @staticmethod
    def parse_name(content):
        name = None
        try:
            name = content.find('h1', {"class": "DUwDvf"}).text
        
        except Exception as err:
            print("parse_name", err)
            
        return name

    @staticmethod
    def parse_address(content):
        address = None
        try:
            address_block = content.find_all('div', {"class": "RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L"})
            address = address_block[0].text
        
        except Exception as err:
            print("parse_address", err)

        return address
    
    @staticmethod
    def parse_rating_and_reviews(content):
        rating = None
        reviews = None
        try:
            rating_area = content.find('div', {"class": "F7nice"}).text.split("(")
            if len(rating_area) > 1:
                rating = rating_area[0].strip()
                reviews = rating_area[1].split(")")[0].strip()
        
        except Exception as err:
            print("parse_rating_and_reviews", err)
        
        return rating, reviews

    @staticmethod
    def parse_contact_info(content):
        website = None
        phone = None
        try:
            pattern = re.compile(r'[a-zA-Z0-9]+\.+[a-zA-Z]+')
            address_block = content.find_all('div', {"class": "RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L"})
            
            for container in address_block:
                if pattern.search(container.text):
                    website = container.find("a").get('href')

                if "+1" in container.text:
                    phone = container.text

        except Exception as err:
            print("parse_contact_info", err)

        return website, phone

    @staticmethod
    def parse_category(content):
        category = None
        try:
            category = content.find('button', {"class": "DkEaL"}).text
        
        except Exception as err:
            print("parse_category", err)
            
        return category
    
    @staticmethod
    def parse_expense(content):
        expense = None
        try:
            expense = content.find('span', {"class": "mgr77e"}).text.split("·")[1]
        
        except Exception as err:
            print("parse_expense", err)
            
        return expense
    
    @staticmethod
    def parse_time(content):
        time = None
        try:
            for container in content.find_all("span"):
                if "opens" in container.text.lower():
                    # print(container.text)
                    time = container.text.split("⋅")[1].replace("\u202f", " ") 
                    
        except Exception as err:
            print("parse_time", err)

        return time
    @staticmethod
    def get_detail(content):
        detail = None
        try:
            detail = content.find('div', {"class": "PYvSYb"}).text
        
        except Exception as err:
            print("get_detail", err)

        return detail

    @staticmethod
    def append_records(df, record):
        row_to_append = pd.DataFrame([record])
        df = pd.concat([df , row_to_append], ignore_index=True)
        return df

    @staticmethod
    def save_data(df, file_name):
        df.to_csv(file_name, index = False, na_rep = 'NULL')