from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import city, check_exists_by_xpath
import pandas as pd

URL = "https://www.tripadvisor.com/Search?q=" + city
driver = webdriver.Chrome('./chromedriver')
op = webdriver.ChromeOptions()

driver.get(URL)

things_to_do_page = driver.find_element(By.LINK_TEXT, "Things to do")
driver.execute_script("arguments[0].click();", things_to_do_page)
time.sleep(5)

places = driver.find_elements(By.CLASS_NAME, "location-meta-block")
print(len(places))

all_titles = []
all_rtexts = []
all_places = []

for elem, i in zip(places, range(0, len(places))):
    place_name = elem.text.split('\n')[0]
    print(place_name)

    attraction_button = elem.find_element(By.CLASS_NAME, "result-title")
    driver.execute_script("arguments[0].click();", attraction_button)
    time.sleep(10)

    print(driver.current_url)
    driver.switch_to.window(driver.window_handles[i+1])
    print(driver.current_url)

    # collecting n pages of reviews
    for j in range(0, 3):

        reviews_section = driver.find_element(By.CSS_SELECTOR, ".eSDnY")

        # collecting review titles
        titles = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.fiohW.qWPrE.ncFvv.fOtGX")
        for title in titles:
            all_titles.append(title.get_attribute("innerText"))

        # collecting review main texts
        rtexts = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.pZUbB.KxBGd")
        for rtext in rtexts:
            if rtext.get_attribute("innerText")[0:10] != "Review of:":
                all_rtexts.append(rtext.get_attribute("innerText"))

        all_rtexts.pop(j*10)    # removes unnecessary top of the page element with the same css selector

        if check_exists_by_xpath(reviews_section, "//a[contains(@aria-label, 'Next page')]"):
            next_review_page_button = reviews_section.find_element(By.XPATH, "//a[contains(@aria-label, 'Next page')]")
            driver.execute_script("arguments[0].click();", next_review_page_button)
            time.sleep(10)

        j += 1

    i += 1
    driver.switch_to.window(driver.window_handles[0])


print(len(all_titles))
print(len(all_rtexts))

reviews_dict = dict(zip(all_titles, all_rtexts))
reviews_pd = pd.DataFrame(reviews_dict.items(), columns=['Title', 'Review'])
reviews_pd.to_csv("trip_advisor_" + city + ".csv")


