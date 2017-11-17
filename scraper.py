from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class SiteData:
    pass

class Tags:
    pass

eb = SiteData()
eb.url = 'http://www.eddiebauer.ca/browse/sweaters/men/_/N-2774?cm_sp=sub-_-Men-_-Sweaters&currentNode=sweaters&tab=men&previousPage=GNAV'
eb.prod = 'preview-details'
eb.tag_type = 'CSS'
eb.tags = {}
eb.tags['product_name'] = 'prd-name'
eb.tags['regular_price'] = 'regular-price'
eb.tags['sale_price'] = 'sale-price'
eb.tags['reviews'] = 'footnote'
eb.tags['rating'] = 'starRating'

cm = SiteData()
# cm.url = 'http://www.clubmonaco.ca/family/index.jsp?categoryId=12770913&ab=MLP_MSWG&size=99'
cm.url = 'file:///Users/nik/Documents/development/PythonScraping/club_monaco/Men%20_%20Sweaters%20_%20Club%20Monaco%20Canada.htm'
cm.prod = 'product-details'
cm.tag_type = 'XPATH'
cm.tags = {}
cm.tags['product_name'] = './h6/a'
cm.tags['regular_price'] = './a/span'

hr = SiteData()
hr.url = 'https://www.harryrosen.com/en/'
hr.url = 'https://www.harryrosen.com/en/clothing/casual-wear/c/sweaters-knits'
hr.click_path = [
    {'by': 'XPATH', 'value': './a[@href=\'/en/clothing/c/clothing\']'},
    {'by': 'XPATH', 'value': './a[@href=\'/en/clothing/c/casual-wear\']'}
]
hr.prod = 'hr-product-lister-grid-item-inner'
hr.tag_type = 'XPATH'
hr.next_page_button = '//a[@class=\'icon hr-icon-thick-chevron-right next\']'
hr.next_page_button = 'a.icon.hr-icon-thick-chevron-right.next'
hr.tags = {}
hr.tags['designer'] = './div[@class=\'hr-product-lister-grid-item-content-wp\']/h3'
hr.tags['product_name'] = './div[@class=\'hr-product-lister-grid-item-content-wp\']/h4[1]'
hr.tags['regular_price'] = './div[@class=\'hr-product-lister-grid-item-content-wp\']/h4[2]/div[@class=\'price\']/div[@class=\'hr-product-price\']'


def get_page_data(site, driver):

    print('getting page data')
    page_data = []
    prod_elements = driver.find_elements_by_class_name(site.prod)
    for prod_element in prod_elements:
        row = {}

        if site.tag_type == 'XPATH':
            find = prod_element.find_element_by_xpath
        elif site.tag_type == 'CSS':
            find = prod_element.find_element_by_class_name

        for (key, value) in site.tags.iteritems():
            try:
                element = find(value)
                row[key] = element.text
            except:
                print('error in trying to find ', value)
                row[key] = 'error - element not found'

        page_data.append(row)
    # print(page_data)
    return page_data

def is_next_page_available(site, driver):

    print('checking next page link')
    next_page_exists = False
    if site.next_page_button is not None:
        try:
            # next_page_links = driver.find_elements_by_xpath(site.next_page_button)
            print(site.next_page_button)
            next_page_links = driver.find_elements_by_css_selector(site.next_page_button)
            visible_link = None
            for link in next_page_links:
                if link.is_displayed() and link.is_enabled() :
                    visible_link = link
                print(link, link.is_displayed(), link.is_enabled())
            print('next page links found', len(next_page_links))
            print('visible link', visible_link)
            visible_link.click()
            next_page_exists = True
        except Exception as e:
            next_page_exists = False
            print('exception thrown', e)
            
    return next_page_exists, next_page_links

def get_data(site):

    driver = webdriver.PhantomJS()
    driver.get(site.url)
    data = []

    next_page_exists = True
    while next_page_exists:
        data.append(get_page_data(site, driver))
        next_page_exists, next_page_links = is_next_page_available(site, driver)

    driver.close()
    site.data = data

    return next_page_links

next_page_links = get_data(hr)
# print(hr.data)
