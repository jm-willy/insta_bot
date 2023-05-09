import pickle
from insta_bot.source.login_util import current_working_directory

from datetime import datetime


file_1_name = 'black_list_file.pickle'
file_path = current_working_directory + file_1_name

try:
    with open(file_path, 'rb') as file_1:
        black_list = pickle.load(file_1)
except FileNotFoundError:
    black_list = {}
    with open(file_path, 'wb') as file_1:
        pickle.dump(black_list, file_1)


for key in black_list:
    timestamp = black_list[key]
    dt_object = datetime.fromtimestamp(timestamp)
    print(key, dt_object)
