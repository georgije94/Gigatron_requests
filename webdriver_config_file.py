from selenium import webdriver
import variable_file

driver = webdriver.Chrome()
driver.get(variable_file.gigatron_base_url)
driver.maximize_window()
