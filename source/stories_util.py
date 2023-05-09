from random import uniform
from time import sleep

from insta_bot.source.nap_util import nap
from insta_bot.source.respect_limits_util import global_skip_stories
from insta_bot.source.respect_limits_util import respect_hourly_rate_limits
from insta_bot.source.respect_limits_util import stories_blocked
from selenium.common.exceptions import NoSuchElementException

max_stories = 12
max_story_duration = 15
wait_to_watch = max_stories * max_story_duration


def watch_stories_in_page(browser, probability=0.44):
    if stories_blocked:
        return
    if probability > uniform(0, 1):
        if not global_skip_stories:
            try:
                stories_xpath = '//*[@id="react-root"]//section//main/header//img'
                stories = browser.find_element_by_xpath(stories_xpath)
                stories.click()
                'bot_click(browser, xpath=stories_xpath)'
                sleep(wait_to_watch)
                for i in range(0, max_stories):
                    respect_hourly_rate_limits(browser, action='stories')
                nap(2.11)
            except NoSuchElementException:
                pass
