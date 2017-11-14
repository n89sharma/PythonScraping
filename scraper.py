import json
from selenium import webdriver

class SiteData:
    pass

class Tags:
    pass

eb = SiteData()
eb.url = 'http://www.eddiebauer.ca/browse/sweaters/men/_/N-2774?cm_sp=sub-_-Men-_-Sweaters&currentNode=sweaters&tab=men&previousPage=GNAV'
eb.prod = '.preview-details'
eb.tag_type = 'CSS'
eb.tags = {}
eb.tags['product_name'] = '.prd-name'
eb.tags['regular_price'] = '.regular-price'
eb.tags['sale_price'] = '.sale-price'
eb.tags['reviews'] = '.footnote'
eb.tags['rating'] = '.starRating'

cm = SiteData()
# cm.url = 'http://www.clubmonaco.ca/family/index.jsp?categoryId=12770913&ab=MLP_MSWG&size=99'
cm.url = 'file:///Users/nik/Documents/development/PythonScraping/club_monaco/Men%20_%20Sweaters%20_%20Club%20Monaco%20Canada.htm'
cm.prod = '.product'
cm.tag_type = 'XML'
cm.tags = {}
cm.tags['product_name'] = 'h6/a'
cm.tags['regular_price'] = 'a/span'

def getData(site):

    driver = webdriver.PhantomJS()
    driver.get(site.url)
    data = []
    for prod_element in driver.find_elements_by_css_selector(site.prod):
        row = {}

        if(site.tag_type == 'XML'):
            find = prod_element.find_element_by_xpath            
        elif(site.tag_type == 'CSS'):
            find = prod_element.find_element_by_css_selector

        for (key, value) in site.tags.iteritems():
            try:
                element = find(value)
                row[key] = element.text
            except:
                print('error in trying to find ', value)
                row[key] = 'error - element not found'

             
        data.append(row)
    driver.close()
    site.data = data

getData(cm)
print(cm.data)
