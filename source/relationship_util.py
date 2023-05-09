import pickle
import re
from datetime import datetime
from insta_bot.source.browsing_util import format_thousands_str_spanish
from insta_bot.source.browsing_util import go_to_link
from insta_bot.source.browsing_util import insta_bar_search
from insta_bot.source.login_util import current_working_directory
from insta_bot.source.nap_util import nap
from insta_bot.source.respect_limits_util import respect_hourly_rate_limits
from insta_bot.source.respect_limits_util import unfollow_blocked
from insta_bot.source.xpaths import get_xpath
from os import chmod as os_chmod
from random import randint
from random import uniform
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from stat import S_IRWXU
from time import time

non_followers_number = 0
non_followers_lst = []
unfollowed_this_run = []
global_followback_rate = None
followers_lst = []


# selenium also fails to get users this way, use regex 'notranslate _whatever" href="/(.*?)/" role="link'
def get_network_activity(browser, get=True):
    if get:
        network_activity = browser.execute_script('return window.performance.getEntriesByType("resource");')
        return network_activity


def get_relationships(browser, relation='', username=''):
    use_full_grabbing_capabilities = True
    profile_link = 'https://www.instagram.com/{}/'.format(username)
    go_to_link(browser, profile_link)

    if relation == 'followers':
        print('Getting followers...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        number_of_relations_xpath = get_xpath(name='number_of_followers_xpath')
        relations_button_xpath = get_xpath(name='followers_button_xpath')
        relations_window_xpath = get_xpath(name='followers_window_xpath')
        relations_xpath_2 = get_xpath(name='followers_xpath_2')
        close_relations_xpath = get_xpath(name='close_followers_xpath')
    elif relation == 'following':
        print('Getting following...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        number_of_relations_xpath = get_xpath(name='number_of_following_xpath')
        relations_button_xpath = get_xpath(name='following_button_xpath')
        relations_window_xpath = get_xpath(name='following_window_xpath')
        relations_xpath_2 = get_xpath(name='following_xpath_2')
        close_relations_xpath = get_xpath(name='close_following_xpath')
    else:
        raise ValueError

    number_of_relations = int(browser.find_element_by_xpath(number_of_relations_xpath).text)
    relations_button = browser.find_element_by_xpath(relations_button_xpath)
    relations_button.click()
    nap(2.49)

    relations_lst = []
    absolute_scroll = 0
    network_resources = []
    for i in range(0, round(number_of_relations * 0.09)):
        network_resources += get_network_activity(browser, get=use_full_grabbing_capabilities)
        if i < (uniform(0.9, 1.1) * 17):
            base_scroll = 880
        else:
            if 0.25 > uniform(0, 1):
                base_scroll = 2123  # 1970
            else:
                base_scroll = 1431  # 1230
        random_scroll_amount = round(base_scroll * uniform(0.94, 1.06))
        absolute_scroll = absolute_scroll + random_scroll_amount
        relations_window = browser.find_element_by_xpath(relations_window_xpath)
        suggestions_text = browser.find_elements_by_xpath('//*[contains(text(), "sugerencias")]')
        if any(suggestions_text):
            avoid_suggestions = randint(0, 533)
            browser.execute_script('arguments[0].scrollTop = {}'.format(avoid_suggestions), relations_window)
            nap(1.33)
            absolute_scroll = round(absolute_scroll * 0.8)
        network_resources += get_network_activity(browser, get=use_full_grabbing_capabilities)
        try:
            browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), relations_window)
            continue
        except NoSuchElementException:
            relations_window = browser.find_element_by_xpath(relations_window_xpath)
            browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), relations_window)
            continue
        finally:
            network_resources += get_network_activity(browser, get=use_full_grabbing_capabilities)
            pass
    # browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', relations_window)
    network_resources += get_network_activity(browser, get=use_full_grabbing_capabilities)

    relations_elements = browser.find_elements_by_xpath(relations_xpath_2.format(''))
    for element in relations_elements:
        href = element.get_attribute('href')
        if href not in relations_lst and href is not None:
            relations_lst.append(href)

    relations_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
    for element in relations_elements:
        href = element.get_attribute('href')
        if href not in relations_lst and href is not None:
            relations_lst.append(href)

    relations_elements = browser.find_elements_by_class_name("FPmhX notranslate  _0imsa ")
    for element in relations_elements:
        href = element.get_attribute('href')
        if href not in relations_lst and href is not None:
            relations_lst.append(href)

    for i in range(1, number_of_relations):
        xpath_str = relations_xpath_2.format('[{}]'.format(i))
        try:
            element = browser.find_element_by_xpath(xpath_str)
            href = element.get_attribute('href')
            if href not in relations_lst and href is not None:
                relations_lst.append(href)
        except (StaleElementReferenceException, NoSuchElementException):
            try:
                element = browser.find_element_by_xpath(xpath_str)
                href = element.get_attribute('href')
                if href not in relations_lst and href is not None:
                    relations_lst.append(href)
            except (StaleElementReferenceException, NoSuchElementException):
                continue

    for i in range(1, number_of_relations):
        xpath_str = relations_xpath_2.format('')
        xpath_str = '({})[{}]'.format(xpath_str, i)
        try:
            element = browser.find_element_by_xpath(xpath_str)
            href = element.get_attribute('href')
            if href not in relations_lst and href is not None:
                relations_lst.append(href)
        except (StaleElementReferenceException, NoSuchElementException):
            try:
                element = browser.find_element_by_xpath(xpath_str)
                href = element.get_attribute('href')
                if href not in relations_lst and href is not None:
                    relations_lst.append(href)
            except (StaleElementReferenceException, NoSuchElementException):
                continue

    close_window_button = browser.find_element_by_xpath(close_relations_xpath)
    close_window_button.click()
    nap(1.44)

    if use_full_grabbing_capabilities:
        selenium_find_by_failed = 0
        selenium_fails = []
        query_list = []
        for dict_ in network_resources:
            query_url = dict_['name']
            if 'https://www.instagram.com/graphql/query/?query_hash=' in query_url:
                query_list.append(query_url)

        for query_url in query_list:
            go_to_link(browser, query_url)
            nap(1)
            query_response = browser.find_element_by_xpath('//pre').text
            account_names = re.findall('"username":"(.+?)"', query_response)
            for account_name in account_names:
                link = 'https://www.instagram.com/{}/'.format(account_name)
                if link not in relations_lst:
                    relations_lst.append(link)
                    selenium_fails.append(link)
                    selenium_find_by_failed += 1
        print('selenium_find_by_failed =', selenium_find_by_failed)
        print('selenium_fails =', selenium_fails)
    return relations_lst


def unfollow_non_followers(browser, ignore_lst, action_delay=180,
                           sets_of_n_actions=5, set_delay=660, max_unfollows=50,
                           days_to_wait_to_unfollow=12, my_username=''):
    global non_followers_number
    global non_followers_lst
    global unfollowed_this_run
    global global_followback_rate
    global followers_lst

    if unfollow_blocked:
        return

    file_1_name = 'black_list_file.pickle'
    file_path = current_working_directory + file_1_name
    try:
        with open(file_path, 'rb') as file_1:
            black_list = pickle.load(file_1)
    except (FileNotFoundError, EOFError):
        black_list = {}
        with open(file_path, 'wb') as file_1:
            pickle.dump(black_list, file_1)
    print('black_list len =', len(black_list))

    file_2_name = 'non_followers_file.pickle'
    if not any(non_followers_lst):
        file_path = current_working_directory + file_2_name
        try:
            with open(file_path, 'rb') as file_2:
                non_followers_lst = pickle.load(file_2)
        except (FileNotFoundError, EOFError):
            with open(file_path, 'wb') as file_2:
                pickle.dump(non_followers_lst, file_2)

    dump_to_black_list = {}
    days_to_wait_to_unfollow = round(days_to_wait_to_unfollow * 60 * 60 * 24)
    sets_of_n_actions_original = sets_of_n_actions
    sets_of_n_actions = round(sets_of_n_actions * uniform(0.75, 1.23))
    max_unfollows = round(max_unfollows * uniform(0.87, 1))

    my_profile_link = 'https://www.instagram.com/{}/'.format(my_username)
    go_to_link(browser, my_profile_link)

    counter = 0
    max_unfollows_count = 0
    if not any(non_followers_lst):
        followers_lst = get_relationships(browser, relation='followers', username=my_username)
        print('retrieved number of followers =', len(followers_lst))
        following_lst = get_relationships(browser, relation='following', username=my_username)
        print('retrieved number of following =', len(following_lst))

        print('Unfollowing...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        ignore_lst_2 = []
        for account_name in ignore_lst:
            ignore_lst_2.append('https://www.instagram.com/{}/'.format(account_name))
        for user_link in following_lst:
            if user_link not in ignore_lst_2:
                if user_link not in followers_lst:
                    non_followers_lst.append(user_link)
        print('non_followers_lst =', non_followers_lst)
        print('following_lst =', following_lst)
        non_followers_number = len(non_followers_lst)
        print('non_followers_number =', non_followers_number)

        followed_back = []
        for follower in followers_lst:
            if follower in black_list:
                followed_back.append(follower)
        global_followback_rate = len(followed_back) / len(black_list)
    else:
        print('Unfollowing until non_followers_lst is empty...', datetime.now().strftime('%Y-%m-%d %H:%M'))
        non_followers_number = len(non_followers_lst)
        print('non_followers_number =', non_followers_number)

    try:
        for user_link in non_followers_lst:
            scrolled_amount = 0
            base_scroll = 217
            try:
                followed_timestamp = black_list[user_link]
                if round(time() * uniform(1, 1.033)) - followed_timestamp > days_to_wait_to_unfollow:
                    insta_bar_search(browser, user_link, finally_go_to_link=False)
                    nap(6.73)

                    post_count_xpath = get_xpath(name='post_count_xpath')
                    post_count = browser.find_element_by_xpath(post_count_xpath).text
                    post_count = format_thousands_str_spanish(post_count)

                    if 0.58 > uniform(0, 1):
                        for i in range(0, round(post_count / 2)):
                            if 0.16 > uniform(0, 1):
                                random_scroll_amount = round(1.36 * base_scroll * uniform(0.9, 1.1))
                            else:
                                random_scroll_amount = round(base_scroll * uniform(0.8, 1.2))
                            browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
                            scrolled_amount += random_scroll_amount
                            nap(0.52)
                            if i > 10:
                                break
                        while scrolled_amount > 0:
                            if 0.76 > uniform(0, 1):
                                random_scroll_amount = round(1.36 * base_scroll * uniform(0.9, 1.1))
                            else:
                                random_scroll_amount = round(base_scroll * uniform(0.8, 1.2))
                            random_scroll_amount = -1 * random_scroll_amount
                            browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
                            scrolled_amount += random_scroll_amount
                        nap(1.38)

                    unfollow_button_xpath = '//*[@id="react-root"]//*[text()="Siguiendo"]'
                    unfollow_button = browser.find_element_by_xpath(unfollow_button_xpath)
                    unfollow_button.click()
                    'bot_click(browser, xpath=unfollow_button_xpath)'
                    nap(1.98)
                    confirm_unfollow_xpath = '//*[text()="Dejar de seguir"]'
                    confirm_unfollow_button = browser.find_element_by_xpath(confirm_unfollow_xpath)
                    confirm_unfollow_button.click()
                    'bot_click(browser, xpath=confirm_unfollow_xpath)'

                    if 0.08 > uniform(0, 1):
                        for i in range(0, round(post_count / 2)):
                            if 0.46 > uniform(0, 1):
                                random_scroll_amount = round(1.36 * base_scroll * uniform(0.9, 1.1))
                            else:
                                random_scroll_amount = round(base_scroll * uniform(0.8, 1.2))
                            browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
                            scrolled_amount += random_scroll_amount
                            nap(0.52)
                            if i > 10:
                                break
                        while scrolled_amount > 0:
                            if 0.84 > uniform(0, 1):
                                random_scroll_amount = round(1.36 * base_scroll * uniform(0.9, 1.1))
                            else:
                                random_scroll_amount = round(base_scroll * uniform(0.8, 1.2))
                            random_scroll_amount = -1 * random_scroll_amount
                            browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
                            scrolled_amount += random_scroll_amount

                    respect_hourly_rate_limits(browser, action='unfollow')
                    unfollowed_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
                    if unfollow_blocked:
                        return
                    print('Unfollowed = ', user_link, unfollowed_datetime)
                    unfollowed_this_run.append(user_link)
                    counter += 1
                    max_unfollows_count += 1
                    nap(action_delay)

                    if counter >= sets_of_n_actions:
                        counter = 0
                        sets_of_n_actions = round(sets_of_n_actions_original * uniform(0.75, 1.23))
                        print('>---Sleeping after a few unfollows---<')
                        nap(set_delay)
                    if max_unfollows_count >= max_unfollows:
                        print('max_unfollows limit hit', datetime.now().strftime('%Y-%m-%d %H:%M'))
                        nap(action_delay)
                        return
            except KeyError:
                dump_to_black_list.update({user_link: int(time())})
            except NoSuchElementException:
                unfollowed_this_run.append(user_link)
                print('Could not unfollow =', user_link, datetime.now().strftime('%Y-%m-%d %H:%M'))
                pass
        print('Unfollow completed =', datetime.now().strftime('%Y-%m-%d %H:%M'))

    finally:
        black_list.update(dump_to_black_list)
        file_path = current_working_directory + file_1_name
        if any(dump_to_black_list):
            try:
                with open(file_path, 'wb') as file_1:
                    pickle.dump(black_list, file_1)
            except IOError:
                os_chmod(file_path, S_IRWXU)
                with open(file_path, 'wb') as file_1:
                    pickle.dump(black_list, file_1)
        file_1.close()

        local_non_followers_lst = []
        for user in non_followers_lst:
            if user not in unfollowed_this_run:
                local_non_followers_lst.append(user)
        non_followers_lst = local_non_followers_lst
        non_followers_number = len(non_followers_lst)
        file_path = current_working_directory + file_2_name
        try:
            with open(file_path, 'wb') as file_2:
                pickle.dump(non_followers_lst, file_2)
        except IOError:
            os_chmod(file_path, S_IRWXU)
            with open(file_path, 'wb') as file_2:
                pickle.dump(non_followers_lst, file_2)
        file_2.close()
        print('Unfollowed =', max_unfollows_count)
        if max_unfollows_count == 0:
            print('No non-followers available, wait more days')
