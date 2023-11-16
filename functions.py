import variable_file
import concurrent.futures
import config_file
import requests

first_page_monitors_response = requests.get(variable_file.search_url_for_first_page)
monitors = first_page_monitors_response.json()
numberOfMonitors = monitors["limit"]
articles = monitors.get("hits", {}).get("hits", [])
price_list = []


def check_website(url, successful_message, unsuccessful_message):
    try:
        site_response = requests.get(url)
        site_response.raise_for_status()
        config_file.logging.info(successful_message)
        return True
    except requests.exceptions.RequestException as e:
        config_file.logging.info(f"{unsuccessful_message} {e}")
        return False


def display_searched_monitors():
    site_response = requests.get(variable_file.gigatron_base_url)
    if site_response.status_code == 200:
        if len(articles) > 0:
            config_file.logging.info("Monitors are: ")
            for i in range(numberOfMonitors):
                monitor_names = monitors["hits"]["hits"][i]["_source"]["search_result_data"]["name"]
                config_file.logging.info(f"{monitor_names}")
        else:
            config_file.logging.info("There are no articles on this page")
    else:
        config_file.logging.info(variable_file.site_not_available_message)


def check_average_article_value_for_first_page():
    sum_price = 0
    if len(articles) > 0:
        for i in range(numberOfMonitors):
            price = monitors["hits"]["hits"][i]["_source"]["search_result_data"]["price"]
            price_list.append(float(price))
            sum_price += float(price)
        average_price = sum_price / numberOfMonitors
        config_file.logging.info(f"Average price is: {average_price}")
        return average_price
    else:
        config_file.logging.info("There are no articles on this page")


def show_desired_article():
    price_and_monitor_list = []
    average_price = check_average_article_value_for_first_page()
    for i in range(numberOfMonitors):
        price = monitors["hits"]["hits"][i]["_source"]["search_result_data"]["price"]
        monitor_name = monitors["hits"]["hits"][i]["_source"]["search_result_data"]["name"]
        price_and_monitor_list.append({"name": monitor_name, "price": float(price)})
    if numberOfMonitors % 2 == 0:
        unique_sorted_prices = sorted(set(item["price"] for item in price_and_monitor_list))
        if len(unique_sorted_prices) > 1:
            second_min_price = unique_sorted_prices[1]
            second_min_monitor = next((item["name"] for item in price_and_monitor_list if item["price"] ==
                                       second_min_price), None)
            config_file.logging.info(f"The second cheapest price is: {second_min_price} for the monitor: "
                                     f"{second_min_monitor}")
        else:
            config_file.logging.info("Number of prices is less than 1")
    else:
        closest_price = min(price_list, key=lambda x: abs(x - average_price))
        for monitor in monitors["hits"]["hits"]:
            current_price = float(monitor["_source"]["search_result_data"]["price"])
            if current_price == closest_price:
                closest_price_monitor = monitor
                closest_price_monitor_name = closest_price_monitor["_source"]["search_result_data"]['name']
                config_file.logging.info(
                    f"The closest article to average price is: {closest_price_monitor_name}"
                    f" with price {closest_price}")


def get_offers(page):
    url_action_offers_for_all_pages = "https://api-v2.gigatron.rs/core/news/get/2/" + str(
        page) + "?uid=giga65510d81a49ba4.33483555"
    response = requests.get(url_action_offers_for_all_pages)
    offers = response.json()["items"]
    return offers


def get_oldest_offer():
    response = requests.get(variable_file.action_offers_url)
    if response.status_code == 200:
        total_pages = response.json()['total_pages']
        oldest_offer_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            offers_per_page = executor.map(get_offers, range(total_pages))
        for offers in offers_per_page:
            if offers:
                oldest_offer = min(offers, key=lambda x: x["date"])
                oldest_offer_list.append(oldest_offer)
            else:
                config_file.logging.info("There are no offers on the Action page.")
        oldest_offer_for_all_pages = min(oldest_offer_list, key=lambda x: x['date'])
        title_oldest_offer = oldest_offer_for_all_pages['title']
        time_ago_oldest_offer = oldest_offer_for_all_pages['time_ago']
        config_file.logging.info(f"The oldest offer in Actions section is:'{title_oldest_offer}'"
                                 f" with the start of the action: {time_ago_oldest_offer}")
    else:
        config_file.logging.info("Error with getting the offers on the Action page.")
