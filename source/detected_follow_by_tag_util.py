# -*- coding: UTF-8 -*-

import pickle
from datetime import datetime
from os import chmod as os_chmod
from random import randint
from random import sample
from random import uniform
from stat import S_IRWXU
from time import time

from insta_bot.source.browsing_util import format_thousands_str_spanish
from insta_bot.source.browsing_util import go_to_link
from insta_bot.source.browsing_util import insta_bar_search
from insta_bot.source.login_util import current_working_directory
from insta_bot.source.nap_util import nap
from insta_bot.source.respect_limits_util import follow_blocked
from insta_bot.source.respect_limits_util import respect_hourly_rate_limits
from insta_bot.source.stories_util import watch_stories_in_page
from insta_bot.source.xpaths import get_xpath
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

followed_this_run = []


def follow_by_tag(browser, tag_lst, follows_per_tag=5, max_follows=30,
                  max_likes_to_follow=100, action_delay=180, set_delay=660,
                  watch_stories=False):
    global followed_this_run

    if follow_blocked:
        return

    skip_first_9 = 3
    after_scrolling_first_9_skip_first = 7
    reset_after_scrolling_first_9_skip_first = after_scrolling_first_9_skip_first
    prb_click_post = 0.57
    prb_follow_poster = 0.59
    counter = 0
    max_follows_count = 0
    dump_to_black_list = {}

    file_1_name = 'black_list_file.pickle'
    file_path = current_working_directory + file_1_name
    try:
        with open(file_path, 'rb') as file_1:
            black_list = pickle.load(file_1)
    except FileNotFoundError:
        black_list = {}
        with open(file_path, 'wb') as file_1:
            pickle.dump(black_list, file_1)

    file_2_name = 'tag_analysis.pickle'
    file_path = current_working_directory + file_2_name
    try:
        with open(file_path, 'rb') as file_2:
            tag_analysis = pickle.load(file_2)
    except (FileNotFoundError, EOFError):
        tag_analysis = {}
        with open(file_path, 'wb') as file_2:
            pickle.dump(tag_analysis, file_2)
    dump_to_tag_analysis = {}

    max_follows = round(max_follows * uniform(0.87, 1))
    max_likes_to_follow = round(max_likes_to_follow * uniform(0.9, 1.1))
    sets_of_n_actions = round(follows_per_tag * uniform(0.71, 1.23))
    random_len = round(len(tag_lst) * uniform(0.25, 0.75))
    tag_lst = sample(tag_lst, random_len)
    prb_click_post = prb_click_post * uniform(0.97, 1.03)
    prb_follow_poster = prb_follow_poster * uniform(0.97, 1.03)

    print('black_list len =', len(black_list))
    black_list_keys = [list(black_list.keys())]

    try:
        for tag in tag_lst:
            insta_bar_search(browser, search='#{}'.format(tag))
            go_to_link(browser, 'https://www.instagram.com/explore/tags/{}/'.format(tag))
            nap(1.47)

            number_of_posts = browser.find_element_by_css_selector('.g47SY').text
            number_of_posts = format_thousands_str_spanish(number_of_posts)
            if number_of_posts < 10_000:
                after_scrolling_first_9_skip_first += 25
            elif number_of_posts < 50_000:
                after_scrolling_first_9_skip_first += 20
            elif number_of_posts < 100_000:
                after_scrolling_first_9_skip_first += 17
            else:
                after_scrolling_first_9_skip_first = reset_after_scrolling_first_9_skip_first

            if watch_stories:
                watch_stories_in_page(browser)

            post_links_lst = []
            range_end = round(follows_per_tag * (1 / prb_click_post) * (1 / prb_follow_poster))
            for i in range(0, round(range_end / 3) + 1 + skip_first_9 + after_scrolling_first_9_skip_first):
                random_scroll_amount = str(round(277 * uniform(0.9, 1.14)))
                browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
                post_hrefs = browser.find_elements_by_xpath('//*[@id="react-root"]//a[starts-with(@href, "/p/")]')
                try:
                    for href in post_hrefs:
                        href = href.get_attribute('href')
                        if href not in post_links_lst:
                            post_links_lst.append(href)
                except StaleElementReferenceException:
                    post_hrefs = browser.find_elements_by_xpath('//*[@id="react-root"]//a[starts-with(@href, "/p/")]')
                    for href in post_hrefs:
                        href = href.get_attribute('href')
                        if href not in post_links_lst:
                            post_links_lst.append(href)
                nap(0.67)
            nap(0.79)

            post_links_lst = post_links_lst[(skip_first_9 + after_scrolling_first_9_skip_first) * 3:]
            maybe_break_next = False
            for post_link in post_links_lst:
                if prb_click_post > uniform(0, 1):
                    go_to_link(browser, post_link)
                    nap(5.53)
                    number_of_likes_xpath = get_xpath(name='number_of_likes_xpath')
                    try:
                        number_of_likes = browser.find_element_by_xpath(number_of_likes_xpath).text
                        number_of_likes = format_thousands_str_spanish(number_of_likes)
                    except NoSuchElementException:
                        number_of_likes = randint(0, 1)
                    try:
                        user_href_xpath = '//*[@id="react-root"]//article/header/div[2]/div[1]/div[1]/h2/a'
                        user_href = browser.find_element_by_xpath(user_href_xpath)
                        user_href = user_href.get_attribute('href')
                    except NoSuchElementException:
                        continue

                    if user_href not in black_list_keys:
                        if prb_follow_poster > uniform(0, 1) and number_of_likes <= max_likes_to_follow:
                            try:
                                follow_button_xpath = '//button[text()="Seguir"]'
                                follow_button = browser.find_element_by_xpath(follow_button_xpath)
                                'browser.execute_script("arguments[0].click();", follow_button)'
                                follow_button.click()
                                respect_hourly_rate_limits(browser, action='follow')
                                if follow_blocked:
                                    return
                                print('Followed = ', user_href, datetime.now().strftime('%Y-%m-%d %H:%M'))
                                followed_this_run.append(user_href)
                                counter += 1
                                max_follows_count += 1
                                dump_to_black_list.update({user_href: round(time())})
                                dump_to_tag_analysis.update({user_href: tag})
                                nap(action_delay)

                                if maybe_break_next:
                                    if 0.89 > uniform(0, 1):
                                        break
                                if counter >= sets_of_n_actions:
                                    counter = 0
                                    sets_of_n_actions = round(follows_per_tag * uniform(0.75, 1.19))
                                    print('>---Sleeping after a few follows---<')
                                    nap(set_delay)
                                    if 0.31 > uniform(0, 1):
                                        break
                                    else:
                                        maybe_break_next = True
                                if max_follows_count >= max_follows:
                                    print('max_follows limit hit', datetime.now().strftime('%Y-%m-%d %H:%M'))
                                    nap(action_delay)
                                    return
                            except NoSuchElementException:
                                pass
        print('follow_by_tag completed =', datetime.now().strftime('%Y-%m-%d %H:%M'))

    finally:
        print('Followed =', max_follows_count)
        black_list.update(dump_to_black_list)
        file_path = current_working_directory + file_1_name
        if any(dump_to_black_list):
            try:
                with open(file_path, 'wb') as file_1:
                    pickle.dump(black_list, file_1)
            except IOError:
                os_chmod(file_path, S_IRWXU)
                with open(file_path, 'wb') as file_2:
                    tag_analysis.dump(tag_analysis, file_2)
        file_1.close()

        if any(dump_to_tag_analysis):
            tag_analysis.update(dump_to_tag_analysis)
            file_path = current_working_directory + file_2_name
            try:
                with open(file_path, 'wb') as file_2:
                    tag_analysis.dump(dump_to_tag_analysis, file_2)
            except IOError:
                os_chmod(file_path, S_IRWXU)
                with open(file_path, 'wb') as file_2:
                    tag_analysis.dump(dump_to_tag_analysis, file_2)
        file_2.close()
