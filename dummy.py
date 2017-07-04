# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep    
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
item = "Stm32f103c8t6"
# print item
print item
# create a new Chrome session
driver = webdriver.Chrome()
#driver.implicitly_wait(30)
driver.maximize_window()



# navigate to the application home page
#driver.get("https://world.taobao.com")
driver.get("https://acmemcu.taobao.com/shop/view_shop.htm?spm=a230r.1.14.64.ebb2eb2wZmcEZ&user_number_id=2142287760")
driver.implicitly_wait(10)
search = driver.find_element_by_xpath("//input[@name='keyword']")

'''
# get the search textbox
search_field = driver.find_element_by_name("q")
 
# enter search keyword and submit
search_field.send_keys(item)
search_field.submit()

# reached Stm32f103c8t6 searching page
# get the area that linked to the seller page
shop = driver.find_elements_by_xpath("//div[@class='shop']")
shop_name = []

shop_html = shop[0].get_attribute('innerHTML')
s = BeautifulSoup(shop_html,'html.parser')
for shop_span in s.find_all('span'):
    if(shop_span.get('class')== None):
        shop_name.append(shop_span.string)
shop[9].click()
driver.switch_to_window(driver.window_handles[1])

search = driver.find_element_by_xpath("//input[@name='keyword']")
#search_button = driver.find_element_by_xpath("//li/button[@type='submit']")
search.send_keys(item)
search.submit()
print driver.window_handles
'''
