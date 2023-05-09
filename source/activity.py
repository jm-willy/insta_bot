# -*- coding: UTF-8 -*-
from sys import exit as sys_exit
from time import sleep

from insta_bot.source.browsing_util import set_full_human_emulation
from insta_bot.source.login_util import current_working_directory
from insta_bot.source.login_util import log_in
from insta_bot.source.loop_follow_unfollow_util import loop_f_uf
from insta_bot.source.recomment_util import re_comment_own_posts
from insta_bot.source.respect_limits_util import set_hourly_limits
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sleep(1)

# set chrome driver
chrome_options = Options()
user_data_path = 'C:/Users/User/AppData/Local/Google/Chrome/User Data/Default'
chrome_options.add_argument("--user-data-dir={}".format(user_data_path))
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver_path = current_working_directory + 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
browser.implicitly_wait(31)


#
'''Login credentials'''
my_username = 'my_user'
my_password = '****'
#
tags_to_follow_users = []

ignore_users = ["dont_unfollow", "example_1"]

#
'''Activity'''
#

set_full_human_emulation(use_full_human_emulation=False)

log_in(browser, my_username=my_username, my_password=my_password, open_more_tabs=False, start_timer_hours=0)

set_hourly_limits(follow_limit=23, unfollow_limit=23,
                  comment_limit=11, stories_limit=20,
                  minutes_to_stop=7, max_hours_to_run=7)

loop_f_uf(browser, tags_to_follow_users, ignore_users,
          action_delay=115, sets_of_n_actions=4, set_delay=184,
          max_actions=100, days_to_wait_to_unfollow=2, max_likes_to_follow=25,
          my_username=my_username, followback_rate=0.06, loops=9, f=True, uf=False,
          watch_stories=False)

re_comment_own_posts(browser, action_delay=173, sets_of_n_actions=4,
                     set_delay=297, my_username=my_username, last_to_first_order=False)

sys_exit()
