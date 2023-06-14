from selenium import webdriver
from collect_reviews_from_single_location import *


URL = "https://www.tripadvisor.com/Search?q=" + city
driver = webdriver.Chrome('./chromedriver')
op = webdriver.ChromeOptions()

driver.get(URL)

things_to_do_page = driver.find_element(By.LINK_TEXT, "Things to do")
driver.execute_script("arguments[0].click();", things_to_do_page)
time.sleep(5)

places = driver.find_elements(By.CLASS_NAME, "location-meta-block")
print(len(places))

reviews_pd = pd.DataFrame(columns=['Title', 'Review', 'Location'])
reviews_pd.to_csv("trip_advisor_reviews_" + city + ".csv")

for elem, i in zip(places, range(0, len(places))):
    place_name = elem.text.split('\n')[0]
    print(place_name)

    attraction_button = elem.find_element(By.CLASS_NAME, "result-title")
    driver.execute_script("arguments[0].click();", attraction_button)
    time.sleep(10)

    driver.switch_to.window(driver.window_handles[i+1])

    collect_reviews_from_single_location(driver, place_name)

    i += 1
    driver.switch_to.window(driver.window_handles[0])






