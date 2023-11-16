import config_file
import webdriver_config_file
import variable_file
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random
from selenium.common import TimeoutException


def click_cookie_button():
    try:
        cookie_button = WebDriverWait(webdriver_config_file.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, variable_file.accept_cookie_button)))
        cookie_button.click()
    except TimeoutException as e:
        config_file.logging.info(f"Timed out waiting for cookie button: {e}")


def display_searched_monitors_selenium():
    if variable_file.site_tittle in webdriver_config_file.driver.title:
        config_file.logging.info(variable_file.site_available_message)
        click_cookie_button()
        search_box = webdriver_config_file.driver.find_element(By.CSS_SELECTOR, variable_file.search_box_locator)
        search_box.send_keys("Monitor")
        search_box.send_keys(Keys.ENTER)
        try:
            WebDriverWait(webdriver_config_file.driver, 10).until(
                ec.presence_of_element_located((By.ID, variable_file.grid_products_locator)))
            config_file.logging.info("Search results are displayed.")
        except Exception as e:
            config_file.logging.info(f"Timeout exception for monitors displaying: {e}")
    else:
        config_file.logging.info(variable_file.site_not_available_message)
    webdriver_config_file.driver.quit()


def display_random_article_selenium():
    if variable_file.site_tittle in webdriver_config_file.driver.title:
        config_file.logging.info(variable_file.site_available_message)
        search_box = webdriver_config_file.driver.find_element(By.CSS_SELECTOR, variable_file.search_box_locator)
        search_box.send_keys("Laptop")
        search_box.send_keys(Keys.ENTER)
        click_cookie_button()
        displayed_laptops = WebDriverWait(webdriver_config_file.driver, 10).until(
            ec.visibility_of_element_located((By.ID, "grid-products")))
        displayed_laptops_child_elements = displayed_laptops.find_elements(By.XPATH, "*")
        random_chosen_laptop_element = random.choice(displayed_laptops_child_elements)
        random_chosen_laptop_child_element = random_chosen_laptop_element.find_element(By.XPATH, "*")
        laptop_data = random_chosen_laptop_child_element.text
        laptop_name = laptop_data.split("\n")[0]
        random_chosen_laptop_id = random_chosen_laptop_child_element.get_attribute("ID")
        appropriate_laptop_locator = f"#{random_chosen_laptop_id} > a.item__image > img"
        random_chosen_laptop = WebDriverWait(webdriver_config_file.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, appropriate_laptop_locator)))
        random_chosen_laptop.click()
        appropriate_xpath = f"//*[contains(text(), '{laptop_name}')]"
        try:
            WebDriverWait(webdriver_config_file.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, appropriate_xpath)))
            config_file.logging.info("An accurate random article was visited.")
        except TimeoutException:
            config_file.logging.info("There is an error related to the accuracy of the randomly chosen article.")
    else:
        config_file.logging.info(variable_file.site_not_available_message)
    webdriver_config_file.driver.quit()
