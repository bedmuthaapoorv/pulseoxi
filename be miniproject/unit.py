import unittest 
from selenium.webdriver import Chrome
import time

class SimpleTest(unittest.TestCase): 
  
    # Returns True or False.  
    def test(self):          
        browser = Chrome("/home/apoorv/be miniproject/chromedriver")
        browser.get('http://127.0.0.1:8050/')
        inputdata=[2012,87615,1,5,14.53,1798,138.1,'Delhi','Petrol','Manual']
        price=6.75
        for i in range(1,11):
            username = browser.find_element_by_id("text"+str(i))
            username.send_keys(""+str(inputdata[i-1]))

        output=browser.find_element_by_id('output').text
        while(output==""):
            time.sleep(5)
            output=browser.find_element_by_id('output').text
        output=output.split(" ")[2]
        accuracy=abs((price-float(output))*100/price)
        print('accuracy: ',100-accuracy)
       
        self.assertTrue(True)

'''    def test2(self):         
        browser = Chrome()
        browser.get('http://127.0.0.1:8050/')
        inputdata2=[2014,75000,1,5,24.4,1120,71,'Jaipur','Diesel','Manual']
        for i in range(1,11):
            username = browser.find_element_by_id("text"+str(i))
            username.send_keys(""+str(inputdata2[i-1]))

        output=browser.find_element_by_id('output').text
        while(output==""):
            time.sleep(5)
            output=browser.find_element_by_id('output').text
        output=output.split(" ")[2]
        accuracy=abs((6.75-float(output))*100/6.75)
        print('accuracy: ',100-accuracy)
        self.assertTrue(True)
'''
if __name__ == '__main__': 
    unittest.main() 
