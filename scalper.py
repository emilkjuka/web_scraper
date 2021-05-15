import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

driver.get("https://www.anhoch.com/product/599870452/gigabyte-geforce-rtx-3080-gaming-oc-10gb-gddr6x-2xhdmi3xdp-dx12u-rgb-windforce-3x")

addToCartButton = driver.find_element_by_class_name("add-to-cart")
foundButton = False

while not foundButton:  
    if("disabled" in addToCartButton.get_attribute("class")):
        time.sleep(10)
        driver.get("https://www.anhoch.com/product/599870452/gigabyte-geforce-rtx-3080-gaming-oc-10gb-gddr6x-2xhdmi3xdp-dx12u-rgb-windforce-3x")
        addToCartButton = driver.find_element_by_class_name("add-to-cart")
    else:
        foundButton=True

addToCartButton.click()




#https://www.anhoch.com/product/599867068/speaker-marshall-stockwell-ii-bluetooth-black
#https://www.anhoch.com/product/599870452/gigabyte-geforce-rtx-3080-gaming-oc-10gb-gddr6x-2xhdmi3xdp-dx12u-rgb-windforce-3x