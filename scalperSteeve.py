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
# every variable is made to read from a file. The variable takes only what is inbetween the quotation marks from the designated line.
# The reading from a file is encapsulated in a try except block in order to check if everything is read correctly
try:
    read = open('info.txt')
    fileLines = read.readlines()
    first_name = fileLines[0][fileLines[0].index('"')+1:-2]
    last_name = fileLines[1][fileLines[1].index('"')+1:-2]
    receiver_email = fileLines[2][fileLines[2].index('"')+1:-2]
    phone_number = fileLines[3][fileLines[3].index('"')+1:-2]
    city = fileLines[4][fileLines[4].index('"')+1:-2]
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
    website = fileLines[22][fileLines[22].index('"')+1:-2]
    print("Information was correctly read")
except:
    print("Information wasn't correctly read")

# this creates a instance of the browser and then open a website

driver = webdriver.Firefox()
driver.get(website)

# takes the item name for later notifications

itemName = driver.find_element_by_class_name("sc_layouts_title_caption").text


# flag used for checking if the the addToCart button is or isn't there

foundButton = False

# function sent for notifying the user


def notification(itemName):
    return (itemName + " is currently in stock").encode()


# while loop to check for the add to cart button
# if true then stop and send a notification
# else sleep for 1 second refresh the page and make a new instance
# count the attempt and then print the number of the last attempt
while not foundButton:
    try:
        addToCartButton = driver.find_element_by_class_name(
            "single_add_to_cart_button ")
        print(notification(itemName))
        addToCartButton.click()
        foundButton = True
    except:
        time.sleep(1)
        driver.refresh()
        driver.get(website)
        counter = counter + 1
        print("didn't find the button, attemptNum: " + str(counter))

# sleep for 3 seconds and then go to the cart of the current website
# this is configured to work for the specific website and it won't work for other since every website is different and by that I mean the html, css and selectors used for each tag
# are unique for the website

cart = "https://stevesleaves.com/cart/"
time.sleep(3)
if foundButton:
    # using mail.py send the user an email through the burner email provided and then closes the email service
    mail.notify_user(notification(itemName))
    driver.get(cart)
    driver.find_element_by_class_name("checkout-button").click()
    # gets the input tag from the page and then simulates entering keys for the given strings
    # for somepages this works fine, but if the page uses an Iframe this approach won't work
    driver.find_element_by_id("billing_first_name").send_keys(first_name)
    driver.find_element_by_id("billing_last_name").send_keys(last_name)

    driver.find_element_by_id("billing_address_1").send_keys(address)
    driver.find_element_by_id("billing_postcode").send_keys(zip_code)
    driver.find_element_by_id("billing_city").send_keys(city)

    driver.find_element_by_class_name("select2-selection--single").text
    time.sleep(1)
    # this is used to simulate pressing/ selecting the state of the recepient
    # this approach won't work on everypage, as I said this is dependant on the structure of the page
    driver.find_elements_by_class_name("select2-selection--single")[0].click()
    states = driver.find_elements_by_class_name("select2-results__option")
    for state in states:
        if(state.text == state_of_rec):
            state.click()
            break

    time.sleep(0.5)
    driver.find_element_by_id("billing_email").send_keys(receiver_email)

    time.sleep(3)
    driver.find_element_by_class_name(
        "wc-credit-card-form-card-number").send_keys(number_on_card)
    driver.find_element_by_class_name(
        "wc-credit-card-form-card-expiry").send_keys(month)
    driver.find_element_by_class_name(
        "wc-credit-card-form-card-expiry").send_keys(year)
    driver.find_element_by_class_name(
        "wc-credit-card-form-card-cvc").send_keys(cvc)
    driver.find_element_by_id("place_order").click()
# if something doesn't work then print a failure message
else:
    print("failure at the end of the program")
