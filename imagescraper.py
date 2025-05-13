import requests
# import beautiful soup for webscraping
from bs4 import BeautifulSoup

# import selenium for loading pages properly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
# time for delays
import time

# urls
# site uses relative urls, keep track of base url to actually visit it
base_url = "https://en.cf-vanguard.com"
# url = "https://en.cf-vanguard.com/cardlist/cardsearch/?expansion=5"
# url = input("Please enter official vanguard set url: ")
# [3,43] - 11
for vcl in range (34, 34):
    url = "https://en.cf-vanguard.com/cardlist/cardsearch/?expansion=" + str(vcl)


    # First, since the site is loaded dynamically,
    # we can use selenium to ensure all the cards are loaded
    # before we continue with the webscraping

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # let page load
    time.sleep(5)

    # time amount between attempts to load by scrolling
    scroll_pause_time = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll to bottom, wait, check new scroll height and compare
        # if theres more to scroll continue, else break out

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Selenium has completed page loading via scrolling")

    # use the page selenium loads to webscrape
    card_list_div = driver.find_element


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    card_list_div = soup.find('div', class_='cardlist_gallerylist')

    card_links = card_list_div.find_all('a')
    all_links = []
    for card in card_links:
        all_links.append(base_url + card['href'])


    card_images = []

    i = 0
    for link in all_links:
        page_response = requests.get(all_links[i])

        card_soup = BeautifulSoup(page_response.text, 'html.parser')
        card_image_div = card_soup.find('div', class_='main')
        if card_image_div:
            card_image_tag = card_image_div.find('img')
            card_images.append(base_url + card_image_tag['src'])

        else:
            print("Error finding card image")
        i+=1

    print(f"Got image links for: {url}")

    with open("D:\\VanguardImages\\" + str(vcl) + ".txt", "w", newline="") as file:
        for l in card_images:
            file.write(l)
            file.write("\n")

    driver.quit()
