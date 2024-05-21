# imports
import time
import os
import multiprocessing
import random

# selenium for webdriver imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.service import Service

# data storing
import json
import gzip

import requests


# main element scraping funciton
def search(bot, cookies):

    # stores all data
    restaurant_data = []
    bot.get('https://food.grab.com/sg/en/')  # main url
    time.sleep(2)

    # set cookies to the browser
    for name, value in cookies.items():
        bot.add_cookie({"name": name, "value": value})
    time.sleep(2)

    bot.refresh()  # Refresh the page to apply cookies(input updates)

    # search button to trigger restaurants list
    search_button = WebDriverWait(bot, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[3]/div/button")))
    search_button.click()

    time.sleep(10)

    count = 0   # count hold the last element scrapped!

    for i in range(0, 20):  # change 20 according to the data requirement each loop may get 20 to 30 restaurants!

        i += 1  # loop update

        # checks for all the available restaurants
        restaurant_elements = WebDriverWait(bot, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.RestaurantListCol___1FZ8V")))

        # scroll to fetch the next batch
        print(restaurant_element)
        last_restaurant_element = restaurant_elements[-1]
        bot.execute_script(
            "arguments[0].scrollIntoView();", last_restaurant_element)
        time.sleep(5)

        # scrape the required data
        for restaurant_element in restaurant_elements[count:]:
            count = count+1
            try:
                restaurant_cuisine = restaurant_element.find_element(
                    By.CSS_SELECTOR, "div.basicInfoRow___UZM8d").text
                restaurant_name = restaurant_element.find_element(
                    By.CSS_SELECTOR, "p.name___2epcT").text
                rating = restaurant_element.find_element(
                    By.CSS_SELECTOR, "div.numbersChild___2qKMV:nth-child(1)").text
                duration_distance = restaurant_element.find_element(
                    By.CSS_SELECTOR, "div.numbersChild___2qKMV:nth-child(2)").text
                image_element = WebDriverWait(bot, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.show___3oA6B")))
                image_url = image_element.get_attribute("src")
                restaurant_id = restaurant_element.find_element(
                    By.CSS_SELECTOR, "a").get_attribute("href").split('/')[-1][:-1]

                # get lat_long:

                url = "https://portal.grab.com/foodweb/v2/merchants/{}?latlng=1.396364,103.747462".format(
                    restaurant_id)
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse the HTML content of the response
                    soup = json.loads(response.text)

                    # Extract the latitude and longitude data
                    latitude = soup['merchant']['latlng']['latitude']
                    longitude = soup['merchant']['latlng']['longitude']
                    eta = soup['merchant']['ETA']
                    estimatedDeliveryFee = soup['merchant']['estimatedDeliveryFee']

                else:
                    latitude = "couldnt get lat"
                    longitude = "coudnt get long"

                # Check if promo element exists
                try:
                    promo_element = restaurant_element.find_element(
                        By.CSS_SELECTOR, "p.promoText___2LmzI")
                    promo_available = "True"
                except NoSuchElementException:
                    promo_available = "False"

                # Check if offers element exists
                try:
                    offers_element = restaurant_element.find_element(
                        By.CSS_SELECTOR, "span.discountText___GQCkj")
                    offers = offers_element.text
                except NoSuchElementException:
                    offers = "No discount"

                # Check if notice element exists
                try:
                    notice_element = restaurant_element.find_element(
                        By.CSS_SELECTOR, "p.closeSoon___1eGf8")
                    notice = notice_element.text
                except NoSuchElementException:
                    notice = "No promo"

                # Create a dictionary for the restaurant data
                restaurant_dict = {
                    "Restaurant Id": restaurant_id,
                    "Restaurant Name": restaurant_name,
                    "Cuisine": restaurant_cuisine,
                    "Rating": rating,
                    "Duration": duration_distance,
                    "Promo": promo_available,
                    "restaurant_id": restaurant_id,
                    "offers": offers,
                    "notice": notice,
                    "image_url": image_url,
                    "latitude": latitude,
                    "longitude": longitude,
                    "Estimate time of delivery": eta,
                    "Estimated Delivery Fee": estimatedDeliveryFee
                }

                # Append the dictionary to the list
                restaurant_data.append(restaurant_dict)

            except NoSuchElementException:
                continue

    # Write the list of dictionaries to a newline-delimited JSON file
    with gzip.open(f"restaurant_data_{multiprocessing.current_process().name}.ndjson.gz", "wt", encoding="utf-8") as f:
        for data in restaurant_data:
            json.dump(data, f)
            f.write('\n')

    time.sleep(20)
 # scrape function to initialization of webdriver bot


def scrape(cookies):

    # initialize selenium webdriver
    service = Service()
    options = webdriver.ChromeOptions()
    selected_user_agent = "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    options.add_argument(f"user-agent={selected_user_agent}")

    # initialize bot
    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15)

    search(bot, cookies)

    bot.quit()
# this function handles the process with different data


def start_process():

    cookies_list = [{
        "gfc_country": "SG",
        "gfc_session_guid": "694226c1-b9c1-4b47-89a7-0d98fc4abe21",
        "next-i18next": "en",
        "_gsvid": "1a6fec89-c5b1-421e-a7cb-21586fcb3a1e",
        "_gcl_au": "1.1.701740744.1715357490",
        "hwuuid": "adc3d9c5-d28c-4470-8cd5-1d400945a0ff",
        "hwuuidtime": "1715357540",
        "_ga": "GA1.1.1032334565.1715454609",
        "location": '{"id":"IT.064IKGTYU624R","latitude":1.367476,"longitude":103.858326,"address":"Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456","countryCode":"SG","isAccurate":true,"addressDetail":"Chong Boon Dental Surgery - Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456","noteToDriver":"","city":"Singapore City","cityID":6,"displayAddress":"Chong Boon Dental Surgery - Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456"}',
        "pid": "www.google.com",
        "c": "non-paid",
        "_gssid": "2404151150-xial46y7nxr",
        "_ga_RPEHNJMMEM": "GS1.1.1715773927.6.0.1715773927.60.0.995007504"
    },
        {
        "gfc_country": "SG",
        "gfc_session_guid": "694226c1-b9c1-4b47-89a7-0d98fc4abe21",
        "next-i18next": "en",
        "_gsvid": "1a6fec89-c5b1-421e-a7cb-21586fcb3a1e",
        "_gcl_au": "1.1.701740744.1715357490",
        "hwuuid": "adc3d9c5-d28c-4470-8cd5-1d400945a0ff",
        "hwuuidtime": "1715357540",
        "_ga": "GA1.1.1032334565.1715454609",
        "location": '{"id": "IT.2EPYOYVWDKGU3", "latitude": 1.396364,"longitude": 103.747462,"address": "Choa Chu Kang North 6, Singapore, 689577","countryCode": "SG", "isAccurate": true, "addressDetail": "PT Singapore - Choa Chu Kang North 6, Singapore, 689577", "noteToDriver": "", "city": "Singapore City", "cityID": 6, "displayAddress": "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"}',
        "pid": "www.google.com",
        "c": "non-paid",
        "_gssid": "2404151909-niaypmwmt29",
        "_ga_RPEHNJMMEM": "GS1.1.1715800156.7.1.1715800314.54.0.1428779389"
    }]
    processes = []
    for idx, cookies in enumerate(cookies_list, start=1):
        process = multiprocessing.Process(
            target=scrape, args=(cookies,), name=f"Process-{idx}")
        processes.append(process)

    # Start each process
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()


# this code excutes 1st
if __name__ == '__main__':
    TIMEOUT = 15
    start_process()
