import variable_file
import functions
import webdriver_functions_file


if __name__ == '__main__':
    # 1 Request
    functions.check_website(variable_file.gigatron_base_url, variable_file.site_available_message,
                            variable_file.site_not_available_message)
    # 2 Request
    functions.display_searched_monitors()
    # webdriver_functions_file.display_searched_monitors_selenium() - Uncomment this line for additional UI check
    # for request 2

    # 3 Request
    functions.check_average_article_value_for_first_page()

    # 4 Request
    functions.show_desired_article()

    # 5 Request
    webdriver_functions_file.display_random_article_selenium()

    # 6. request
    functions.get_oldest_offer()
