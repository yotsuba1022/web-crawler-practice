from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


TW_BANK_HOUSE_URL = 'http://www.bot.com.tw/house/default.aspx'
DRIVER_PATH = '../driver/'
CHROME_DRIVER = 'chromedriver'
PHANTOMJS_DRIVER = 'phantomjs'


def get_selenium_driver(execute_core):
    if execute_core == CHROME_DRIVER:
        # The chrome driver will launch chrome browser in your computer.
        return webdriver.Chrome(DRIVER_PATH + CHROME_DRIVER)
    elif execute_core == PHANTOMJS_DRIVER:
        # With PhantomJS, it will not trigger a real browser, instead, the crawler will run in background.
        return webdriver.PhantomJS(DRIVER_PATH + PHANTOMJS_DRIVER)
    else:
        return None


def init_selenium_driver(driver, url):
    driver.maximize_window()
    driver.set_page_load_timeout(60)
    driver.get(url)
    return driver


def launch_driver(driver, from_date, to_date):
    try:
        # Target the date fields and input date values.
        element = driver.find_element_by_id('fromdate_TextBox')
        element.send_keys(from_date)
        element = driver.find_element_by_id('todate_TextBox')
        element.send_keys(to_date)

        # Click the option list.
        driver.find_element_by_id('purpose_DDL').click()

        # Choose the specified option.
        for option in driver.find_elements_by_tag_name('option'):
            if option.text == '住宅':
                option.click()

        # Submit the form.
        element = driver.find_element_by_id('Submit_Button').click()

        # Wait until the result appear.
        element = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, 'House_GridView'))
        )

        # page_source will return the current content shown on browser.
        dom = BeautifulSoup(driver.page_source, 'html5lib')
        table = dom.find(id='House_GridView')
        for row in table.find_all('tr'):
            print([s for s in row.stripped_strings])
    finally:
        # Close the browser and finish the webdriver process.
        driver.quit()


def main():
    from_date = '1020101'
    to_date = '1060101'
    driver = get_selenium_driver(PHANTOMJS_DRIVER)
    if driver:
        driver = init_selenium_driver(driver, TW_BANK_HOUSE_URL)
        launch_driver(driver, from_date, to_date)
    else:
        print('Driver not found.')


if __name__ == '__main__':
    main()
