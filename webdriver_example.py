import os
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep    
  
# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()
 
# navigate to the application home page
driver.get("https://world.taobao.com")
 
# get the search textbox
search_field = driver.find_element_by_name("q")
 
# enter search keyword and submit
search_field.send_keys("Stm32")
search_field.submit()

# reached stm32 searching page
# navigate to different product pages
product = driver.find_element_by_class_name("item-inner")
driver1 = product.click()
print driver.current_url

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
