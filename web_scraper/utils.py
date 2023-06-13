from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

city = 'Barcelona'
path_to_output_file = 'trip_advisor_'+city+'.csv'
pages_to_scrape = 1

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
