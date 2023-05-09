from datetime import datetime
from os import getpid
from os import times
from random import randint
from random import seed
from random import uniform
from time import sleep

seed_str = str(datetime.now()) + str(getpid()) + str(times())


def new_seed():
    if 0.1 > uniform(0, 1):
        seed(str(randint(0, 1_000_000)) + seed_str + str(uniform(0, 10)))


def nap(seconds):
    variation = 0.24
    new_seed()
    if 0.91 > uniform(0, 1):
        seconds = seconds * uniform(1 - variation, 1 + variation)
    else:
        seconds = seconds * uniform(1, 4)
    sleep(seconds)
