from configparser import ConfigParser
from class_scraper import MapScraper

if __name__ == "__main__":
    config = ConfigParser()
    config.read("Configurations.ini")
    url = config.get("URL", "map")
    search = config.get("Search_Parameters", "location")
    panel_xpath = config.get("XPath", "panel")
    retires = int(config.get("Tries", "tries"))

    obj = MapScraper(retires, search)
    
    obj.config_driver()
    obj.search_location(url, search)
    obj.load_locations(panel_xpath)
    obj.get_business_info()
