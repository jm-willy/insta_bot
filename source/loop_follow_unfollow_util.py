import pickle

from insta_bot.source.follow_by_tag_util import follow_by_tag
from insta_bot.source.follow_by_tag_util import followed_this_run
from insta_bot.source.relationship_util import followers_lst
from insta_bot.source.relationship_util import global_followback_rate
from insta_bot.source.relationship_util import unfollow_non_followers
from insta_bot.source.relationship_util import unfollowed_this_run


def loop_f_uf(browser, tags_to_follow_users, ignore_users,
              action_delay=43, sets_of_n_actions=4, set_delay=251,
              max_actions=200, days_to_wait_to_unfollow=3, max_likes_to_follow=35,
              my_username='', followback_rate=0.03, loops=3, f=True, uf=True, watch_stories=False):
    count = 0
    f_per_loop = max_actions * 0.5
    uf_per_loop = (max_actions * 0.5) * (1 - followback_rate)
    remainder = max_actions - f_per_loop - uf_per_loop

    try:
        while count < loops:
            if uf:
                uf_this_loop = round(((remainder * 0.5) + uf_per_loop - 1) / loops)
                if uf_this_loop < 1:
                    uf_this_loop = 1
                print('unfollow_this_loop =', uf_this_loop)
                unfollow_non_followers(browser, ignore_users, action_delay=action_delay,
                                       sets_of_n_actions=sets_of_n_actions, set_delay=set_delay,
                                       max_unfollows=uf_this_loop,
                                       days_to_wait_to_unfollow=days_to_wait_to_unfollow, my_username=my_username)
            if f:
                f_this_loop = round(((remainder * 0.5) + f_per_loop + 1) / loops)
                if f_this_loop < 1:
                    f_this_loop = 1
                print('follow_this_loop =', f_this_loop)
                follow_by_tag(browser, tags_to_follow_users, follows_per_tag=(sets_of_n_actions + 1),
                              max_follows=f_this_loop, max_likes_to_follow=max_likes_to_follow,
                              action_delay=action_delay, set_delay=set_delay,
                              watch_stories=watch_stories)
            count += 1
    finally:
        print('-' * 41)
        print('followed_this_run =', len(followed_this_run))
        print('unfollowed_this_run =', len(unfollowed_this_run))
        if followback_rate is None:
            print('followback_rate =', global_followback_rate)
        print(' ')

        # tag analysis
        if any(followers_lst):
            print('tag_analysis:')
            with open('tag_analysis.pickle', 'rb') as file_1:
                tag_analysis = pickle.load(file_1)
            for tag in tags_to_follow_users:
                followed_per_tag = 0
                followed_back_per_tag = 0
                for user in tag_analysis:
                    if tag == tag_analysis[user]:
                        followed_per_tag += 1
                        if user in followers_lst:
                            followed_back_per_tag += 1
                followback_rate_per_tag = followed_back_per_tag / followed_per_tag
                print('tag =', tag, 'followback_rate_per_tag =', followback_rate_per_tag)
