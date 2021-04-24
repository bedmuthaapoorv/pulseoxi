from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select

browser = Chrome("/home/apoorv/be miniproject/chromedriver")
browser.get('http://127.0.0.1:8050/')
print(browser.title)
#browser = Chrome()
#        browser.get('http://127.0.0.1:8050/')
inputdata2=[2014,75000,1,5,24.4,1120,71,'Jaipur','Diesel','Manual']
for i in range(1,11):
    username = browser.find_element_by_id("text"+str(i))
    username.send_keys(""+str(inputdata2[i-1]))
output=browser.find_element_by_id('output').text
while(output==""):
    output=browser.find_element_by_id('output').text
arr=output.split(' ')
try:
    print(float(arr[2]),"-> Test case passed")
except:
    print("test case failed")
