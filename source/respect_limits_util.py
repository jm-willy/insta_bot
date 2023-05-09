from datetime import datetime
from random import uniform
from sys import exit as sys_exit
from time import time

from insta_bot.source.nap_util import nap
from selenium.common.exceptions import NoSuchElementException

follow_blocked = False
unfollow_blocked = False
comment_blocked = False
stories_blocked = False

follow_count = 0
unfollow_count = 0
comment_count = 0
start_timer = time()
start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
last_hour_started = time()
stories_count = 0

global_follow_limit = 0
global_unfollow_limit = 0
global_comment_limit = 0
global_minutes_to_stop = 0
global_max_hours_to_run = 0
global_stories_limit = 0
global_skip_stories = False


def set_hourly_limits(follow_limit=15, unfollow_limit=15,
                      comment_limit=15, stories_limit=100,
                      minutes_to_stop=30, max_hours_to_run=2):
    global global_follow_limit
    global global_unfollow_limit
    global global_comment_limit
    global global_minutes_to_stop
    global global_max_hours_to_run
    global global_stories_limit

    global_follow_limit = follow_limit
    global_unfollow_limit = unfollow_limit
    global_comment_limit = comment_limit
    global_minutes_to_stop = minutes_to_stop
    global_max_hours_to_run = max_hours_to_run * uniform(0.95, 1.05)
    global_stories_limit = stories_limit


follow_limit = round(global_follow_limit * uniform(0.89, 1))
unfollow_limit = round(global_unfollow_limit * uniform(0.89, 1))
comment_limit = round(global_comment_limit * uniform(0.89, 1))
seconds_to_stop = global_minutes_to_stop * 60 * uniform(0.96, 1.04)
stories_limit = round(global_stories_limit * uniform(0.67, 1))


def respect_hourly_rate_limits(browser, action=''):
    global follow_count
    global unfollow_count
    global comment_count
    global last_hour_started
    global stories_count
    global global_skip_stories

    global follow_limit
    global unfollow_limit
    global comment_limit
    global seconds_to_stop
    global stories_limit

    current_time = time()

    if (current_time - start_timer) > (60 * 60 * global_max_hours_to_run):
        print('_' * 41)
        print('Started,', start_timestamp)
        print('Max hours to run completed', datetime.now().strftime('%Y-%m-%d %H:%M'))
        sys_exit()

    if (current_time - last_hour_started) > (60 * 60):
        print('_' * 41)
        print('Past hourly rates', datetime.now().strftime('%Y-%m-%d %H:%M'))
        if follow_count > 0:
            print('Follow rate', follow_count)
        if unfollow_count > 0:
            print('Unfollow rate', unfollow_count)
        if comment_count > 0:
            print('Comment rate', comment_count)
        if stories_count > 0:
            print('Stories rate', stories_count)
        print('*' * 41)
        last_hour_started = time()
        follow_count = 0
        unfollow_count = 0
        comment_count = 0
        stories_count = 0
        follow_limit = round(global_follow_limit * uniform(0.89, 1))
        unfollow_limit = round(global_unfollow_limit * uniform(0.89, 1))
        comment_limit = round(global_comment_limit * uniform(0.89, 1))
        seconds_to_stop = global_minutes_to_stop * 60 * uniform(0.96, 1.04)
        stories_limit = round(global_stories_limit * uniform(0.67, 1))

    if action == 'follow':
        detect_block(browser, current_action='follow')
        follow_count += 1
        if follow_count >= follow_limit:
            print('_' * 41)
            print('>>Sleeping to respect limits, action: follow', datetime.now().strftime('%Y-%m-%d %H:%M'))
            nap(seconds_to_stop)
            print('Resumed', datetime.now().strftime('%Y-%m-%d %H:%M'))
            print('_' * 41)

    elif action == 'unfollow':
        detect_block(browser, current_action='unfollow')
        unfollow_count += 1
        if unfollow_count >= unfollow_limit:
            print('_' * 41)
            print('>>Sleeping to respect limits, action: unfollow', datetime.now().strftime('%Y-%m-%d %H:%M'))
            nap(seconds_to_stop)
            print('Resumed', datetime.now().strftime('%Y-%m-%d %H:%M'))
            print('_' * 41)

    elif action == 'comment':
        detect_block(browser, current_action='comment')
        comment_count += 1
        if comment_count >= comment_limit:
            print('_' * 41)
            print('>>Sleeping to respect limits, action: comment', datetime.now().strftime('%Y-%m-%d %H:%M'))
            nap(seconds_to_stop)
            print('Resumed', datetime.now().strftime('%Y-%m-%d %H:%M'))
            print('_' * 41)

    elif action == 'stories':
        detect_block(browser, current_action='stories')
        stories_count += 1
        if stories_count >= stories_limit:
            global_skip_stories = True

    else:
        raise ValueError


def detect_block(browser, current_action=''):
    global follow_blocked
    global unfollow_blocked
    global comment_blocked
    global stories_blocked

    nap(0.55)
    text_sample_lst = ['Based on previous use of this feature',
                       'your account has been temporarily blocked from taking this action',
                       'This block will expire on',
                       'We restrict certain content and actions to protect our community',
                       'Tell us if you think we made a mistake',
                       'This action was blocked',
                       "You've been temporarily blocked from using it"]
    for text_sample in text_sample_lst:
        try:
            browser.find_element_by_xpath('//*[contains(text(), "{}")]'.format(text_sample))
            block_warning =  browser.find_elements_by_xpath('//*[contains(text(), "{}")]'.format(text_sample))
            if any(block_warning):
                if current_action == 'follow':
                    follow_blocked = True
                    print('!' * 41)
                    print('Block detected', datetime.now().strftime('%Y-%m-%d %H:%M'))
                    print('Blocked from', current_action, ', skipping')
                    s = 1/0
                    #driver.save_screenshot("screenshot.png")
                elif current_action == 'unfollow':
                    unfollow_blocked = True
                    print('!' * 41)
                    print('Block detected', datetime.now().strftime('%Y-%m-%d %H:%M'))
                    print('Blocked from', current_action, ', skipping')
                    s = 1 / 0
                elif current_action == 'comment':
                    comment_blocked = True
                    print('!' * 41)
                    print('Block detected', datetime.now().strftime('%Y-%m-%d %H:%M'))
                    print('Blocked from', current_action, ', skipping')
                elif current_action == 'stories':
                    stories_blocked = True
                    print('!' * 41)
                    print('Block detected', datetime.now().strftime('%Y-%m-%d %H:%M'))
                    print('Blocked from', current_action, ', skipping')
                else:
                    raise ValueError
        except NoSuchElementException:
            pass
