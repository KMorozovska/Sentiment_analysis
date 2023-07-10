from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time


def check_if_elem_exists(driver, by, name):
    try:
        driver.find_element(by, name)
    except NoSuchElementException:
        return False
    return True


def collect_reviews_from_single_location(driver, city, place_name):
    all_titles = []
    all_rtexts = []
    all_scores = []

    # collecting 3 pages of reviews
    for j in range(0, 3):

        reviews_section = driver.find_element(By.CSS_SELECTOR, ".eSDnY")

        # collecting review titles
        titles = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.fiohW.qWPrE.ncFvv.fOtGX")
        for title in titles:
            all_titles.append(title.get_attribute("innerText"))

        # collecting review scores
        scores = reviews_section.find_elements(By.CSS_SELECTOR, ".UctUV.d.H0")
        for score in scores:
            all_scores.append(score.get_attribute("ariaLabel"))
            print(score.get_attribute("ariaLabel"))

        # collecting review main texts
        rtexts = reviews_section.find_elements(By.CSS_SELECTOR, ".biGQs._P.pZUbB.KxBGd")
        for rtext in rtexts:
            if rtext.get_attribute("innerText")[0:10] != "Review of:":
                all_rtexts.append(rtext.get_attribute("innerText"))

        all_rtexts.pop(j * 10)  # removes unnecessary top of the page element with the same css selector

        # go to next page of reviews if next page exists
        if check_if_elem_exists(reviews_section, By.XPATH, "//a[contains(@aria-label, 'Next page')]"):
            next_review_page_button = reviews_section.find_element(By.XPATH, "//a[contains(@aria-label, 'Next page')]")
            driver.execute_script("arguments[0].click();", next_review_page_button)
            time.sleep(10)

        j += 1

    all_rtexts = all_rtexts[0:len(all_titles)]
    all_scores = all_scores[0:len(all_titles)]

    # save reviews for each location by appending to .csv
    single_place_reviews_df = pd.DataFrame(np.column_stack([all_titles, all_rtexts, all_scores]),
                                   columns=['Title', 'Review', 'Score'])
    single_place_reviews_df['City'] = city
    single_place_reviews_df['Location'] = place_name
    single_place_reviews_df.to_csv("trip_advisor_reviews_" + city + ".csv", mode='a', header=False, index=False)
