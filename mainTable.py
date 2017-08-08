# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4.QtCore import *
from selenium import webdriver
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from bs4 import BeautifulSoup
import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
import table_example
import os
import re


# Stm32f103c8t6
class taobao:
    # check the exists of class name
    def check_exists_by_class_name(self,driver, class_name):
        try:
            driver.find_element_by_class_name(class_name)
        except NoSuchElementException:
            print "false"
            return False
        print "True"
        return True

    def search_item_in_shop_page(self,driver, item):
        # get the search textbox from the shop website
        search = driver.find_element_by_name("q")
        search_button = driver.find_element_by_xpath("//*[contains(text(), '搜本店')]")
        search.click()
        search.send_keys(item)
        driver.implicitly_wait(30)
        search_button.click()
        driver.implicitly_wait(30)
            
    def getPrice(self, item):
        # create a new Chrome session
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)



        # navigate to the application home page
        driver.get("https://login.taobao.com/member/login.jhtml?spm=a21wu.241046-my.754894437.1.4519fd50dPXaMM&f=top&redirectURL=https%3A%2F%2Fworld.taobao.com%2F%3Fspm%3Da21bp.8077467.1417485807582.1.6449e6bcStIj9X")

        # login to Taobao website
        username = driver.find_element_by_id("TPL_username_1")
        password = driver.find_element_by_id("TPL_password_1")
        username.send_keys("yenng3")
        password.send_keys("12345678abc")
        login = driver.find_element_by_id("J_SubmitStatic")
        login.click()
         
        # get the search textbox
        search_field = driver.find_element_by_name("q")
         
        # enter search keyword and submit
        search_field.send_keys(item)
        search_field.submit()
        driver.implicitly_wait(30)

        # get the total pages of the search
        total = driver.find_element_by_xpath("//div[@class='total']")
        total_page = int(re.search(r'\d+',total.text).group())

        # reached Stm32f103c8t6 searching page
        # get the area that linked to the seller page
        shop = driver.find_elements_by_xpath("//div[@class='shop']")
        self.shop_name = []

        next_page = driver.find_element_by_xpath("//li[@class='item next']")
        ''' for loop to get all shops (working)
        for x in range(len(shop)):
            #print shop[x]
            i = 0
        '''
        count = 0
        repeat = 0
        self.item_price_all = []
        item_price_list = []
        for k in range(len(shop)):
            # get the html code within the area that got above
            shop_html = shop[k].get_attribute('innerHTML')

            # pass the html using beautifulsoup
            s = BeautifulSoup(shop_html,'html.parser')

            # get the seller's shop name
            for shop_span in s.find_all('span'):
                if(shop_span.get('class')== None):
                    self.shop_name.append(shop_span.string)
                    # check whether the shop name is repeated
                    for j in range(len(self.shop_name)-1):
                        if(shop_span.string == self.shop_name[j]):
                            del self.shop_name[-1]

        # print self.shop_name
        self.linkList = []
        
        for i in range(len(self.shop_name)):
            #print shop_name
            print "Shop name: ", self.shop_name[i]
            # navigate to the seller's shop website
            shop[i].click()

            # switch the handling window to shop website
            driver.switch_to_window(driver.window_handles[1])
            driver.implicitly_wait(30)
            self.linkList.append(str(driver.current_url))
            if(driver.current_url.find("tmall")==-1):
                url = driver.current_url
                pos = url.find(".taobao")
                url = url[:pos] + ".world" + url[pos:]
                driver.get(url)
                driver.implicitly_wait(30)
            #else:
            #    break
            search = driver.find_element_by_name("q")
            search_button = driver.find_element_by_xpath("//*[contains(text(), '搜本店')]")
            for n in range(3):
                try:
                    search.click()
                    driver.implicitly_wait(30)
                    search.send_keys(item)
                    driver.implicitly_wait(30)
                    search_button.click()
                    break
                except StaleElementReferenceException:
                    #print n
                    driver.refresh()
            # switch the handling window to item searching page of shop website
            driver.switch_to_window(driver.window_handles[1])

            # get the area of the item list
            # This handle taobao webside
            if(driver.current_url.find("tmall")==-1):
                if (self.check_exists_by_class_name(driver, "item3line1")):
                    searchedItem = driver.find_element_by_class_name("item3line1")
                else:
                    searchedItem = driver.find_element_by_class_name("item4line1")
            # This handle tmall webside
            else:
                if (self.check_exists_by_class_name(driver, "item5line1")):
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
                    self.item_price_all.append(item_price[-1])

            # print the items' price
            print "Price: ", item_price
            item_price_list.append(item_price)

            # close the current window (shop website)
            # and return to the search page
            driver.close()
            driver.switch_to_window(driver.window_handles[0])

            # switch off chrome driver
            #driver.quit()
        #next_page.click()
        #driver.implicitly_wait(30)

        self.item_price_list = item_price_list
        #print item_price_all

        ''' **********************Draw graph********************************** '''
        
        #plt.figure(1)
        self.item_price_total = 0
        t = 0
        for x in range(len(self.item_price_all)):
            self.item_price_total += self.item_price_all[x]
        self.item_price_mu = self.item_price_total/(x+1)
        for x in range(len(self.item_price_all)):
            t += np.square(self.item_price_all[x]-self.item_price_mu)
        self.item_price_sigma = np.sqrt(t/(x+1))

        '''
        print item_price_total
        print item_price_mu
        print item_price_sigma
        '''              


class ExampleTable(QtGui.QDialog, table_example.Ui_Dialog):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)

        self.figure = plt.figure(1)
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.canvas)
        #self.verticalLayout.addWidget(self.toolbar)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        
        self.Plot.clicked.connect(self.plot)
        self.getData.clicked.connect(self.data)
        self.confirm.clicked.connect(self.Confirm)

    def Confirm(self):
        title = QStringList()
        shop_title = QString('Shop Name')
        item_title = QString(self.itemInput.text())
        link_title = QString('Link')
        title.append(shop_title)
        title.append(item_title)
        title.append(link_title)
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.item = str(self.itemInput.text())


        
    def data(self):
        tb = taobao()
        tb.getPrice(self.item)

        for i in range(len(tb.shop_name)):
            if(self.tableWidget.rowCount() == i):
                self.tableWidget.insertRow(int(self.tableWidget.rowCount()))
            self.tableWidget.setItem(i,0, QTableWidgetItem(tb.shop_name[i]))
            x = tb.item_price_list[i]
            price = ""
            for j in range(len(x)):
                price = price +" " + str(x[j])
            self.tableWidget.setItem(i,1, QTableWidgetItem(price))
            self.tableWidget.setItem(i,2, QTableWidgetItem(tb.linkList[i]))

        self.item_price_all = tb.item_price_all

        
    def plot(self):
        x = self.item_price_all

        total = 0

        ax = self.figure.add_subplot(111)

        ax.hold(False)
        
        for i in range(len(x)):
            total += x[i]
        avr = total/len(x)
        y = 0
        for i in range(len(x)):
            y += np.square(x[i]-avr)
        sd = np.sqrt(y/len(x))

        n, bins, patches = ax.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
        z = mlab.normpdf(bins, avr, sd)
        ax.axis([0, 200, 0, 0.1])
        ax.plot(bins, z, '--')

        self.canvas.draw()
        
def main():
    app = QtGui.QApplication(sys.argv)
    dialog = ExampleTable()
    dialog.show()
    app.exec_()

if __name__ == '__main__':
    main()
