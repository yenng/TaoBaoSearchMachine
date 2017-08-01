# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4.QtCore import *
from selenium import webdriver
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
import table_example
import os
import re

class taobao:
    # check the exists of class name
    def check_exists_by_class_name(self,driver, class_name):
        print "entering.."
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
            
    def getPrice(self):
        self.item = "Stm32f103c8t6"
        # print item
        print self.item
        # create a new Chrome session
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        #driver.maximize_window()



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
        search_field.send_keys(self.item)
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
        item_price_all = []
        item_price_list = []
        for i in range(len(shop)):
            # get the html code within the area that got above
            shop_html = shop[i].get_attribute('innerHTML')

            # pass the html using beautifulsoup
            s = BeautifulSoup(shop_html,'html.parser')

            # get the seller's shop name
            for shop_span in s.find_all('span'):
                if(shop_span.get('class')== None):
                    self.shop_name.append(shop_span.string)

            for j in range(len(self.shop_name)-1):
                if(self.shop_name[i] == self.shop_name[j]):
                    repeat = 1
                    break
                else:
                    repeat = 0

            if(repeat == 0):
                print count, i
                count+=1
                #print shop_name
                print "Shop name: ", self.shop_name[i]
                # navigate to the seller's shop website
                shop[i].click()

                # switch the handling window to shop website
                driver.switch_to_window(driver.window_handles[1])
                driver.implicitly_wait(30)
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
                        search.send_keys(self.item)
                        driver.implicitly_wait(30)
                        search_button.click()
                        driver.implicitly_wait(30)
                        break
                    except StaleElementReferenceException:
                        print n
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
                        item_price_all.append(item_price[-1])

                # print the items' price
                print "Price: ", item_price
                item_price_list.append(item_price)

                # close the current window (shop website)
                # and return to the search page
                driver.close()
                driver.switch_to_window(driver.window_handles[0])

                # switch off chrome driver
                #driver.quit()
        next_page.click()
        driver.implicitly_wait(30)

        self.item_price_list = item_price_list
        #print item_price_all

        ''' **********************Draw graph********************************** '''
        plt.figure(1)
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
        self.tableWidget.setColumnCount(2)

        self.Plot.clicked.connect(self.plot)
        self.getData.clicked.connect(self.data)


        
    def data(self):
        tb = taobao()
        tb.getPrice()
        title = QStringList()
        shop_title = QString('Shop Name')
        item_title = QString(self.item)
        title.append(shop_title)
        title.append(item_title)
        table.setHorizontalHeaderLabels(title)

        for i in range(len(tb.shop_name)):
            if(self.tableWidget.rowCount() == i):
                self.tableWidget.insertRow(int(self.tableWidget.rowCount()))
            self.tableWidget.setItem(i,0, tb.shop_name[i])
            self.tableWidget.setItem(i,1, tb.item_price_list[i])

        self.item_price_total = tb.item_price_total
        self.item_price_mu = tb.item_price_mu
        self.item_price_sigma = tb.item_price_sigma
        '''
        # create a new Chrome session
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        #driver.maximize_window()

        # navigate to the application home page
        driver.get("https://login.taobao.com/member/login.jhtml?spm=a21wu.241046-my.754894437.1.4519fd50dPXaMM&f=top&redirectURL=https%3A%2F%2Fworld.taobao.com%2F%3Fspm%3Da21bp.8077467.1417485807582.1.6449e6bcStIj9X")

        # login to Taobao website
        username = driver.find_element_by_id("TPL_username_1")
        password = driver.find_element_by_id("TPL_password_1")
        username.send_keys("yenng3")
        password.send_keys("12345678abc")
        login = driver.find_element_by_id("J_SubmitStatic")
        login.click()

        self.tableWidget.setItem(0,0, QTableWidgetItem("Item (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Item (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Item (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Item (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Item (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Item (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Item (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Item (4,2)"))
        self.tableWidget.insertRow(int(self.tableWidget.rowCount()))
        x = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(x)'''
        
        
    def plot(self):
        x = self.item_price_total
        '''[17.5, 9.8, 5.88, 6.4, 21.8, 28.0, 9.9, 8.0, 26.0, 5.4, 5.3, 7.5, 5.8,
             8.7, 9.0, 5.4, 26.0, 18.9, 8.7, 18.0, 16.5, 9.7, 9.5, 25.0, 58.0, 147.0,
             5.4, 5.4, 5.4, 6.8, 5.5, 4.2, 18.0, 17.5, 18.0, 5.69, 5.55, 19.88, 95.0,
             15.9, 35.6, 9.8, 23.75, 24.51, 18.8, 9.0, 20.0, 15.0, 7.3, 7.3, 4.9, 5.66,
             9.85, 15.35, 15.9, 28.0, 7.99, 13.7, 10.0, 27.0, 8.65, 65.0, 39.0, 9.9,
             5.18, 5.4, 16.5, 11.8, 16.8, 13.5, 18.9, 69.0, 59.0, 23.9, 150.0, 13.5,
             60.0, 18.0, 11.2, 25.0, 9.0, 7.25, 24.99, 6.08, 3.6, 7.1, 11.5, 17.5,
             29.0, 21.0, 8.5, 198.0]'''
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
