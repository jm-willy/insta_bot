# for common and long xpaths


def get_xpath(name=''):
    if name == 'number_of_likes_xpath':
        number_of_likes_xpath = '//*[@id="react-root"]//section/div/div/button/span'
        return number_of_likes_xpath
    elif name == 'number_of_likes_xpath_2':
        number_of_likes_xpath_2 = '//section[2]//button/span'
        return number_of_likes_xpath_2
    elif name == 'number_of_tags_xpath':
        number_of_tags_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/ul/div/li/div' \
                               '/div[1]/div[2]/h3/*[@title="{}"]/following::span[1]/a'
        return number_of_tags_xpath
    elif name == 'tags_in_profile_comment_xpath':
        tags_in_profile_comment_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]' \
                                        '/div[1]/ul/ul/div/li/div/div[1]/div[2]/h3/*[@title="{}"]' \
                                        '/following::span[1]/a[{}]'
        return tags_in_profile_comment_xpath

    elif name == 'number_of_followers_xpath':
        number_of_followers_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'
        return number_of_followers_xpath
    elif name == 'number_of_following_xpath':
        number_of_following_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
        return number_of_following_xpath
    elif name == 'number_of_followers_xpath_2':
        number_of_followers_xpath_2 = '//*[@role="presentation"]//div[text()="Seguidores"]/following::div[2]//li'
        return number_of_followers_xpath_2
    elif name == 'number_of_following_xpath_2':
        number_of_following_xpath_2 = '//*[@role="presentation"]//div[text()="Siguiendo"]/following::div[2]//li'
        return number_of_following_xpath_2

    elif name == 'followers_xpath_1':
        followers_xpath_1 = '//*[@role="presentation"]//div[text()="Seguidores"]/following::div[2]//li/div/div[' \
                            '2]/div/div/div/a'
        return followers_xpath_1
    elif name == 'following_xpath_1':
        following_xpath_1 = '//*[@role="presentation"]//div[text()="Siguiendo"]/following::div[2]//li/div/div[' \
                            '2]/div/div/div/a'
        return following_xpath_1
    elif name == 'followers_xpath_2':
        followers_xpath_2 = '//*[@role="presentation"]//div[text()="Seguidores"]/following::div[2]//li{}/div/div/div[' \
                            '2]/div/a'
        return followers_xpath_2
    elif name == 'following_xpath_2':
        following_xpath_2 = '//*[@role="presentation"]//div[text()="Siguiendo"]/following::div[2]//li{}/div/div/div[' \
                            '2]/div/a'
        return following_xpath_2

    elif name == 'followers_button_xpath':
        followers_button_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        return followers_button_xpath
    elif name == 'following_button_xpath':
        following_button_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        return following_button_xpath
    elif name == 'followers_window_xpath':
        followers_window_xpath = '//*[@role="presentation"]//div[text()="Seguidores"]/following::div[2]'
        return followers_window_xpath
    elif name == 'following_window_xpath':
        following_window_xpath = '//*[@role="presentation"]//div[text()="Siguiendo"]/following::div[2]'
        return following_window_xpath
    elif name == 'close_followers_xpath':
        close_followers_xpath = '//*[@role="presentation"]//div[text()="Seguidores"]/following::div[1]//*[' \
                                '@aria-label="Cerrar"]'
        return close_followers_xpath
    elif name == 'close_following_xpath':
        close_following_xpath = '//*[@role="presentation"]//div[text()="Siguiendo"]/following::div[1]//*[' \
                                '@aria-label="Cerrar"]'
        return close_following_xpath

    elif name == 'post_count_xpath':
        post_count_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
        return post_count_xpath

    else:
        raise ValueError
