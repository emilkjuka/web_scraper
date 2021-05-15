from contextlib import nullcontext
from logging import exception
import mail
import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


# variables : readed from the info.file for conv 
read = open('info.txt')
fileLines = read.readlines()
first_name = fileLines[0][fileLines[0].index('"')+1:-2]
last_name =fileLines[1][fileLines[1].index('"')+1:-2]
receiver_email = fileLines[2][fileLines[2].index('"')+1:-2]
phone_number = fileLines[3][fileLines[3].index('"')+1:-2]
city =  fileLines[4][fileLines[4].index('"')+1:-2]
state = fileLines[5][fileLines[5].index('"')+1:-2]
zip_code = fileLines[6][fileLines[6].index('"')+1:-2]
address = fileLines[7][fileLines[7].index('"')+1:-2]
name_on_card = fileLines[11][fileLines[11].index('"')+1:-2]
type_of_card = fileLines[12][fileLines[12].index('"')+1:-2]
number_on_card = fileLines[13][fileLines[13].index('"')+1:-2]
month = fileLines[14][fileLines[14].index('"')+1:-2]
year = fileLines[15][fileLines[15].index('"')+1:-2]
expiery_date = fileLines[16][fileLines[16].index('"')+1:-2]
cvc = fileLines[17][fileLines[17].index('"')+1:-2]

#creates an instance of a browser and opens the website
# "https://www.lechuza.us/accessories-lechuza-pon/lechuza-pon-1.4-us.dry.gal/19561.html#cgid=Substrate"
driver = webdriver.Firefox()
website = "https://www.lechuza.us/trend/cube-color-14-white/13380.html#cgid=Tischgefaesse"
driver.get(website)


itemName = driver.find_elements_by_class_name("product-heading")[1].text

foundButton = False
# counter is for testing  
counter = 0


def notification(itemName):
    if foundButton == True:
        return itemName + " is currently in stock"
    else : 
        return itemName + " is currently not in stock"

while not foundButton:
    try:
        addToCartButton = driver.find_element_by_id("add-to-cart")  
        print("found the button")
        addToCartButton.click()
        foundButton = True
    except:
        time.sleep(1)
        driver.refresh()
        driver.get(website)
        counter = counter + 1
        print("didn't find the button, attemptNum: " + str(counter))
        if counter == 50:
            break
        


if foundButton :
    # mail.notify_user(notification(itemName))
    driver.get("https://www.lechuza.us/cart/")
    # select = Select(driver.find_element_by_name('dwfrm_cart_shipments_i0_items_i0_quantity'))
    # select.select_by_visible_text("1")
    checkOutBtn = driver.find_elements_by_class_name("cart-action-checkout")
    checkOutBtn[1].click()
    checkOutAsGuest = driver.find_element_by_name("dwfrm_login_unregistered")
    checkOutAsGuest.click()
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_firstname").send_keys(first_name)
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_lastname").send_keys(last_name)
    # driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_companyname").send_keys("e")
    # time.sleep(1)
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_address1").send_keys(address)
    
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_zip").send_keys(zip_code)
    
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_city").send_keys(city)
    
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_addressFields_phone").send_keys(phone_number)
    
    driver.find_element_by_id("dwfrm_singleshipping_billingAddress_email_emailAddress").send_keys(receiver_email)
    
    driver.find_elements_by_name("dwfrm_singleshipping_shippingAddress_save")[1].click()

else :
    print("failure at the end of the program")