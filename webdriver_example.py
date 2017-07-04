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

# check the exists of class name
def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def search_item_in_shop_page(driver, item):
    # get the search textbox from the shop website
    
    if(driver.current_url.find("tmall")!=-1):
        search = driver.find_element_by_name("q")
        search_button = driver.find_element_by_xpath("//*[contains(text(), '搜本店')]")
        search.send_keys(item)
        search_button.click()
    elif(driver.current_url.find("world")==-1):
        search = driver.find_element_by_xpath("//input[@name='keyword']")
        #search_button = driver.find_element_by_xpath("//li/button[@type='submit']")
        search.send_keys(item)
        search.submit()
        # some shop open the item page in new tab, close the current tab and
        # focus on the tab we interested
        if(len(driver.window_handles)>2):
            driver.close()
            driver.switch_to_window(driver.window_handles[-1])
    else:
        search = driver.find_element_by_name("q")
        search_button = driver.find_element_by_xpath("//*[contains(text(), '搜本店')]")
        search.send_keys(item)
        search_button.click()
    
    # enter search keyword and sendby
    
    
item = "Stm32f103c8t6"
# print item
print item
# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()



# navigate to the application home page
driver.get("https://world.taobao.com")
 
# get the search textbox
search_field = driver.find_element_by_name("q")
 
# enter search keyword and submit
search_field.send_keys(item)
search_field.submit()

# reached Stm32f103c8t6 searching page
# get the area that linked to the seller page
shop = driver.find_elements_by_xpath("//div[@class='shop']")
shop_name = []


''' for loop to get all shops (working)
for x in range(len(shop)):
    #print shop[x]
    i = 0
'''
count = 0
repeat = 0
item_price_all = []
for i in range(len(shop)):
    # get the html code within the area that got above
    shop_html = shop[i].get_attribute('innerHTML')

    # pass the html using beautifulsoup
    s = BeautifulSoup(shop_html,'html.parser')

    # get the seller's shop name
    for shop_span in s.find_all('span'):
        if(shop_span.get('class')== None):
            shop_name.append(shop_span.string)

    for j in range(len(shop_name)-1):
        if(shop_name[i] == shop_name[j]):
            repeat = 1
            break
        else:
            repeat = 0

    if(repeat == 0):
        print count, i
        count+=1
        #print shop_name
        print "Shop name: ", shop_name[i]
        # navigate to the seller's shop website
        shop[i].click()

        # switch the handling window to shop website
        driver.switch_to_window(driver.window_handles[1])
        search_item_in_shop_page(driver, item)

        # switch the handling window to item searching page of shop website
        driver.switch_to_window(driver.window_handles[1])

        # get the area of the item list
        # This handle taobao webside
        if(driver.current_url.find("tmall")==-1):
            if (check_exists_by_class_name(driver, "item3line1")):
                searchedItem = driver.find_element_by_class_name("item3line1")
            else:
                searchedItem = driver.find_element_by_class_name("item4line1")
        # This handle tmall webside
        else:
            if (check_exists_by_class_name(driver, "item5line1")):
                searchedItem = driver.find_element_by_class_name("item5line1")
            else:
                searchedItem = driver.find_element_by_class_name("item4line1")
        
        # get the html code of the area that found
        item_html = searchedItem.get_attribute('innerHTML')
        item_price = []

        # pass the html using beautifulsoup
        soup = BeautifulSoup(item_html,'html.parser')

        # find all the items' price 
        for span in soup.find_all('span'):
            if(span.get('class')==[u'c-price']):
                # remove extra white space with strip() 
                item_price.append(float(span.string.strip()))
                item_price_all.append(item_price[-1])

        # print the items' price
        print "Price: ", item_price

        # close the current window (shop website)
        # and return to the search page
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

        # switch off chrome driver
        #driver.quit()

print item_price_all

''' **********************Draw graph********************************** '''
plt.figure(1)
item_price_total = 0
t = 0
for x in range(len(item_price_all)):
    item_price_total += item_price_all[x]
item_price_mu = item_price_total/(x+1)
for x in range(len(item_price_all)):
    t += np.square(item_price_all[x]-item_price_mu)
item_price_sigma = np.sqrt(t/(x+1))

print item_price_total
print item_price_mu
print item_price_sigma               




''' 
# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name  method
lists= driver.find_elements_by_class_name("r")
 
# get the number of elements found
print ("Found" + str(len(lists)) +  "searches:")
 
# iterate through each element and print the text that is
# name of the search
 
i=0
for listitem in lists:
   print (listitem)
   i=i+1
   if(i>10):
      break
 
# close the browser window
driver.quit()
'''
