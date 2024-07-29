import booking.constants as const
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from booking.booking_filterations import BookingFiltration


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"/Users/henil/Downloads/chromedriver-mac-arm64/chromedriver", teardown=False):
        self.teardown = teardown
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def check_for_signin_info(self):
        signin_info = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[aria-label="Dismiss sign in information."]'
        )
        if signin_info.is_displayed():
            signin_info.click()

    def change_currency(self, currency="INR"):
        WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']"))
        )
        currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value="button[data-testid='header-currency-picker-trigger']"
        )
        currency_element.click()
        WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="selection-item"]'))
        )
        selected_currency_element = self.find_elements(
            by=By.CSS_SELECTOR,
            value='button[data-testid="selection-item"]'
        )
        for element in selected_currency_element:
            if re.search(f'{currency}', element.text) is not None:
                element.click()
                break

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(
            by=By.ID,
            value=':rh:'
        )
        search_field.clear()
        search_field.send_keys(place_to_go)
        # time.sleep(2) static 2 seconds wait...
        WebDriverWait(self, 5).until(
            EC.invisibility_of_element_located(
                (By.ID, 'group-0-heading')
            )
        )
        first_result = self.find_element(
            by=By.ID,
            value='autocomplete-result-0'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'span[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'span[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="occupancy-config"]').click()

        while True:
            decrease_count_element = self.find_element(by=By.XPATH, value='//*[@id=":ri:"]/div/div[1]/div[2]/button[1]')
            decrease_count_element.click()
            current_value_elem = self.find_element(by=By.ID,value='group_adults')
            current_value = current_value_elem.get_attribute('value')

            if int(current_value) == 1:
                break

        for _ in range(count-1):
            selection_elem = self.find_element(
                by=By.XPATH,
                value='//*[@id=":ri:"]/div/div[1]/div[2]/button[2]'
            )
            selection_elem.click()

    def click_search(self):
        button = self.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')
        button.click()

    def apply_alterations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_lowest_first()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.teardown:
            input("Waiting for conformation to teardown: ")
            self.quit()
