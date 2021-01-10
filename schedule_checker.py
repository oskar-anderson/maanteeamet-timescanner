"""Read readme."""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from time import sleep
from typing import *
import re

# local imports
# ====================
from util.alert import Alert
from util import constants, helper
from model.accountLoginDetails import AccountLoginDetails
from model.available_reservation import Reservation
# ====================


def find_good_times(good_cities: List[str],
                    before_date: datetime,
                    times: List[Reservation],
                    old_good_times: List[Reservation]
                    ) -> List[Reservation]:
    good_cities = [x.lower() for x in good_cities]
    new_good_times = [x for x in times if
                      x.place.lower() in good_cities and
                      x.date <= before_date and
                      x not in old_good_times]
    return new_good_times


def wait_for_user_to_close_calender():
    print("Input \"Y\" when you have logged into the website and gone to "
          "\"Juhtimisõiguse ja esmase juhiloa taotlemine\" "
          "-> \"B-kategooria sõidueksam\" "
          "-> \"Muuda valikut\". "
          "Click on \"Kus saab kõige kiiremini eksamile?\" and close the pop-up calender.")
    user_input = input("calender is closed/exit? (Y/N)>").upper()
    if user_input == "Y":
        return
    else:
        exit()


def private_data_scraper(driver: WebDriver, main_page: str) -> List[Reservation]:
    """
    For getting info uses Maanteeamet e-service's strange web function where first available times in every city are loaded
    once user clicks on "Kus saab kõige kiiremini eksamile?" but once the popup is closed they will not
    be loaded on the same page again.
    If the user then left clicks on the button and opens a new tab of the Maanteeamet e-service,
    the new tab will be loaded with the calender popup.
    """
    # todo find out why the id's change and find a more permanent solution - regex?
    xpaths: List[str] = [
        "//*[@id=\"j_idt106:j_idt127:j_idt135\"]",
        "//*[@id=\"j_idt106:j_idt109:j_idt117\"]"
    ]
    reserve_time: WebElement = None
    for index, xpath in enumerate(xpaths, start=0):
        try:
            reserve_time = driver.find_element_by_xpath(xpath)
            print(f"Used xpath number: {index}, value: {xpath}")
        except NoSuchElementException:
            if index == len(xpaths) - 1:
                print("Navigation error")
                exit()
    assert (reserve_time.text == "Kus saab kõige kiiremini eksamile?")
    reserve_time.click()
    driver.execute_script("window.open("");")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(main_page)
    # find popup calender data.
    times: WebElement = driver.find_element_by_xpath("//*[@id=\"varaseimadEksamiajadForm\"]/ul")
    driver.close()
    # although window was closed, window 1 is still the active one.
    driver.switch_to.window(driver.window_handles[0])

    list_times_raw: List[str] = times.text.replace(" »", "").split("\n")
    list_times: List[Reservation] = helper.parse_list_times(list_times_raw)
    return list_times


def time_scanner(use_public_data: bool):
    """
    Main function. Use Selenium to automate Google Chrome and process extracted info.

    :type use_public_data:
    Whether to use times from Maanteeamet private reservation page (requires login)
    or use public available data.
    Program is more likely to work with public data,
    since private data scraping functionality was done back in Dec 2019,
    when only 3 months were available for reservation - the website has likely changed.
    """
    driver: WebDriver = webdriver.Chrome("chromedriver.exe")
    if use_public_data:
        main_page: str = "https://eteenindus.mnt.ee/public/vabadSoidueksamiajad.xhtml"
    else:
        main_page: str = "https://eteenindus.mnt.ee/pages/juht/juhiloataotlus/juhiloaTaotlus.jsf"
    driver.get(main_page)

    userdata: dict = helper.getConfig(constants.UserData.FILE_NAME)
    acc: AccountLoginDetails = AccountLoginDetails(
        email=userdata[constants.UserData.SENDER_EMAIL_ADDRESS],
        password=userdata[constants.UserData.SENDER_PASSWORD]
    )

    send_email_address: str = userdata[constants.UserData.RECEIVER_EMAIL]
    good_places: List[str] = userdata[constants.UserData.GOOD_CITIES].split(",")
    good_places = [x.strip().lower() for x in good_places]
    before_date: datetime = datetime.strptime(userdata[constants.UserData.EXAM_BEFORE], "%d.%m.%Y")

    print(f"Email sender account email: {acc.email}")
    print(f"Email sender account password: {acc.password}")
    print(f"Email will be sent to: {send_email_address}")
    print("Looking in: " + ", ".join(good_places))
    print("Looking timeframe: " + datetime.now().strftime("%d.%m.%Y") + " <  X  <= " + before_date.strftime("%d.%m.%Y"))
    print()


    if not use_public_data:
        wait_for_user_to_close_calender()

    old_good_times: List[Reservation] = []
    while True:
        if use_public_data:
            times: str = driver.find_element_by_id("eksami_ajad:kategooriaBEksamiAjad_data").text
            times_regex = re.findall(pattern="(?!\s)(\D+) (\d+.\d+.\d+) (\d+.\d+)", string=times)
            list_times: List[Reservation] = [Reservation(place=x[0], date=x[1], time=x[2]) for x in times_regex]
        else:
            list_times: List[Reservation] = private_data_scraper(driver=driver, main_page=main_page)
        list_times = list(filter(lambda x: x.place.lower() in good_places, list_times))
        list_times.sort(key=lambda x: (x.date, x.time))

        print("Time: " + datetime.now().strftime("%H:%M:%S"))
        print("\n".join([str(x) for x in list_times]))
        print()

        new_good_times = find_good_times(
            good_cities=good_places,
            before_date=before_date,
            times=list_times,
            old_good_times=old_good_times
        )
        for new_good_time in new_good_times:
            old_good_times.append(new_good_time)
            print(f"New good time found: {new_good_time}")
        if len(old_good_times) != 0:
            print("Good times found:")
            print("\n".join([str(x) for x in old_good_times]))
            print()
        if len(new_good_times) != 0:
            Alert.send_email(from_account=acc,
                             to_email=send_email_address,
                             subject="Available Maanteeamet exam time found",
                             msg="Python program detected a driving exam time on: \n" +
                                 "\n".join([str(x) for x in new_good_times]))
            Alert.create_noise()
        sleep(30)
        continue

if __name__ == '__main__':
    time_scanner(use_public_data=True)