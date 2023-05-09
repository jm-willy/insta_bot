# -*- coding: UTF-8 -*-

from datetime import datetime
from insta_bot.source.browsing_util import go_to_link
from insta_bot.source.nap_util import nap
from insta_bot.source.respect_limits_util import comment_blocked
from insta_bot.source.respect_limits_util import respect_hourly_rate_limits
from insta_bot.source.xpaths import get_xpath
from random import shuffle
from random import uniform


def re_comment_own_posts(browser, action_delay=180, sets_of_n_actions=5, set_delay=660, my_username='',
                         last_to_first_order=False):
    if comment_blocked:
        return

    avg_engagement = 0.036
    counter = 0
    sets_of_n_actions_original = sets_of_n_actions
    sets_of_n_actions = round(sets_of_n_actions * uniform(0.71, 1.23))

    my_profile_link = 'https://www.instagram.com/{}/'.format(my_username)
    go_to_link(browser, my_profile_link)

    number_of_followers_xpath = get_xpath(name='number_of_followers_xpath')
    number_of_followers = int(browser.find_element_by_xpath(number_of_followers_xpath).text)

    post_count_xpath = get_xpath(name='post_count_xpath')
    post_count = int(browser.find_element_by_xpath(post_count_xpath).text)

    post_links_lst = []
    for i in range(0, round(post_count / 3) + 1):
        random_scroll_amount = str(round(279 * uniform(0.89, 1.15)))
        browser.execute_script("window.scrollBy(0, {})".format(random_scroll_amount))
        post_hrefs = browser.find_elements_by_xpath('//*[@id="react-root"]//a[starts-with(@href, "/p/")]')
        for href in post_hrefs:
            href = href.get_attribute('href')
            if href not in post_links_lst:
                post_links_lst.append(href)
        nap(2.57)
    nap(2.73)

    if last_to_first_order:
        post_links_lst.reverse()

    counter_1 = 0
    print('Number of posts =', len(post_links_lst))
    for post_link in post_links_lst:
        go_to_link(browser, post_link)

        load_more_comments_xpath = '//*[@id="react-root"]//*[@aria-label="Load more comments"]'

        number_of_tags_xpath = get_xpath(name='number_of_tags_xpath')
        number_of_tags_xpath = number_of_tags_xpath.format(my_username)
        number_of_tags = len(browser.find_elements_by_xpath(number_of_tags_xpath))

        number_of_likes_xpath = get_xpath(name='number_of_likes_xpath')
        number_of_likes = int(browser.find_element_by_xpath(number_of_likes_xpath).text)
        nap(0.8)
        prb = 12 + (number_of_followers * avg_engagement * 0.1)
        if (prb / number_of_likes) > uniform(0.0, 1.0) or number_of_likes < (avg_engagement * number_of_followers):
            n_likes_bool = True
        else:
            n_likes_bool = False

        tags_in_comment = []
        if number_of_tags > 1 and n_likes_bool:
            while_counter = 0
            while number_of_tags > len(tags_in_comment) and while_counter < 4:
                print('Getting every tag...')
                tags_in_comment.clear()
                for tags in range(1, number_of_tags):
                    tags_in_profile_comment_xpath = get_xpath(name='tags_in_profile_comment_xpath')
                    tags_in_profile_comment_xpath = tags_in_profile_comment_xpath.format(my_username, str(tags))
                    tags = str(browser.find_element_by_xpath(tags_in_profile_comment_xpath).text).encode()
                    tags_in_comment.append(tags)
                    nap(0.29)
                while_counter += 1

            shuffle(tags_in_comment)

            comment_options_button_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]' \
                                           '/ul/ul/div/li/div/div[1]/div[2]/h3' \
                                           '/*[@title="{}"]/following::span[2]'.format(my_username)

            comment_options_button = browser.find_element_by_xpath(comment_options_button_xpath)
            browser.execute_script("arguments[0].click();", comment_options_button)
            nap(1.33)

            delete_button_xpath = '//*[@role="presentation"]//*[@role="dialog"]/div/div/button[2]'
            delete_button = browser.find_element_by_xpath(delete_button_xpath)
            delete_button.click()
            nap(1.33)

            space_bar = ' '
            comment_input_xpath = '//*[@id="react-root"]//textarea[@placeholder="Añade un comentario..."]'
            comment_input = browser.find_element_by_xpath(comment_input_xpath)
            comment_input.click()
            for utf8_bytes in tags_in_comment:
                utf8_decoded = utf8_bytes.decode()  # also str(utf8_bytes)
                comment_input = browser.find_element_by_xpath(comment_input_xpath)
                comment_input.send_keys(utf8_decoded + space_bar)
                nap(0.57)
                current_tags = browser.find_element_by_xpath(comment_input_xpath).text
                while utf8_decoded not in current_tags:
                    nap(0.11)
                    comment_input = browser.find_element_by_xpath(comment_input_xpath)
                    comment_input.send_keys(utf8_decoded + space_bar)
                    current_tags = browser.find_element_by_xpath(comment_input_xpath).text
                    nap(0.20)
                else:
                    pass

            tags_in_comment.clear()

            post_button_xpath = '//*[@id="react-root"]//*[@type="submit"]'
            post_button = browser.find_element_by_xpath(post_button_xpath)
            post_button.click()
            nap(action_delay * 0.05)
            respect_hourly_rate_limits(browser, action='comment')
            if comment_blocked:
                return

            print('Commented = ', post_link, datetime.now().strftime('%Y-%m-%d %H:%M'))
            counter += 1
            nap(action_delay * 0.95)

            if counter >= sets_of_n_actions:
                counter = 0
                sets_of_n_actions = round(sets_of_n_actions_original * uniform(0.75, 1.19))
                print('>---Sleeping after a few re_comments---<')
                nap(set_delay)

        else:
            print('Enough likes or no tags: skipped', post_link, datetime.now().strftime('%Y-%m-%d %H:%M'))
            nap(action_delay * 0.33)

        counter_1 += 1
        print('Re_comments completed = ', counter_1 / len(post_links_lst))
