#!/bin/env python3
"""
RMB's Selenium Module
"""

import argparse
import base64
import random
import re
import sys

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


class RmbSelenium:

    Required_constructor_args = ['site', 'xpaths']
    Optional_constructor_args = ['browser']
    Required_site_keys = ['url', 'user', 'password']

    def __init__(self, **kwargs):

        self.depth = 0
        self.totalcalls = 0
        self.browser = 'chrome'  # < default, can be overriden by 'browser' in kwargs

        parser = argparse.ArgumentParser()
        parser.add_argument("--loglevel", default=None, type=str.upper, choices=['EMERGENCY', 'CRITICAL', 'ALERT', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG'])
        parser.add_argument("--download_dir", default='downloads')
        parser.add_argument("--headless", default=False, action="store_true")
        parser.add_argument("--session_ID", default=datetime.now().strftime('%Y-%m%d-%H%M%S'))

        cmdline_args, unknown_args = parser.parse_known_args(sys.argv[1:])

        self.download_dir = cmdline_args.download_dir
        self.headless = cmdline_args.headless
        self.session_ID = cmdline_args.session_ID

        if cmdline_args.loglevel is not None:
            Rmblogging.loglevel = LogLevels[cmdline_args.loglevel]

        # Grab the required constructor arguments from kwargs..
        for arg_name in RmbSelenium.Required_constructor_args:
            if arg_name in kwargs.keys():
                setattr(self, arg_name, kwargs[arg_name])
            else:
                error(f'Required argument "{arg_name}" not passed to RmbSelenium constructor')

        # Check the optional contructor arguments from kwargs..
        for arg_name in RmbSelenium.Optional_constructor_args:
            if arg_name in kwargs.keys():
                setattr(self, arg_name, kwargs[arg_name])
                debug(f'Optional constructor arg detected in kwargs: {arg_name=}, setting to {kwargs[arg_name]}')

        # Validate the site data..
        for key in RmbSelenium.Required_site_keys:
            if key in self.site.keys():
                if key == 'password':
                    debug(f'{key}: {len(self.site[key])*"*"}')
                else:
                    debug(f'{key}: {self.site[key]}')
            else:
                error(f'Required site dictionary key "{key}" not found during constructor for RmbSelenium class')

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
        if 'alias' in self.site.keys():
            alias = self.site['alias']
        else:
            alias = self.site['url']

        debug(f"==> COMMENCE {alias}")
        debug("Opening browser..")

        if self.browser == 'chrome':
            self.driver = driver = webdriver.Chrome(options=self.options)
        elif self.browser == 'gecko':
            self.driver = driver = webdriver.Firefox()
        elif self.browser == '1111':
            self.options = Options()
            self.options.add_experimental_option("debuggerAddress", "127.0.0.1:1111")
            # lf.options.add_experimental_option("detach", True)  # <== invalid option (for non-chromedriver?)
            self.driver = driver = webdriver.Chrome(options=self.options)
        else:
            raise RuntimeError(f'Unsupported browser: {self.browser = }')

        self.very_long_wait = WebDriverWait(driver, 60)
        self.long_wait = WebDriverWait(driver, 20)
        self.medium_wait = WebDriverWait(driver, 5)
        self.quick_wait = WebDriverWait(driver, 1.33)
        self.mini_wait = WebDriverWait(driver, 0.5)
        self.driver.maximize_window()
        self.driver.get(self.site['url'])

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

    def examine_element(self, web_element, xpath):

        print()
        print(f'~'*88)
        print(f'WEB ELEMENT..')
        print(f'{type(web_element)      = }')
        print(f'{xpath                  = }')

        if type(web_element) is selenium.webdriver.remote.webelement.WebElement:
            print(f'{web_element.id         = }')
            print(f'{web_element.tag_name   = }')
            print(f'{web_element.text[:144] = }')
        else:
            print(f'Whoa! Found an alien in examine_element!')

        self.dig_into_the_tag(web_element, xpath)
        # lf.save_web_element_screenshot_from_base64(web_element)
        ...

    def examine_driver(self, parent_element, xpath):

        print()
        print(f'~'*88)
        print(f'DRIVER..')
        print(f'{type(parent_element)             = }')

        if type(parent_element) is selenium.webdriver.chrome.webdriver.WebDriver:

            print(f'{parent_element.current_url       = }')
            print(f'{parent_element.title             = }')
            print(f'{parent_element.window_handles    = }')
            print(f'{parent_element.page_source[:144] = }')

            web_elements = parent_element.find_elements(By.XPATH, xpath)

            print(f'{len(web_elements) = }')
            for web_element in web_elements:
                print(f'{web_element.id = } {web_element.tag_name = } {web_element.text[:66] = }')

            for web_element in web_elements:
                xpath_ = xpath + f'/{web_element.tag_name}'
                self.examine_element(web_element, xpath_)

        else:
            print(f'Whoa! Found an alien in examine_driver!')

    def login(self):
        """
        Attempts to log in to the intended site whoose URL is in self.url.

        The following values are assumed to exist in the self.site dictionary..
            'url'
            'username'
            'password'

        The following xpaths are assumed to exist in the self.xpaths dictionary..
            'agreement_popup' [optional]
            'login_button1' [optional]
            'username'
            'continue_to_password' [optional]
            'password'
            'login_button2'
            'continue_to_email' [optional]

        NOTES:

        The following keys are optional. If they do not exist, the corresponding action will not be taken.

            'agreement_popup' Required if user must click on a consent-to-user popup before getting to the (possibly preliminary) login page.

            'login_button1' Required if a user must click a button to bring up the login page.

            'continue_to_password' Required if a button must be clicked after entering a username before a password can be typed.

            'continue_to_email' Required if an email service has a separate page for email that must be clicked after a successful login.

        An exception is raised if any error is encountered.

        :return: Nothing
        """

        info(f"Logging in as {self.site['user']}")
        sleep(4)

        self.examine_driver(self.driver, r'/*')

        if 'agreement_popup' in self.xpaths.keys():
            self.sleep(10, 'Waiting for user to click on Agree in the consent popup')
            # None of this worked..
            # popup = self.driver.find_element(By.XPATH, '//body//iframe[contains(@name, "tcfapiLocator")]')
            # popupup = self.driver.switch_to.frame(popup)
            # popupup.find_element(By.XPATH, '//button')
            # popupwait = WebDriverWait(popupup, 8)
            # button = popupwait.until(ec.element_to_be_clickable((By.XPATH, '//button[contains(@id, "onetrust-accept")]')))
            # button.click()
        if 'login_button1' in self.xpaths.keys():
            element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['login_button1'])))
            element.click()
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, self.xpaths['username'])))
        element.send_keys(self.site['user'])
        if 'continue_to_password' in self.xpaths.keys():
            element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['continue_to_password'])))
            element.click()
        element = self.long_wait.until(ec.presence_of_element_located((By.XPATH, self.xpaths['password'])))
        element.send_keys(self.site['password'])
        element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['login_button2'])))
        element.click()
        if 'continue_to_email' in self.xpaths.keys():
            element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['continue_to_email'])))
            element.click()

    def logout(self):
        """
        Attempts to log out of the currently active site

        The following xpaths are assumed to exist in the self.xpaths dictionary..
            'logout_menu' (optional - click brings user to logout page)
            'logout_button' (click logs out from the site)

        NOTE: If the current page already has a visible logout button (i.e., there is no need to click on a
        menu to go to a logout page), leave login_menu undefined.

        An exception is raised if any error is encountered.

        :return: Nothing
        """

        info("Logging out..")
        if 'logout_menu' in self.xpaths.keys():
            element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['logout_menu'])))
            element.click()
        element = self.long_wait.until(ec.element_to_be_clickable((By.XPATH, self.xpaths['logout_button'])))
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

    def save_web_element_screenshot_from_base64(self, web_element):

        image_filename = f"/tmp/rmbselenium_{datetime.now().strftime('%Y-%m%d-%H%M%S-%f')}.png"
        print()
        print('==> IN: save_web_element_screenshot_from_base64')
        print(f'{               image_filename = }')
        print(f'   location scrolled into view = {web_element.location_once_scrolled_into_view}')
        print(f'{         web_element.location = }')
        print(f'{             web_element.rect = }')
        print(f'{             web_element.size = }')
        print(f'{         web_element.tag_name = }')

        with open(image_filename, 'bx') as image_fh:
            try:
                decoded_data = base64.b64decode((web_element.screenshot_as_base64))
                image_fh.write(decoded_data)
            except Exception as e:
                print(f'Could not write to {image_filename}: {repr(e)}')
            else:
                print(f'Yay! Could write to {image_filename}')

    def dig_into_the_tag(self, web_element, curr_xpath):

        self.depth += 1
        self.totalcalls += 1

        indent = self.depth*2*' '

        print()
        print(f'{indent}==> IN: dig_into_the_tag() {self.depth = } {self.totalcalls = }')

        if self.depth > 2000 or self.totalcalls > 20000:
            raise RuntimeError('Whoa! Time to quit!!!')

        try:
            print(f'{indent}{curr_xpath = }')
            print(f'{indent}{web_element.tag_name = }')
            print(f'{indent}{web_element.text[:144] = }')
            print(f'{indent}{web_element.location = }')
            print(f'{indent}{web_element.rect = }')
            print(f'{indent}{web_element.size = }')
            print(f'{indent}location scrolled into view = {web_element.location_once_scrolled_into_view}')
            print(f'{indent}{web_element.id = }')
        except exception as e:
            print(f'{indent}{e}')

        if not web_element.tag_name in ['head', 'script', 'img', 'zhtmlz', 'zbodyz', 'zdivz', 'zspanz']:

            elements = web_element.find_elements(By.XPATH, curr_xpath)

            print()
            print(f'{indent}Found the following subelements for {curr_xpath}..')

            for element in elements:
                print(f'{indent}{element.tag_name = }')
                ...
            ...

            if self.depth < 200:
                for element in elements:
                    new_xpath = curr_xpath + '/' + element.tag_name
                    print(48*'~')
                    print(f'{indent}==> {element.text[:144] = }')
                    print(f'{indent}==> {element.tag_name = }')
                    print(f'{indent}==> {new_xpath = }')
                    self.dig_into_the_tag(element, new_xpath)
                    ...
                ...
            else:
                print(f'{indent}Whoa! Backing out due to {self.depth = }')

        self.depth -= 1
        print(f'{indent}(leaving recursion, new depth is {self.depth}')

if __name__ == '__main__':
    ...

