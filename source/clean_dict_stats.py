# run to clean stats dict
import pickle
from os import chmod as os_chmod
from stat import S_IRWXU

from insta_bot.source.login_util import current_working_directory

file_1_name = 'black_list_file.pickle'
file_path = current_working_directory + file_1_name
try:
    with open(file_path, 'rb') as file_1:
        black_list = pickle.load(file_1)
except FileNotFoundError:
    pass

file_2_name = 'tag_analysis.pickle'
file_path = current_working_directory + file_2_name
try:
    with open(file_path, 'rb') as file_2:
        tag_analysis = pickle.load(file_2)
except FileNotFoundError:
    pass

black_list_keys = list(black_list.keys())
print(len(black_list_keys))
print()
print(black_list_keys)

cut = black_list_keys.index('https://www.instagram.com/pilou_fred/')

black_list_keys = black_list_keys[cut:]
print(len(black_list_keys))
print(black_list_keys)
print(tag_analysis)

clean_tag_analysis = {}
clean_black_list = {}

for user in black_list_keys:
    del black_list[user]
    del tag_analysis[user]

file_path = current_working_directory + file_1_name

try:
    with open(file_path, 'wb') as file_1:
        pickle.dump(black_list, file_1)
except IOError:
    os_chmod(file_path, S_IRWXU)
    with open(file_path, 'wb') as file_2:
        tag_analysis.dump(tag_analysis, file_2)
file_1.close()

file_path = current_working_directory + file_2_name
try:
    with open(file_path, 'wb') as file_2:
        tag_analysis.dump(tag_analysis, file_2)
except IOError:
    os_chmod(file_path, S_IRWXU)
    with open(file_path, 'wb') as file_2:
        tag_analysis.dump(tag_analysis, file_2)
file_2.close()
