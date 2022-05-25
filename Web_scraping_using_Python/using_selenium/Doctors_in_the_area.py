#!/usr/bin/env python3

# Program : Web scraping using selenium web driver
# Author : Ramya Pozhath

"""
This program extracts the data such as 
the Name, Hospital address, Phone number and Speciality of all the doctors 
within 15 miles of the location corresponding to the zipcode entered (here 92126), 
from the webpage https://www.medicare.gov/care-compare/ and saves it to a csv file 
named Doctors_list.csv

"""

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np



website = "https://www.medicare.gov/care-compare/"

# Path of the selenium web driver stored in your system
webdriverpath = r"C:\Program Files (x86)\chromedriver.exe"
s = Service(webdriverpath)
driver = webdriver.Chrome(service = s)


driver.get(website)
time.sleep(3)

# Finding and closing the pop up
cross_button = driver.find_element(By.XPATH, """//*[@id="prefix-overlay-header"]/button""")
cross_button.click()

# Finding and clearing the location entry bar
location_bar = driver.find_element(By.XPATH, """//input[@data-placeholder="Street, ZIP code, city, or state"]""")
#location_bar.click()
location_bar.clear()


# Entering the zip code to the location entry bar
location_bar.send_keys("92126")
time.sleep(1)

# selecting from the autocomplete option
driver.switch_to.active_element
location_bar.send_keys(Keys.ARROW_DOWN)
location_bar.send_keys(Keys.ENTER)

time.sleep(1)

# Finding and clicking on the provider entry bar
provider_bar = driver.find_element(By.XPATH, """//*[@id="mat-select-value-1"]""")
provider_bar.click()

time.sleep(1)

# selecting the 'Doctors & clinicians' options from the dropd-down menu for the provider entry bar
driver.find_element(By.XPATH,"""//mat-option[@id="mat-option-1"]/span""" ).click()

time.sleep(1)


# Finding and clicking on the Search button
search_button = driver.find_element(By.XPATH, """//span[@class="ProviderSearchSearchButton__submit-text_wrapper"]""")
search_button.click()
time.sleep(2)


# Finding and clicking on the 'All' text link
all_link = driver.find_element(By.LINK_TEXT, "All")
all_link.click()


time.sleep(5)

name = []
speciality = []
address = []
phone = []

# Getting all the elements corresponding to the results
elements = driver.find_elements(By.XPATH, """//mat-card[@class="mat-card mat-focus-indicator ProviderSearchResultCardContainer__card d-flex"]""")

# Looping through all the elements and extracting the required fields
for ele in elements:
    name_ = ele.find_element(By.XPATH, """.//a[@routerlinkeventname="search_result_engaged"]""" )
    name.append(name_.text)
    spec_ = ele.find_element(By.XPATH,""".//div[@class="PhysicianSpecialties__primary mat-h5 ng-star-inserted"]""")
    speciality.append(spec_.text)
    try:
        phone_ = ele.find_element(By.XPATH,""".//div[2]/div[1]/div[3]/ccxp-address/div/div[2]/a""" )
        phone.append(phone_.get_attribute("innerHTML"))

    except:
        phone.append(np.nan)
        print("Element not found")
    
    address_ = ele.find_element(By.XPATH, """.//div[2]/div[2]/div/ccxp-address/div/div[1]""")
    address.append(address_.text)
 

# constructing dictionary of all the extracted data
my_dict = {"Name": name , "Address": address, "Phone": phone, "Speciality": speciality }

# constructing dataframe from the dictionary
df = pd.DataFrame(data=my_dict )

# Saving the dataframe to csv file.
df.to_csv("Doctors_list.csv", index=False)
