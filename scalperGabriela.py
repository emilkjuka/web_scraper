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
try:
    read = open('info.txt')
    fileLines = read.readlines()
    first_name = fileLines[0][fileLines[0].index('"')+1:-2]
    last_name =fileLines[1][fileLines[1].index('"')+1:-2]
    receiver_email = fileLines[2][fileLines[2].index('"')+1:-2]
    phone_number = fileLines[3][fileLines[3].index('"')+1:-2]
    city =  fileLines[4][fileLines[4].index('"')+1:-2]
    state_of_rec = fileLines[5][fileLines[5].index('"')+1:-2]
    zip_code = fileLines[6][fileLines[6].index('"')+1:-2]
    address = fileLines[7][fileLines[7].index('"')+1:-2]
    name_on_card = fileLines[11][fileLines[11].index('"')+1:-2]
    type_of_card = fileLines[12][fileLines[12].index('"')+1:-2]
    number_on_card = fileLines[13][fileLines[13].index('"')+1:-2]
    month = fileLines[14][fileLines[14].index('"')+1:-2]
    year = fileLines[15][fileLines[15].index('"')+1:-2]
    expiery_date = fileLines[16][fileLines[16].index('"')+1:-2]
    cvc = fileLines[17][fileLines[17].index('"')+1:-2]
    website = fileLines[23][fileLines[23].index('"')+1:-2]
    print("Information was correctly read")
except:
    print("Information wasn't correctly read")


#creates an instance of a browser and opens the website
# https://www.gabriellaplants.com/collections/home-page/products/2-5-agave-victoria-reginae
#  https://www.gabriellaplants.com/products/3-philodendron-hederaceum-gabby?_pos=1&_sid=72c3fe61f&_ss

driver = webdriver.Firefox()
driver.get(website)


itemName = driver.find_element_by_class_name("entry-title").text



foundButton = False
# counter is for testing  
counter = 0


def notification(itemName):
        return (itemName + " is currently in stock")


while not foundButton:
    try:
        addToCartButton = driver.find_elements_by_class_name("single_add_to_cart_button")[0]
        print(notification(itemName))
        addToCartButton.click()
        foundButton = True
    except:
        time.sleep(1)
        driver.refresh()
        driver.get(website)
        counter = counter + 1
        print("didn't find the button, attemptNum: " + str(counter))
        
        
cart = "https://www.gabriellaplants.com/cart"

time.sleep(3)
if foundButton :
    mail.notify_user(notification(itemName))
    driver.find_elements_by_class_name("btn-checkout")[0].click()
    driver.find_element_by_id("checkout_email").send_keys(receiver_email)
   
    driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(first_name)
    driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(last_name)

    driver.find_element_by_id("checkout_shipping_address_address1").send_keys(address)
    driver.find_element_by_id("checkout_shipping_address_zip").send_keys(zip_code)
    driver.find_element_by_id("checkout_shipping_address_city").send_keys(city)
    driver.find_element_by_id("checkout_shipping_address_country").click()
    Select(driver.find_element_by_id("checkout_shipping_address_country")).select_by_value("United States")
    time.sleep(0.5)
    Select(driver.find_element_by_id("checkout_shipping_address_province")).select_by_visible_text(state_of_rec)
    

    time.sleep(2)
    
    
    driver.find_element_by_id("continue_button").click()
    time.sleep(2)
    driver.find_element_by_id("continue_button").click()
    time.sleep(2)
   
    
    print("Credit card phase: Please Input your information")

else :
    print("failure at the end of the program")