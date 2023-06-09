from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import city

URL = "https://www.tripadvisor.com/Search?q="+city
driver = webdriver.Chrome('./chromedriver')
op = webdriver.ChromeOptions()

driver.get(URL)

things_to_do_page = driver.find_element(By.LINK_TEXT, "Things to do")
driver.execute_script("arguments[0].click();", things_to_do_page)
time.sleep(5)

places = driver.find_elements(By.CLASS_NAME, "location-meta-block")
print(len(places))

for elem in places:
    print(elem.text)

    attraction_button = elem.find_element(By.CLASS_NAME, "result-title")
    driver.execute_script("arguments[0].click();", attraction_button)
    time.sleep(10)

    print(driver.current_url)
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)

    #review_score = driver.find_element(By.CSS_SELECTOR, ".UctUV.d.H0")
    #print(review_score.get_attribute("aria_label"))
    review_title = driver.find_element(By.CSS_SELECTOR, ".yCeTE")
    print(review_title.get_attribute("outerText"))
    review_text = driver.find_element(By.CSS_SELECTOR, "._T.FKffI.bmUTE")
    print(review_text.get_attribute("outerText"))

    print('done')