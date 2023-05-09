import pickle
from datetime import datetime
from random import randint
from random import uniform
from time import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from source.browsing_util import go_to_link
from source.browsing_util import insta_bar_search
from source.nap_util import all_or_nothing_nap
from source.nap_util import nap
from source.respect_limits_util import respect_hourly_rate_limits
from source.xpaths import get_xpath

non_followers_number = None
non_followers_lst = []
unfollowed_this_run = []


def get_relationships(browser, relation='', username=''):
    profile_link = 'https://www.instagram.com/{}/'.format(username)
    go_to_link(browser, profile_link)
    nap(0.77)

    if relation == 'followers':
        print('Getting followers...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        number_of_relations_xpath = get_xpath(name='number_of_followers_xpath')
        relations_button_xpath = get_xpath(name='followers_button_xpath')
        relations_window_xpath = get_xpath(name='followers_window_xpath')
        relations_xpath_1 = get_xpath(name='followers_xpath_1')
        relations_xpath_2 = get_xpath(name='followers_xpath_2')
        close_relations_xpath = get_xpath(name='close_followers_xpath')
    elif relation == 'following':
        print('Getting following...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        number_of_relations_xpath = get_xpath(name='number_of_following_xpath')
        relations_button_xpath = get_xpath(name='following_button_xpath')
        relations_window_xpath = get_xpath(name='following_window_xpath')
        relations_xpath_1 = get_xpath(name='following_xpath_1')
        relations_xpath_2 = get_xpath(name='following_xpath_2')
        close_relations_xpath = get_xpath(name='close_following_xpath')
    else:
        return

    number_of_relations = int(browser.find_element_by_xpath(number_of_relations_xpath).text)
    relations_button = browser.find_element_by_xpath(relations_button_xpath)
    relations_button.click()
    nap(2.49)

    relations_lst = []
    absolute_scroll = 0
    switch_finding_method = False
    for i in range(0, round(number_of_relations * 0.11)):
        if i < (uniform(0.9, 1.1) * 17):
            base_scroll = 880
        else:
            if 0.25 > uniform(0, 1):
                base_scroll = 1790
            else:
                base_scroll = 1230
        switch_finding_method = not switch_finding_method
        random_scroll_amount = round(base_scroll * uniform(0.95, 1.05))
        absolute_scroll = absolute_scroll + random_scroll_amount
        suggestions_text = browser.find_elements_by_xpath('//*[contains(text(), "sugerencias")]')
        relations_window = browser.find_element_by_xpath(relations_window_xpath)
        if any(suggestions_text):
            avoid_suggestions = randint(0, 533)
            browser.execute_script('arguments[0].scrollTop = {}'.format(avoid_suggestions), relations_window)
            nap(0.33)
            absolute_scroll = round(absolute_scroll * 0.8)
        try:
            # browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', relations_window)
            browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), relations_window)
        except NoSuchElementException:
            relations_window = browser.find_element_by_xpath(relations_window_xpath)
            browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), relations_window)

        if len(relations_lst) <= 12:
            if switch_finding_method:
                relations_elements = browser.find_elements_by_xpath(relations_xpath_1)
            else:
                relations_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
            try:
                for element in relations_elements:
                    href = element.get_attribute('href')
                    account_name = element.get_attribute('title')
                    link_from_account_name = 'https://www.instagram.com/{}/'.format(account_name)
                    if href not in relations_lst and href is not None:
                        relations_lst.append(href)
                    if link_from_account_name not in relations_lst:
                        relations_lst.append(link_from_account_name)
            except StaleElementReferenceException:
                if switch_finding_method:
                    relations_elements = browser.find_elements_by_xpath(relations_xpath_1)
                else:
                    relations_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
                for element in relations_elements:
                    href = element.get_attribute('href')
                    account_name = element.get_attribute('title')
                    link_from_account_name = 'https://www.instagram.com/{}/'.format(account_name)
                    if href not in relations_lst and href is not None:
                        relations_lst.append(href)
                    if link_from_account_name not in relations_lst:
                        relations_lst.append(link_from_account_name)
            except NoSuchElementException:
                pass

        else:
            if switch_finding_method:
                relations_elements = browser.find_elements_by_xpath(relations_xpath_2)
            else:
                relations_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
            try:
                for element in relations_elements:
                    href = element.get_attribute('href')
                    account_name = element.get_attribute('title')
                    link_from_account_name = 'https://www.instagram.com/{}/'.format(account_name)
                    if href not in relations_lst and href is not None:
                        relations_lst.append(href)
                    if link_from_account_name not in relations_lst:
                        relations_lst.append(link_from_account_name)
                    try:
                        text_name = element.text()
                        link_from_text_name = 'https://www.instagram.com/{}/'.format(text_name)
                        if link_from_text_name not in relations_lst:
                            relations_lst.append(link_from_text_name)
                    except TypeError:
                        pass
            except StaleElementReferenceException:
                if switch_finding_method:
                    if switch_finding_method:
                        relations_elements = browser.find_elements_by_xpath(relations_xpath_2)
                    else:
                        relations_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
                for element in relations_elements:
                    href = element.get_attribute('href')
                    account_name = element.get_attribute('title')
                    link_from_account_name = 'https://www.instagram.com/{}/'.format(account_name)
                    if href not in relations_lst and href is not None:
                        relations_lst.append(href)
                    if link_from_account_name not in relations_lst:
                        relations_lst.append(link_from_account_name)
                    try:
                        text_name = element.text()
                        link_from_text_name = 'https://www.instagram.com/{}/'.format(text_name)
                        if link_from_text_name not in relations_lst:
                            relations_lst.append(link_from_text_name)
                    except TypeError:
                        pass
            except NoSuchElementException:
                pass
        nap(1)

    relations_elements_css = browser.find_elements_by_css_selector('.FPmhX.notranslate')
    relations_elements_xpath = browser.find_elements_by_xpath(relations_xpath_2)
    relations_elements_lst = [relations_elements_css, relations_elements_xpath]
    for relations_elements in relations_elements_lst:
        for element in relations_elements:
            href = element.get_attribute('href')
            account_name = element.get_attribute('title')
            link_from_account_name = 'https://www.instagram.com/{}/'.format(account_name)
            if href not in relations_lst and href is not None:
                relations_lst.append(href)
            if link_from_account_name not in relations_lst:
                relations_lst.append(link_from_account_name)
            try:
                text_name = element.text()
                link_from_text_name = 'https://www.instagram.com/{}/'.format(text_name)
                if link_from_text_name not in relations_lst:
                    relations_lst.append(link_from_text_name)
            except TypeError:
                pass
        nap(1)

    for i in range(0, number_of_relations):
        xpath_str = '({})[{}]'.format(relations_xpath_2, i)
        try:
            element = browser.find_element_by_xpath(xpath_str)
            href = element.get_attribute('href')
            if href not in relations_lst and href is not None:
                relations_lst.append(href)
            nap(0.44)
        except StaleElementReferenceException:
            element = browser.find_element_by_xpath(xpath_str)
            href = element.get_attribute('href')
            if href not in relations_lst and href is not None:
                relations_lst.append(href)
            nap(0.44)
        except NoSuchElementException:
            nap(0.44)
            pass

    close_window_button = browser.find_element_by_xpath(close_relations_xpath)
    close_window_button.click()
    nap(1.44)

    return relations_lst
