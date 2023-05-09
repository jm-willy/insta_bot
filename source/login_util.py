from datetime import datetime
from os import getcwd
from random import uniform
from time import sleep

from insta_bot.source.browsing_util import full_human_emulation
from insta_bot.source.browsing_util import go_to_link
from insta_bot.source.browsing_util import open_link_in_new_tab
from insta_bot.source.nap_util import nap
from selenium.common.exceptions import NoSuchElementException

current_working_directory = getcwd() + '/'
logged = False


def log_in(browser, my_username=None, my_password=None, open_more_tabs=False, start_timer_hours=0):
    if start_timer_hours > 0:
        print(' ')
        print('Sleeping', start_timer_hours, 'hours before starting')
        sleep(start_timer_hours * 60 * 60)

    print('*' * 41)
    print('current_working_directory =', current_working_directory)
    print('Started', datetime.now().strftime('%Y-%m-%d %H:%M'))
    print('_' * 41)

    global logged
    login_button_xpath = '//button[text()="Entrar"]'

    my_profile_link = 'https://www.instagram.com/{}/'.format(my_username)
    browser.get(my_profile_link)
    go_to_link(browser, my_profile_link)
    nap(3)

    try:
        login_button = browser.find_element_by_xpath(login_button_xpath)
        login_button.click()
        nap(3)
    except NoSuchElementException:
        logged = True

    if not logged:
        my_username_input_xpath = '//input[@name="username"]'
        my_username_input = browser.find_element_by_xpath(my_username_input_xpath)
        my_username_input.send_keys(my_username)
        nap(4)
        my_password_input_xpath = '//input[@name="password"]'
        my_password_input = browser.find_element_by_xpath(my_password_input_xpath)
        my_password_input.send_keys(my_password)
        nap(6)
        final_login_button_xpath = '//button[@type="submit"]'
        final_login_button = browser.find_element_by_xpath(final_login_button_xpath)
        final_login_button.click()
        nap(3)
        try:
            login_button = browser.find_element_by_xpath(login_button_xpath)
            login_button.click()
        except NoSuchElementException:
            logged = True
    if open_more_tabs or full_human_emulation:
        if 0.73 > uniform(0, 1) or full_human_emulation:
            open_link_in_new_tab(browser, link='https://www.instagram.com/', switch=False)
        else:
            if 0.48 > uniform(0, 1):
                explore_xpath = '//*[@id="react-root"]//*[@aria-label="Buscar personas"]'
                # makes a left click doesn't work
                'open_link_new_tab_right_click(browser, xpath=explore_xpath, switch=False)'
                explore = browser.find_element_by_xpath(explore_xpath)
                open_link_in_new_tab(browser, link='https://www.instagram.com/explore/', switch=False)
            else:
                activity_xpath = '//*[@id="react-root"]//*[@aria-label="Sección de actividades"]'
                activity_button = browser.find_element_by_xpath(activity_xpath)
                # makes a left click doesn't work
                'open_link_new_tab_right_click(browser, xpath=activity_xpath, switch=False)'
                activity_button.click()
                nap(1.7)
                open_link_in_new_tab(browser, link='https://www.instagram.com/accounts/activity/', switch=False)
    return logged
