import os
import pickle
import json
from selenium import webdriver

class SiteData():
	pass


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

fileName = 'data.pickle'
d = load()
wclear = lambda: os.system('CLS')
mclear = lambda: os.system('clear')
driver = webdriver.PhantomJS()
get = lambda url: driver.get(url)
find = lambda css_selector: driver.find_elements_by_css_selector(css_selector)
find_in_el = lambda el, css_selector: el.find_elements_by_css_selector(css_selector)