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
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

followed_this_run = []


def follow_by_tag(browser, tag_lst, follows_per_tag=5, max_follows=30,
                  max_likes_to_follow=100, action_delay=180, set_delay=660,
                  watch_stories=False):
    global followed_this_run

    if follow_blocked:
        return

    scroll_down_n_posts = 22
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
    sets_of_n_actions = round(follows_per_tag * uniform(0.75, 1.23))
    random_len = round(len(tag_lst) * uniform(0.25, 0.75))
    tag_lst = sample(tag_lst, random_len)
    prb_click_post = prb_click_post * uniform(0.97, 1.03)
    prb_follow_poster = prb_follow_poster * uniform(0.97, 1.03)

    print('black_list len =', len(black_list))
    black_list_keys = [list(black_list.keys())]

    try:
        for tag in tag_lst:
            reset_scroll_down_n_posts = scroll_down_n_posts

            insta_bar_search(browser, search='#{}'.format(tag))
            go_to_link(browser, 'https://www.instagram.com/explore/tags/{}/'.format(tag))
            nap(1.47)

            number_of_posts = browser.find_element_by_css_selector('.g47SY').text
            number_of_posts = format_thousands_str_spanish(number_of_posts)
            if number_of_posts < 10_000:
                scroll_down_n_posts += 25
            elif number_of_posts < 50_000:
                scroll_down_n_posts += 20
            elif number_of_posts < 100_000:
                scroll_down_n_posts += 17
            else:
                scroll_down_n_posts = reset_scroll_down_n_posts

            if watch_stories:
                watch_stories_in_page(browser)

            already_viewed_xpaths = []
            range_end = round(follows_per_tag * (1 / prb_click_post) * (1 / prb_follow_poster) * uniform(0.9, 1.1))
            range_end = round(range_end / 3) + 1 + round(scroll_down_n_posts / 3) + 1
            base_scroll = 210
            posts_xpath = '//*[@id="react-root"]//a[starts-with(@href, "/p/")]'
            maybe_break_next = False
            loop_counter_lock_view = 0
            scrolled_amount = 0
            for post_number in range(1, range_end):
                if loop_counter_lock_view == 0:
                    if 0.34 > uniform(0, 1):
                        random_scroll_amount = round(1.4 * base_scroll * uniform(0.95, 1.08))
                    else:
                        random_scroll_amount = round(base_scroll * uniform(0.9, 1.14))
                    browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount + scrolled_amount))
                    scrolled_amount += random_scroll_amount
                    nap(0.33)

                post_xpath = '({})[{}]'.format(posts_xpath, post_number)
                post = browser.find_element_by_xpath(post_xpath)
                loop_counter_lock_view += 1
                if loop_counter_lock_view >= 3:
                    loop_counter_lock_view = 0
                if post_number <= 9:
                    continue
                if prb_click_post > uniform(0, 1) and post_xpath not in already_viewed_xpaths:
                    nap(2.73)
                    post.click()
                    nap(4.53)
                    number_of_likes_xpath = get_xpath(name='number_of_likes_xpath_2')
                    try:
                        number_of_likes = browser.find_element_by_xpath(number_of_likes_xpath).text
                        number_of_likes = format_thousands_str_spanish(number_of_likes)
                    except NoSuchElementException:
                        number_of_likes = randint(0, 1)
                    try:
                        user_href_xpath = '//article/header//h2/a'
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
                                nap(0.72)
                                respect_hourly_rate_limits(browser, action='follow')
                                followed_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
                                if follow_blocked:
                                    return
                                print('Followed = ', user_href, followed_datetime)
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
                                    sets_of_n_actions = round(follows_per_tag * uniform(0.75, 1.23))
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
                            except (NoSuchElementException, ElementClickInterceptedException):
                                pass
                            finally:
                                try:
                                    close_post_window_xpath = '//*[contains(text(), "Cerrar")]'
                                    close_post_window = browser.find_element_by_xpath(close_post_window_xpath)
                                    close_post_window.click()
                                except NoSuchElementException:
                                    pass
                    try:
                        close_post_window_xpath = '//*[contains(text(), "Cerrar")]'
                        close_post_window = browser.find_element_by_xpath(close_post_window_xpath)
                        close_post_window.click()
                    except NoSuchElementException:
                        pass
                    already_viewed_xpaths.append(post_xpath)
            nap(0.48)
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
                with open(file_path, 'wb') as file_1:
                    pickle.dump(black_list, file_1)
        file_1.close()

        if any(dump_to_tag_analysis):
            tag_analysis.update(dump_to_tag_analysis)
            file_path = current_working_directory + file_2_name
            try:
                with open(file_path, 'wb') as file_2:
                    pickle.dump(dump_to_tag_analysis, file_2)
            except IOError:
                os_chmod(file_path, S_IRWXU)
                with open(file_path, 'wb') as file_2:
                    pickle.dump(dump_to_tag_analysis, file_2)
        file_2.close()
