import glob
import json

from selenium import webdriver


class Scraper:
    scraped_data = {}
    can_go_to_next_page = True
    driver = webdriver.PhantomJS()
    site_data = {}

    def __init__(self, site_data_map, exclude_orgs=[], max_pages=2, windowx=1024, windowy=800, implicit_wait=5):
        self.driver.set_window_size(windowx, windowy)
        self.driver.implicitly_wait(implicit_wait)
        self.max_pages = max_pages
        self.current_page = 1
        self.site_data_map = site_data_map
        self.complete_data_set = {}
        self.exclude_orgs = exclude_orgs

    def run(self):
        for org, site_data in self.site_data_map.iteritems():
            if org not in self.exclude_orgs:
                print(org)
                site_scraped_data = []
                self.site_data = site_data
                self.driver.get(site_data['url'])
                self.reset_page()
                while self.can_go_to_next_page:
                    site_scraped_data.extend(self.get_page_data())
                    self.is_page_available_and_within_target()
                self.complete_data_set[org] = site_scraped_data
        self.driver.close()

    def get_page_data(self):
        page_data = []
        prod_elements = self.driver.find_elements(
            by=self.site_data['target']['by'],
            value=self.site_data['target']['tag'])
        print(len(prod_elements))
        for prod_element in prod_elements:
            row = {}
            for tag_data in self.site_data['tags']:
                key, by, tag = tag_data['key'], tag_data['by'], tag_data['tag']
                element = self.get_element(by, tag, prod_element)
                if element:
                    if 'text_attribute' not in tag_data.keys():
                        row[key] = element.get_attribute("innerText")
                    else:
                        row[key] = element.get_attribute(tag_data['text_attribute'])
            page_data.append(row)
        return page_data

    def get_element(self, by, value, element=None):
        if element:
            sub_element = self.get_elements(by, value, element)                
        else:
            sub_element = self.get_elements(by, value, self.driver)
        if not sub_element:
            print("Element not found. By: ", by, ", value: ", value)
        return sub_element

    def get_elements(self, by, value, elementOrDriver):
        sub_elements = elementOrDriver.find_elements(by, value)
        if len(sub_elements) > 0:
            return sub_elements[0]
        else:
            return None

    def is_page_available_and_within_target(self):
        is_page_available_and_within_target = False
        by = self.site_data['next_page_tag']['by']
        tag = self.site_data['next_page_tag']['tag']
        if by and tag:
            next_page_link = self.get_element(by, tag)
            if self.current_page < self.max_pages and next_page_link is not None and next_page_link.is_displayed():
                next_page_link.click()
                self.current_page += 1
                is_page_available_and_within_target = True
        self.can_go_to_next_page = is_page_available_and_within_target
        return is_page_available_and_within_target

    def reset_page(self):
        self.current_page = 1
        self.can_go_to_next_page = True


site_data_map = {}
for file_path in glob.glob("./site_data/*.json"):
    json_data = json.load(open(file_path))
    site_data_map[json_data['organization']] = json_data

scraper = Scraper(site_data_map=site_data_map, max_pages=26)
scraper.run()

with open('result.json', 'w') as f:
    json.dump(scraper.complete_data_set, f)
