import json
from selenium import webdriver

class SiteData:
    pass

class Tags:
    pass

eb = SiteData()
eb.url = 'http://www.eddiebauer.ca/browse/sweaters/men/_/N-2774?cm_sp=sub-_-Men-_-Sweaters&currentNode=sweaters&tab=men&previousPage=GNAV'
eb.prod = '.preview-details'
eb.tags = {}
eb.tags['product_name'] = '.prd-name'
eb.tags['regular_price'] = '.regular-price'
eb.tags['sale_price'] = '.sale-price'
eb.tags['reviews'] = '.footnote'
eb.tags['rating'] = '.starRating'

cm = SiteData()
cm.url = 'http://www.clubmonaco.ca/family/index.jsp?categoryId=12770913&ab=MLP_MSWG&size=99'
cm.prod = '.product'
cm.tags = {}
cm.tags['product_name'] = '//div[2]/h6/a'
cm.tags['regular_price'] = '//div[2]/a/span'

def getData(site):

    driver = webdriver.PhantomJS()
    driver.get(site.url)
    data = []
    for prod_elements in driver.find_elements_by_css_selector(site.prod):
        row = {}
        for (key, value) in site.tags.iteritems():
            elements = prod_elements.find_elements_by_css_selector(value)
            if(len(elements) > 0):
                row[key] = elements[0].text 
        data.append(row)
    driver.close()
    eb.data = data

def getProds(site):

    driver = webdriver.PhantomJS()
    driver.get(site.url)
    return driver.find_elements_by_css_selector(site.prod)

prods = getProds(cm)
prod = prods[0].find_elements_by_xpath(cm.tags['product_name'])[0].text
print(prod)
