from selenium import webdriver

option = webdriver.ChromeOptions()
#option.add_argument('headless')
web = webdriver.Chrome('chromedriver.exe',chrome_options=option)
web.get('https://tw.stock.yahoo.com/d/i/fgbuy_tse.html')


for i in web.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table[2]').find_elements_by_tag_name('a'):
    print(i.text)