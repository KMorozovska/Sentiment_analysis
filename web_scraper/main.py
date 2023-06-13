from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import city
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

for elem in places:
    place_name = elem.text.split('\n')[0]
    print(place_name)

    attraction_button = elem.find_element(By.CLASS_NAME, "result-title")
    driver.execute_script("arguments[0].click();", attraction_button)
    time.sleep(10)

    print(driver.current_url)
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)

    for i in range(0, 4):

        reviews_section = driver.find_element(By.CSS_SELECTOR, ".eSDnY")

        titles = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.fiohW.qWPrE.ncFvv.fOtGX")
        for title in titles:
            all_titles.append(title.get_attribute("innerText"))

        rtexts = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.pZUbB.KxBGd")
        for rtext in rtexts:
            if rtext.get_attribute("innerText")[0:10] != "Review of:":
                all_rtexts.append(rtext.get_attribute("innerText"))

        all_rtexts.pop(i*10)

        next_review_page_button = reviews_section.find_element(By.XPATH, "//a[contains(@aria-label, 'Next page')]")
        driver.execute_script("arguments[0].click();", next_review_page_button)
        time.sleep(10)

        # driver.switch_to.window(driver.window_handles[i])
        i += 1
        print('======== done ========')

    break

print(len(all_titles))
print(len(all_rtexts))

reviews_dict = dict(zip(all_titles, all_rtexts))
reviews_pd = pd.DataFrame(reviews_dict.items(), columns=['Title', 'Review'])
reviews_pd.to_csv("trip_advisor_" + city + ".csv")
