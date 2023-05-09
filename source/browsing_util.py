from datetime import datetime
from random import randint
from random import uniform

from insta_bot.source.generate_curves_util import curve_from_straight
from insta_bot.source.nap_util import nap
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

last_x_mouse_position = None
last_y_mouse_position = None

full_human_emulation = False

dirty_input_text_field = False
dirty_input_text_len = 0


def set_full_human_emulation(use_full_human_emulation=False):
    global full_human_emulation
    full_human_emulation = use_full_human_emulation
    if full_human_emulation:
        print('full_human_emulation =', full_human_emulation)
        print('Reminder: Mouse should NOT be placed inside any active window')


def go_to_link(browser, link):
    count = 0
    nap(1.11)
    while browser.current_url != link and count < 10:
        if count > 0:
            print('reloading page =', browser.current_url, 'attempts =', count, 'target link =', link)
        browser.get(link)
        count += 1
        nap(1.33 + (count * 3))


def insta_bar_search(browser, search='', finally_go_to_link=False):
    global dirty_input_text_field
    global dirty_input_text_len

    link = ''
    if 'https' in search:
        link = search
    elif '#' in search:
        link = 'https://www.instagram.com/explore/tags/{}/'.format(search[1:])

    search_bar_xpath = '//*[@id="react-root"]//input[@placeholder="Busca"]'
    try:
        if dirty_input_text_field:
            search_bar = browser.find_element_by_xpath(search_bar_xpath)
            browser.execute_script("arguments[0].click();", search_bar)
            if 0.86 > uniform(0, 1):
                for character in range(0, randint(dirty_input_text_len, dirty_input_text_len + 6)):
                    search_bar.send_keys(Keys.BACK_SPACE)
            else:
                search_bar.send_keys(Keys.CONTROL + 'a')
                search_bar.send_keys(Keys.DELETE)

        if 'https' in search:
            search = search[26:-1]
        search_bar = browser.find_element_by_xpath(search_bar_xpath)
        browser.execute_script("arguments[0].click();", search_bar)
        'bot_click(browser, xpath=search_bar_xpath)'
        nap(1.97)
        search_bar = browser.find_element_by_xpath(search_bar_xpath)
        search_bar.send_keys(search)
        nap(3.93)
        search_result_xpath = '//*[@id="react-root"]//span[text()="{}"]'.format(search)
        if 0.63 > uniform(0, 1):
            search_result = browser.find_element_by_xpath(search_result_xpath)
            'browser.execute_script("arguments[0].click();", search_result)'
            search_result.click()
            'bot_click(browser, xpath=search_result_xpath)'
        else:
            search_bar = browser.find_element_by_xpath(search_bar_xpath)
            search_bar.send_keys(Keys.ENTER)
        dirty_input_text_field = False
    except (ElementClickInterceptedException, ElementNotInteractableException):
        nap(1)
        search_bar = browser.find_element_by_xpath(search_bar_xpath)
        search_bar.send_keys(Keys.ENTER)
        dirty_input_text_field = False
    except NoSuchElementException:
        dirty_input_text_field = True
        dirty_input_text_len = len(search)
        print('Not found in search bar =', search, datetime.now().strftime('%Y-%m-%d %H:%M'))
    finally:
        if finally_go_to_link:
            go_to_link(browser, link)
        else:
            pass


def open_link_in_new_tab(browser, link, switch=True):
    script = 'window.open("{}", "_blank")'.format(link)
    browser.execute_script(script)
    nap(1.79)
    if switch:
        browser.switch_to_window(browser.window_handles[1])
        nap(0.73)
    else:
        nap(0.41)
        browser.switch_to_window(browser.window_handles[0])
        nap(0.67)


def close_secondary_tab(browser):
    browser.switch_to_window(browser.window_handles[0])
    nap(0.19)
    browser.close()


# makes a left click doesn't work
def open_link_new_tab_right_click(browser, xpath='', switch=True):
    action = ActionChains(browser)
    element = browser.find_element_by_xpath(xpath)
    action.context_click(element)
    action.pause(0.66)
    action.send_keys(Keys.ARROW_DOWN)
    action.pause(0.66)
    action.send_keys(Keys.ENTER)
    action.perform()
    if switch:
        browser.switch_to_window(browser.window_handles[1])
        nap(0.73)
    else:
        nap(0.41)
        browser.switch_to_window(browser.window_handles[0])
        nap(0.67)


# type this in the console to get cursor coordinates:
'''document.addEventListener("mouseover", function( event ) {   
    console.log(event.screenX, event.screenY);
}, false);'''


def off_center_click(browser, xpath=''):
    global last_x_mouse_position
    global last_y_mouse_position

    element = browser.find_element_by_xpath(xpath)
    x_size = element.size['width']
    y_size = element.size['height']
    x_coordinate = element.location['x']
    y_coordinate = element.location['y']
    final_x = randint(round(x_coordinate - (x_size * 0.43)), round(x_coordinate + (x_size * 0.43)))
    final_y = randint(round(y_coordinate - (y_size * 0.43)), round(y_coordinate + (y_size * 0.43)))

    print(final_x, final_y)

    action = ActionChains(browser)
    action.move_by_offset(final_x, final_y)
    action.click()
    action.perform()

    last_x_mouse_position = final_x
    last_y_mouse_position = final_y


def move_mouse(browser, xpath='', click=False):
    global last_x_mouse_position
    global last_y_mouse_position

    'get html display dimensions'
    html = browser.find_element_by_xpath('//html')
    width_html = html.size['width']
    height_html = html.size['height']
    if last_x_mouse_position is None or last_x_mouse_position > width_html:
        first_x_mouse_position = randint(0, width_html)
    else:
        first_x_mouse_position = last_x_mouse_position
    if last_y_mouse_position is None or last_y_mouse_position > height_html:
        first_y_mouse_position = randint(0, height_html)
    else:
        first_y_mouse_position = last_y_mouse_position
    action = ActionChains(browser)
    action.move_by_offset(first_x_mouse_position, first_y_mouse_position).perform()

    element = browser.find_element_by_xpath(xpath)
    x_size = element.size['width']
    y_size = element.size['height']
    x_coordinate = element.location['x']
    y_coordinate = element.location['y']

    final_x = randint(round(x_coordinate - (x_size * 0.39)), round(x_coordinate + (x_size * 0.39)))
    final_y = randint(round(y_coordinate - (y_size * 0.39)), round(y_coordinate + (y_size * 0.39)))

    final_path = curve_from_straight(start_x=first_x_mouse_position, start_y=first_y_mouse_position,
                                     end_x=final_x, end_y=final_y)
    print('final_path', final_path)
    print('size', width_html, height_html)
    print(final_x, final_y)
    for x, y in final_path:
        try:
            action = ActionChains(browser)
            action.move_by_offset(x, y).perform()
        except MoveTargetOutOfBoundsException:
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            action = ActionChains(browser)
            action.move_by_offset(x, y).perform()

    if click:
        off_center_click(browser, xpath)
    else:
        last_x_mouse_position = final_x
        last_y_mouse_position = final_y


def random_mouse(browser, within_element_xpath=None, movements=3):
    global last_x_mouse_position
    global last_y_mouse_position

    if full_human_emulation:
        action = ActionChains(browser)
        if within_element_xpath is None:
            element = browser.find_element_by_xpath('//html')
        else:
            element = browser.find_element_by_xpath(within_element_xpath)
        x_size = element.size['width']
        y_size = element.size['height']
        x_coordinate = element.location['x']
        y_coordinate = element.location['y']

        if last_x_mouse_position is None or last_x_mouse_position > x_size:
            first_x = randint(round(x_coordinate - x_size), round(x_coordinate + x_size))
        else:
            first_x = last_x_mouse_position
        if last_y_mouse_position is None or last_y_mouse_position > y_size:
            first_y = randint(round(y_coordinate - y_size), round(y_coordinate + y_size))
        else:
            first_y = last_y_mouse_position

        random_range = randint(0, movements + 1)
        for i in random_range(0, random_range):
            # generate two random points within the element

            last_x = randint(round(x_coordinate - x_size), round(x_coordinate + x_size))
            last_y = randint(round(y_coordinate - y_size), round(y_coordinate + y_size))

            path = curve_from_straight(start_x=first_x, start_y=first_y, end_x=last_x, end_y=last_y)

            for x, y in path:
                action.move_by_offset(x, y)
            last_x_mouse_position = last_x
            last_y_mouse_position = last_y
        action.perform()
    nap(0.77)


def format_thousands_str_spanish(string):
    result = []
    for i in string:
        if i != '.':
            result.append(i)
    result = ''.join(result)
    return int(result)


def bot_click(browser, xpath=''):
    if full_human_emulation:
        off_center_click(browser, xpath)
        'move_mouse(browser, xpath, click=True)'
    else:
        element = browser.find_element_by_xpath(xpath)
        element.click()
