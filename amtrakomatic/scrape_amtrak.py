"""
Functions to scrape the amtrak site.
"""

import csv
import os
import sys
import logging
from collections import namedtuple
from enum import Enum
import time
from selenium import webdriver
import selenium
from amtrakomatic import fuzzy_match
from amtrakomatic import amtrak_results

logging.basicConfig(level=logging.INFO)

Selector = namedtuple('Selector', ['type', 'query'])
class SelectorType(Enum):
    """
    Type of selector that this is, so we know which function to pass the query to.
    """
    ID = "find_element_by_id"
    NAME = "find_element_by_name"
    XPATH = "find_element_by_xpath"
    XPATH_MULTIPLE = "find_elements_by_xpath"

def class_selector(class_string):
    """
    https://stackoverflow.com/a/9133579
    """
    return '[contains(concat(" ", normalize-space(@class), " "), " %s ")]' % class_string

def class_selectors(class_strings):
    """
    https://stackoverflow.com/a/9133579
    """
    return '[%s]' % ' and '.join(
        ['contains(concat(" ", normalize-space(@class), " "), " %s ")' % class_string
            for class_string in class_strings])

selector_map = {
    'Homepage.Sign_In': Selector(SelectorType.XPATH, "//button[contains(text(),'Sign In')]"),
    'Homepage.From': Selector(SelectorType.XPATH, '//*[@id="mat-input-0"]'),
    'Homepage.To': Selector(SelectorType.XPATH, '//*[@id="mat-input-1"]'),
    # Note: I believe if you click on the return date field, it rerenders them both and this changes
    # to "mat-input-3" because it becomes a "round trip" automatically.
    'Homepage.Depart_Date': Selector(SelectorType.XPATH, '//*[@id="mat-input-2"]'),
    'Homepage.Use_Points_Toggle': Selector(SelectorType.XPATH, '//*[@id="mat-checkbox-2-input"]'),
    'Homepage.Search_Button': Selector(SelectorType.XPATH, '//*[@title="FIND TRAINS"]'),
    'Login.Password': Selector(SelectorType.NAME, "_password"),
    'Login.Name': Selector(SelectorType.NAME, "_name"),
    'Login.Sign_In': Selector(SelectorType.NAME, "//button[contains(text(),'SIGN IN')]"),
    'Date_Popup.Done': Selector(SelectorType.XPATH, "//button[contains(text(),'Done')]"),
    'Results.Pages': Selector(SelectorType.XPATH_MULTIPLE,
        "//li%s" % class_selector('pagination-page')),
    'Results.NextPage': Selector(SelectorType.XPATH, "//li%s" % class_selector('pagination-next')),
    'Results.LegContainer': Selector(SelectorType.XPATH_MULTIPLE,
        "//div%s" % class_selector('search-results-leg')),
    'Results.DetailsLink': Selector(SelectorType.XPATH_MULTIPLE,
        "//span[contains(text(), 'Details')]"),
    'Results.DetailsBody': Selector(SelectorType.XPATH,
        "//div%s" % class_selector('details-modal-container')),
    'Results.CloseDetails': Selector(SelectorType.XPATH,
        "//button%s" % class_selectors(['close', 'pull-right'])),
        }

def find(driver, selector_name, exit_on_error=True):
    """
    Search for the given selector and log failure, where the name is more semantic in meaning than
    the raw path needed to actually find it in the page.
    """
    selector = selector_map[selector_name]
    logging.debug("Searching for %s using driver.%s(\"%s\")", selector_name, selector.type,
            selector.query)
    selector_fn = getattr(driver, selector.type.value)
    try:
        return selector_fn(selector.query)
    except selenium.common.exceptions.NoSuchElementException as exception:
        logging.error("Searching for %s using driver.%s(\"%s\") recieved exception: %s",
                selector_name, selector.type, selector.query, exception)
        if exit_on_error:
            sys.exit(1)
        else:
            return None
def click_when_obscured(driver, element):
    """
    I can't do the normal click in many cases because somehow something is obscuring it.
    See https://stackoverflow.com/a/64499144 for workaround.
    """
    driver.execute_script("arguments[0].click();", element)

def load_amtrak_site(driver):
    """
    Load the amtrak homepage.
    """
    driver.get("https://www.amtrak.com/home.html")

def login(driver):
    """
    Log in to the configured amtrak account.
    """
    find(driver, "Homepage.Sign_In").click()
    find(driver, "Login.Password").clear()
    find(driver, "Login.Password").send_keys(os.environ['AMTRAK_GUEST_REWARDS_PASSWORD'])
    find(driver, "Login.Name").clear()
    find(driver, "Login.Name").send_keys(os.environ['AMTRAK_GUEST_REWARDS_USERNAME'])
    find(driver, "Login.Sign_In").click()

def fill_search_parameters(driver, source, dest, date):
    """
    Perform a search with the given parematers.
    """
    find(driver, "Homepage.From").click()
    find(driver, "Homepage.From").clear()
    find(driver, "Homepage.From").send_keys(fuzzy_match.station(source)[1])
    find(driver, "Homepage.To").click()
    find(driver, "Homepage.To").clear()
    find(driver, "Homepage.To").send_keys(fuzzy_match.station(dest)[1])
    find(driver, "Homepage.Depart_Date").click()
    find(driver, "Homepage.Depart_Date").clear()
    find(driver, "Homepage.Depart_Date").send_keys(date)

    # Click this so that the date selection dialog goes away and we can click find trains.
    find(driver, "Date_Popup.Done").click()

def select_points(driver):
    """
    Select search by points.
    """
    toggle = find(driver, "Homepage.Use_Points_Toggle")
    if not toggle.get_attribute("aria-checked"):
        toggle.click()

def select_dollars(driver):
    """
    Select search by dollars.
    """
    toggle = find(driver, "Homepage.Use_Points_Toggle")
    if toggle.get_attribute("aria_checked"):
        toggle.click()

def search(driver):
    """
    Click search button to start search.
    """
    find(driver, "Homepage.Search_Button").click()

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
def get_search_results(driver, source, destination, date, using_points, dump_html_source=False):
    """
    Assuming we are on search results page, get all the prices.
    """
    logging.debug("Finding pagination links")
    # I think this needs to be here because of a brief animation that plays when the results page
    # shows up.
    time.sleep(1)
    pagination_links = find(driver, "Results.Pages")

    def handle_page(page):
        page_results = []
        time.sleep(1)
        legs = find(driver, "Results.LegContainer")
        details_links = find(driver, "Results.DetailsLink")
        time.sleep(1)
        for index, (leg, details_link) in enumerate(zip(legs, details_links)):
            time.sleep(0.5)
            driver.execute_script("arguments[0].scrollIntoView();", details_link)
            click_when_obscured(driver, details_link)
            result_html = leg.get_attribute('innerHTML')
            details_html = find(driver, "Results.DetailsBody").get_attribute('innerHTML')
            # I have this here because it makes it easier to generate test cases
            if dump_html_source:
                with open("%s_%s_%s_%s_%s_%s_result.html" % (source, destination, date.replace("/",
                    "_"), using_points, page, index), "w+") as source_dump:
                    source_dump.write(result_html)
                with open("%s_%s_%s_%s_%s_%s_details.html" % (source, destination, date.replace("/",
                    "_"), using_points, page, index), "w+") as source_dump:
                    source_dump.write(details_html)
            time.sleep(0.5)
            click_when_obscured(driver, find(driver, "Results.CloseDetails"))
            page_results.append(amtrak_results.AmtrakResult.from_result_and_details(
                result_html, details_html))
        return page_results

    results = []
    for page, _ in enumerate(pagination_links):
        results.extend(handle_page(page))
        if (page + 1) < len(pagination_links):
            # There's crap at the bottom of the page, so just scroll to the bottom every time to not
            # have stuff obscured. See https://stackoverflow.com/a/27760083.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            find(driver, "Results.NextPage").click()
    #print(results)
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
                ticket, price = handle_specific_trip(driver, search_info[0], search_info[1],
                                                     search_info[2], search_info[3].rstrip(),
                                                     use_points)
                print(price)
                ticket.pretty_print()
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
