import os
import pickle
from selenium import webdriver

class SiteData():
	def __init__(self, url, prod, prod_name, sale_price, reg_price, number_reviews, rating, pagination):
		self.url = url
		self.prod = prod
		self.prod_name = prod_name
		self.sale_price = sale_price
		self.reg_price = reg_price
		self.number_reviews = number_reviews
		self.rating = rating
		self.pagination = pagination


def pdir(moduleName):
    for dirs in dir(moduleName):
    	#if callable(getattr(moduleName, dirs)):
        print(dirs)

def load():
    with open(fileName, 'rb') as f:
        d = pickle.load(f)
    return d

def dump(d):
    with open(fileName, 'wb') as f:
        pickle.dump(d, f)

def getData():


fileName = 'data.pickle'
d = load()
clear = lambda: os.system('CLS')
driver = webdriver.PhantomJS()
get = lambda url: driver.get(url)
find = lambda css_selector: driver.find_elements_by_css_selector(css_selector)
find_in_el = lambda el, css_selector: el.find_elements_by_css_selector(css_selector)