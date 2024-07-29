# This file will include a class to interact with our website.
# After we have some results, to apply filtration.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filter_box = self.driver.find_element(by=By.ID, value='filter_group_class_:r2h:')
        star_child_elements = star_filter_box.find_elements(by=By.CSS_SELECTOR, value='*')

        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()

    def sort_price_lowest_first(self):
        button_sort = self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="sorters-dropdown-trigger"]')
        button_sort.click()
        self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-id="price"]').click()


