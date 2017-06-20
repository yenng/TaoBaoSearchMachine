import os
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep    

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

# get the html code within the area that got above
shop_html = shop[0].get_attribute('innerHTML')

# pass the html using beautifulsoup
s = BeautifulSoup(shop_html,'html.parser')

# get the seller's shop name
for shop_span in s.find_all('span'):
    if(shop_span.get('class')== None):
        shop_name = shop_span.string

#print shop_name
print shop_name

''' for loop to get all shops (working)
for x in range(len(shop)):
    #print shop[x]
    i = 0
'''

# navigate to the seller's shop website
shop[0].click()

# switch the handling window to shop website
driver.switch_to_window(driver.window_handles[1])

# get the search textbox from the shop website
search = driver.find_element_by_name("keyword")

# enter search keyword and send 
search.send_keys(item)
search.submit()

# close the current window (shop website)
driver.close()

# switch the handling window to item searching page of shop website
driver.switch_to_window(driver.window_handles[1])

# get the area of the item list
searchedItem = driver.find_element_by_class_name("item5line1")

# get the html code of the area that found
item_html = searchedItem.get_attribute('innerHTML')
item_price = []

# pass the html using beautifulsoup
soup = BeautifulSoup(item_html,'html.parser')

# find all the items' price 
for span in soup.find_all('span'):
    if(span.get('class')==[u'c-price']):
        # remove extra white space with strip() 
        item_price.append(span.string.strip())

# print the items' price
print item_price

# switch off chrome driver
driver.quit()


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
