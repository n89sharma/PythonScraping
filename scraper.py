import json

from selenium import webdriver


class Scraper:
    scraped_data = {}
    can_go_to_next_page = True
    driver = webdriver.PhantomJS()
    site_data = {}

    def __init__(self, site_data_map, max_pages=2, windowx=1920, windowy=1020, implicit_wait=5):
        self.driver.set_window_size(windowx, windowy)
        self.driver.implicitly_wait(implicit_wait)
        self.max_pages = max_pages
        self.current_page = 1
        self.site_data_map = site_data_map
        self.complete_data_set = {}

    def run(self):
        for org, site_data in self.site_data_map.items():
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
        for prod_element in prod_elements:
            row = {}
            for tag_data in self.site_data['tags']:
                key, by, tag = tag_data['key'], tag_data['by'], tag_data['tag']
                element = self.get_element(by, tag, prod_element)
                if element:
                    if 'text_attribute' not in tag_data.keys():
                        row[key] = element.text
                    else:
                        row[key] = element.get_attribute(tag_data['text_attribute'])
            page_data.append(row)
        return page_data

    def get_element(self, by, value, element=None):
        try:
            if element:
                return element.find_element(by, value)
            else:
                return self.driver.find_element(by, value)
        except Exception as e:
            print(e, "by: ", by, "value: ", value)
            return None

    def is_page_available_and_within_target(self):
        is_page_available_and_within_target = False
        by = self.site_data['next_page_tag']['by']
        tag = self.site_data['next_page_tag']['tag']
        if by and tag:
            next_page_link = self.get_element(by, tag)
            if next_page_link.is_displayed() and self.current_page < self.max_pages:
                next_page_link.click()
                self.current_page += 1
                is_page_available_and_within_target = True
        self.can_go_to_next_page = is_page_available_and_within_target
        return is_page_available_and_within_target

    def reset_page(self):
        self.current_page = 1
        self.can_go_to_next_page = True


site_data_map = {
    'eddie bauer': json.load(open('./site_data/eddie_bauer.json')),
    'hary rosen': json.load(open('./site_data/hary_rosen.json')),
    'club monaco': json.load(open('./site_data/club_monaco.json'))}

site_data_map = {
    'eddie bauer': json.load(open('./site_data/eddie_bauer.json'))}

scraper = Scraper(site_data_map)
scraper.run()
print(scraper.complete_data_set)
