#!/bin/env python3
"""
RMB's Selenium Module
"""

# import atexit
# import inspect
# import os
# import re
# import sys
# import time
# from enum import Enum, IntEnum, auto
# from functools import partial

import argparse
import random

from datetime import datetime
from time import sleep

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import rmblogging
from rmblogging import Rmblogging, LogLevels, debug, info, warning, error


class Sites:
    sites = {
        'nosite': {
            'url': r'https://www.saucedemo.com',
            'user': 'standard_user',
            'password': 'secret_sauce',
            'email': 'robertbyers1111@gmail.com',
        },
    }


class Xpaths:
    username_input = r'//input[@id = "user-name"]'
    password_input = r'//input[@id = "password"]'
    login_button = r'//input[@id = "login-button" and @type="submit"]'
    logout_button = r'//a[@id = "logout_sidebar_link"]'
    menu_button = r'//button[@id = "react-burger-menu-btn"]'
    inventory_container = r'//*[@class = "inventory_container"]'
    inventory_list = r'//*[@class = "inventory_list"]'
    inventory_item = r'//*[@class = "inventory_item"]'
    inventory_item_name = r'//*[@class = "inventory_item_name"]'
    inventory_anchor = r'//a[starts-with(@id, "item_") and contains(@id, "_img_link")]'
    add_to_cart_button = r'//button[starts-with(@id, "add-to-cart") and contains(text(), "Add to cart")]'
    back_to_products = r'//button[@id = "back-to-products" and @name = "back-to-products"]'


class RmbSelenium:

    def __init__(self, **kwargs):

        parser = argparse.ArgumentParser()
        parser.add_argument("--loglevel", default=None, type=str.upper, choices=['EMERGENCY', 'CRITICAL', 'ALERT', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG'])
        parser.add_argument("--download_dir", default='downloads')
        parser.add_argument("--headless", default=False, action="store_true")
        parser.add_argument("--session_ID", default=datetime.now().strftime('%Y-%m%d-%H%M%S'))

        cmdline_args, unknown_args = parser.parse_known_args(sys.argv[1:])

        self.download_dir = cmdline_args.download_dir
        self.headless = cmdline_args.headless
        self.session_ID = cmdline_args.session_ID

        # If setting loglevel from command line..
        if cmdline_args.loglevel is not None:
            Rmblogging.loglevel = LogLevels[cmdline_args.loglevel]

        # Or, to manually override loglevel from code (i.e., not from command line) only need this..
        # Rmblogging.loglevel = LogLevels.DEBUG

        # Retrieve the site attributes..
        sites = Sites.sites
        site = self.site
        if site in sites.keys():
            self.url = sites[site]['url']
            self.user = sites[site]['user']
            self.email = sites[site]['email']
            self.password = sites[site]['password']
        else:
            error(f"'{site}' is not a supported site key")

        # Class attributes used for Selenium and the apps..
        self.driver = None
        self.very_long_wait = None
        self.long_wait = None
        self.medium_wait = None
        self.quick_wait = None
        self.mini_wait = None
        self.tab_handles = None
        self.random_seed = datetime.now().strftime('%f%S%M%H')
        random.seed(self.random_seed)

        # Selenium options..
        self.options = Options()
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-extensions")
        if self.headless:
            self.options.add_argument("--headless")
        else:
            self.options.add_argument("start-maximized")
            self.options.add_argument("--window-position=-1920,0")

        self.options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        })

    def sleep(self, seconds, msg=None):

        if seconds <= 4:
            sleepval = random.randint(1, seconds)
        elif seconds <= 8:
            sleepval = random.randint(2, seconds)
        elif seconds <= 16:
            sleepval = random.randint(4, seconds)
        elif seconds <= 32:
            sleepval = random.randint(8, seconds)
        else:
            sleepval = random.randint(int(seconds/4), seconds)

        if msg is None:
            debug(f"Sleep {sleepval}")
        else:
            debug(f"Sleep {sleepval} {msg}")

        sleep(sleepval)

    def start_browser(self):
        debug("Opening browser..")
        self.driver = driver = webdriver.Chrome(options=self.options)
        self.very_long_wait = WebDriverWait(driver, 60)
        self.long_wait = WebDriverWait(driver, 20)
        self.medium_wait = WebDriverWait(driver, 5)
        self.quick_wait = WebDriverWait(driver, 1.33)
        self.mini_wait = WebDriverWait(driver, 0.5)
        self.driver.maximize_window()
        self.driver.get(self.url)

    def open_new_tab(self):
        debug(f"Opening new browser tab..")
        self.driver.execute_script("window.open('');")  # open a new tab.
        self.tab_handles = self.driver.window_handles
        self.driver.switch_to.window(self.tab_handles[1])
        self.sleep(4, "after switching to new tab")
        return

    def close_current_tab(self):
        debug("Closing current browser tab..")
        self.driver.close()
        tab_handles = self.driver.window_handles
        new_last_tab = tab_handles[-1]
        self.driver.switch_to.window(new_last_tab)
        self.sleep(4, "after closing current tab and switching to previous tab")

    def login(self):
        info(f"Logging in as {self.user}")
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, Xpaths.username_input)))
        element.send_keys(self.user)
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, Xpaths.password_input)))
        element.send_keys(self.password)
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, Xpaths.login_button)))
        element.click()

    def logout(self):
        info("Logging out..")
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, Xpaths.menu_button)))
        element.click()
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, Xpaths.logout_button)))
        element.click()

    def wait_for_element_helper(self, ec_method, xpath_expression):
        """
        - OPTIONAL -
        Perform a Selenium ec wait-for method for a particular xpath, with retries.
        Throws an error after no retries remain.

        :param   ec_method: (func ref) A Selenium ec wait-for method (e.g., ec.presence_of_element_located)
        :param   xpath_expression: (str) The XPath expression to be waited for

        :return: Returns whatever is returned by ec_method. Raises an exception upon failure - only returns upon success.
        """
        attempts_remaining = 2
        while attempts_remaining >= 0:
            try:
                return_val = self.long_wait.until(ec_method((By.XPATH, xpath_expression)))
            except (selenium.common.exceptions.TimeoutException, TimeoutError):
                attempts_remaining -= 1
                if attempts_remaining >= 1:
                    warning(f"Timeout waiting for {xpath_expression=}, {attempts_remaining=}")
                else:
                    error(f"Timeout waiting for {xpath_expression=}, {attempts_remaining=}")
            else:
                return return_val


if __name__ == '__main__':
    ...
