import os
from time import sleep

dir = os.path.dirname(__file__)
dir += "/DATA/"

files = os.listdir(dir)

for file in files:
    os.system(f'python converter.py {dir+file}')
    sleep(2)