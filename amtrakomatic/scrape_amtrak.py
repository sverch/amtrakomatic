"""
Functions to scrape the amtrak site.
"""

import csv
import os
import sys
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from amtrakomatic import fuzzy_match
from amtrakomatic import amtrak_results

logging.basicConfig(level=logging.INFO)

def load_amtrak_site(driver):
    """
    Load the amtrak homepage.
    """
    driver.get("https://www.amtrak.com/home.html")

def login(driver):
    """
    Log in to the configured amtrak account.
    """
    driver.find_element_by_xpath("//button[contains(text(),'Sign In')]").click()
    driver.find_element_by_name("_password").clear()
    driver.find_element_by_name("_password").send_keys(os.environ['AMTRAK_GUEST_REWARDS_PASSWORD'])
    driver.find_element_by_name("_name").clear()
    driver.find_element_by_name("_name").send_keys(os.environ['AMTRAK_GUEST_REWARDS_USERNAME'])
    driver.find_element_by_xpath("//button[contains(text(),'SIGN IN')]").click()

def fill_search_parameters(driver, source, dest, date):
    """
    Perform a search with the given parematers.
    """

    # I don't know why, but this selector is more reliable
    # I get:
    # selenium.common.exceptions.ElementNotInteractableException: Message: Element <input
    # class="search-station-field__inp form-input-with-label__inp
    # request-missing-points__ticket-form__input" name="wdf_origin" type="text"> could not be
    # scrolled into view
    def base_selector(name):
        return "(.//*[normalize-space(text()) and normalize-space(.)='%s'])" % name

    from_field = "%s[5]/following::input[2]" % base_selector("From")
    to_field = "%s[5]/following::input[2]" % base_selector("To")
    date_field = "%s[3]/following::input[1]" % base_selector("Depart")

    driver.find_element_by_xpath(from_field).click()
    driver.find_element_by_xpath(from_field).clear()
    driver.find_element_by_xpath(from_field).send_keys(fuzzy_match.station(source)[1])
    driver.find_element_by_xpath(to_field).click()
    driver.find_element_by_xpath(to_field).clear()
    driver.find_element_by_xpath(to_field).send_keys(fuzzy_match.station(dest)[1])
    driver.find_element_by_xpath(date_field).click()
    driver.find_element_by_xpath(date_field).clear()
    driver.find_element_by_xpath(date_field).send_keys(date)

    # Click this so that the date selection dialog goes away and we can click find trains.
    driver.find_element_by_xpath(from_field).click()

def select_points(driver):
    """
    Select search by points.
    """
    driver.find_element_by_xpath(
        "(.//*[contains(text(), 'Done')])[1]/following::span[5]").click()


def select_dollars(driver):
    """
    Select search by dollars.
    """
    driver.find_element_by_xpath(
        "(.//*[contains(text(), 'Done')])[1]/following::span[4]").click()

def search(driver):
    """
    Click search button to start search.
    """
    driver.find_element_by_id("findtrains").click()

def skip_dog_page(driver):
    """
    I don't have a dog.
    """
    dog_buttons = driver.find_elements_by_name(
        "_handler=amtrak.presentation.handler.request.rail.AmtrakAncillaryProductsRequestHandler")
    for dog_button in dog_buttons:
        dog_button.click()

def fill_passenger_information(driver):
    """
    Just skip travel insurance.  Note this assumes your profile is complete.
    """
    driver.find_element_by_xpath(
        "//span[contains(text(), 'No, I choose not to protect my')]").click()
    driver.find_element_by_xpath("//input[@value='Continue']").click()

def get_price(driver, use_points):
    """
    Get price from result page.
    """
    if use_points:
        return driver.find_element_by_id("total_points_redeemed")
    return driver.find_element_by_id("amtrakTotal")

# pylint: disable=too-many-arguments,too-many-locals
def get_search_results(driver, source, destination, date, using_points, train_name_to_click=None,
                       dump_html_source=False):
    """
    Assuming we are on search results page, get all the prices.
    """
    logging.debug("Finding pagination links")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Use beautiful soup to test if we have page links because it's much faster...
    if not soup.find("a", "pagination_page"):
        pagination_links = []
    else:
        pagination_links = driver.find_elements_by_xpath("//a[contains(@class, 'pagination_page')]")

    def handle_page(page):
        if dump_html_source:
            with open("%s_%s_%s_%s_%s.html" % (source, destination, date.replace("/", "_"),
                                               using_points, page), "w+") as source_dump:
                source_dump.write(driver.page_source)
        return amtrak_results.AmtrakResults.from_html(driver.page_source).results

    def check_for_ticket(name, results):
        ticket = None
        for result in results:
            for leg in result.legs:
                if leg["train_name"] == name:
                    ticket = result
                    break
        return ticket

    def click_on_ticket(ticket):
        add_to_cart_selector = "//input[@name=\"%s\"]" % ticket.add_to_cart_button_name_attribute
        price_selector = "//input[@value='%s']" % ticket.minimum_fare_value_attribute

        # There's a weird thing when searching for points where the result page looks like it's
        # completely duplicated but one of them is hidden.  Maybe be a round trip thing?
        def try_to_click_all(elements):
            last_exception = None
            for element in elements:
                try:
                    element.click()
                    return
                # pylint: disable=broad-except
                except Exception as exception:
                    last_exception = exception
            if last_exception:
                raise last_exception

        try_to_click_all(driver.find_elements_by_xpath(price_selector))
        try_to_click_all(driver.find_elements_by_xpath(add_to_cart_selector))

    results = []
    # Make sure we get all pages
    for page in range(1, len(pagination_links) + 1):
        logging.debug("Finding page %s", page)
        driver.find_element_by_xpath("//a[text()='%s']" % page).click()
        current_page_results = handle_page(page)
        if train_name_to_click:
            ticket = check_for_ticket(train_name_to_click, current_page_results)
            if ticket:
                click_on_ticket(ticket)
                return [ticket]
        results.extend(current_page_results)
    if not pagination_links:
        current_page_results = handle_page(0)
        if train_name_to_click:
            ticket = check_for_ticket(train_name_to_click, current_page_results)
            if ticket:
                click_on_ticket(ticket)
                return [ticket]
        results.extend(current_page_results)
    if train_name_to_click:
        raise Exception("Attempted to click on a train but did not find it: %s" % (
            train_name_to_click))
    return amtrak_results.AmtrakResults(results)

def get_all_fares(source, destination, date, use_points=False):
    """
    Get all prices for a given search.
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    load_amtrak_site(driver)
    fill_search_parameters(driver, source, destination, date)
    if use_points:
        select_points(driver)
    else:
        select_dollars(driver)
    search(driver)
    results = get_search_results(driver, source, destination, date, use_points)
    driver.quit()
    return results

# pylint: disable=too-many-arguments
def handle_specific_trip(driver, source, destination, date, name, use_points):
    """
    Does all the clicking an automation necessary to get the price for a specific trip.
    """
    fill_search_parameters(driver, source, destination, date)
    if use_points:
        select_points(driver)
    else:
        select_dollars(driver)
    search(driver)
    results = get_search_results(driver, source, destination, date, use_points, name)
    skip_dog_page(driver)
    fill_passenger_information(driver)
    return results, get_price(driver, use_points).text

def iterate_csv_trips(csv_trips_filename, interactive):
    """
    Given a CSV file, iterate all the trips by loading the actual page.
    """
    with open(csv_trips_filename) as amtrak_trips_file:
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        load_amtrak_site(driver)
        login(driver)
        load_amtrak_site(driver)
        reader = csv.reader(amtrak_trips_file, delimiter=',', quotechar='"')
        total_dollars = 0
        total_points = 0
        for search_info in reader:
            use_points = search_info[4].strip() == "points"
            load_amtrak_site(driver)
            if interactive:
                print(search_info)
                print("\n")
                print(handle_specific_trip(driver, search_info[0], search_info[1],
                                           search_info[2], search_info[3].rstrip(),
                                           use_points))
                print("\n")
                go_to_next = ""
                while go_to_next not in ["c"]:
                    go_to_next = input("Type \"c\" to continue, or CTRL-D to exit: ").lower()
                    if not go_to_next:
                        print("Exiting!")
                        sys.exit(0)
            else:
                ticket, price = handle_specific_trip(driver, search_info[0], search_info[1],
                                                     search_info[2], search_info[3].rstrip(),
                                                     use_points)
                print(search_info)
                if use_points:
                    ticket.pretty_print()
                    print("Price (points): %s" % price)
                    total_points = total_points + int(price.replace(",", ""))
                else:
                    ticket.pretty_print()
                    print("Price (dollars): %s" % price)
                    total_dollars = total_dollars + float(price.replace("$", "").replace(",", ""))
    print("Total point cost: %s" % total_points)
    print("Total dollar cost: %s" % total_dollars)
    driver.quit()
