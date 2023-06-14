from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from utils import city
import time


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def collect_reviews_from_single_location(driver, place_name):
    all_titles = []
    all_rtexts = []

    # collecting 3 pages of reviews
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

        all_rtexts.pop(j * 10)  # removes unnecessary top of the page element with the same css selector

        # go to next page of reviews if next page exists
        if check_exists_by_xpath(reviews_section, "//a[contains(@aria-label, 'Next page')]"):
            next_review_page_button = reviews_section.find_element(By.XPATH, "//a[contains(@aria-label, 'Next page')]")
            driver.execute_script("arguments[0].click();", next_review_page_button)
            time.sleep(10)

        j += 1

    # save reviews for each location by appending to .csv
    single_place_reviews_dict = dict(zip(all_titles, all_rtexts))
    single_place_reviews_df = pd.DataFrame(single_place_reviews_dict.items(), columns=['Title', 'Review'])
    single_place_reviews_df['Location'] = place_name
    single_place_reviews_df.to_csv("trip_advisor_reviews_" + city + ".csv", mode='a', header=False)
