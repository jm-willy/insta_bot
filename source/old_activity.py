from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

my_username = 'your user_name here'
my_password = ''
user_to_get_following = ''
user_data_path = '- - - -'
driver_path = '- - - - '
use_xpath_for_finding_following = False
use_css_selector_for_finding_following = True
###############################################################
chrome_options = Options()
chrome_options.add_argument("--user-data-dir={}".format(user_data_path))
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
browser.implicitly_wait(11)

logged = False
login_button_xpath = '//button[text()="Log In"]'
my_profile_link = 'https://www.instagram.com/{}/'.format(my_username)
browser.get(my_profile_link)
#
try:
    login_button = browser.find_element_by_xpath(login_button_xpath)
    login_button.click()
except NoSuchElementException:
    logged = True

if not logged:
    my_username_input_xpath = '//input[@name="username"]'
    my_username_input = browser.find_element_by_xpath(my_username_input_xpath)
    my_username_input.send_keys(my_username)
    sleep(3)
    my_password_input_xpath = '//input[@name="password"]'
    my_password_input = browser.find_element_by_xpath(my_password_input_xpath)
    my_password_input.send_keys(my_password)
    sleep(3)
    final_login_button_xpath = '//button[@type="submit"]'
    final_login_button = browser.find_element_by_xpath(final_login_button_xpath)
    final_login_button.click()
    sleep(3)
    try:
        login_button = browser.find_element_by_xpath(login_button_xpath)
        login_button.click()
    except NoSuchElementException:
        logged = True
#

number_of_following_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
following_window_xpath = '//*[@role="presentation"]//div[text()="Following"]/following::div[2]'
following_xpath_1 = '//*[@role="presentation"]//div[text()="Following"]/following::div[2]//li/div/div/div[2]/div/a'
following_xpath_2 = '//*[@role="presentation"]//div[text()="Following"]/following::div[2]//li/div/div/div[2]/div/a'
browser.get('https://www.instagram.com/{}/'.format(user_to_get_following))
number_of_following = int(browser.find_element_by_xpath(number_of_following_xpath).text)

following_lst = []
absolute_scroll = 0
for i in range(0, round(number_of_following * 0.5)):
    if i < 40:
        base_scroll = 35
    else:
        base_scroll = 375
    absolute_scroll = str(absolute_scroll + base_scroll)
    try:
        following_window = browser.find_element_by_xpath(following_window_xpath)
        browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), following_window)
    except NoSuchElementException:
        following_window = browser.find_element_by_xpath(following_window_xpath)
        browser.execute_script('arguments[0].scrollTop = {}'.format(absolute_scroll), following_window)
    if use_xpath_for_finding_following:
        following_elements = browser.find_elements_by_xpath(following_xpath_1)
    elif use_css_selector_for_finding_following:
        following_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
    if len(following_lst) <= 12:
        try:
            for element in following_elements:
                href = element.get_attribute('href')
                if href not in following_lst and href is not None:
                    following_lst.append(href)
        except StaleElementReferenceException:
            if use_xpath_for_finding_following:
                following_elements = browser.find_elements_by_xpath(following_xpath_1)
            elif use_css_selector_for_finding_following:
                following_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
            for element in following_elements:
                href = element.get_attribute('href')
                if href not in following_lst and href is not None:
                    following_lst.append(href)
        except NoSuchElementException:
            pass
    else:
        if use_xpath_for_finding_following:
            following_elements = browser.find_elements_by_xpath(following_xpath_1)
        elif use_css_selector_for_finding_following:
            following_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
        try:
            for element in following_elements:
                href = element.get_attribute('href')
                if href not in following_lst and href is not None:
                    following_lst.append(href)
        except StaleElementReferenceException:
            if use_xpath_for_finding_following:
                following_elements = browser.find_elements_by_xpath(following_xpath_1)
            elif use_css_selector_for_finding_following:
                following_elements = browser.find_elements_by_css_selector('.FPmhX.notranslate')
            for element in following_elements:
                href = element.get_attribute('href')
                if href not in following_lst and href is not None:
                    following_lst.append(href)
        except NoSuchElementException:
            pass