import requests as req
import json
import time
from tqdm import tqdm
import riot_function as rf

while(1):
    menu = int(input('''
메뉴를 골라주세요.

1. 소환사명 검색
2. 종료
'''))
    if menu == 1:
        s_name = input('소환사명을 입력해주세요: ')
        rf.get_info_by_summoner_name(s_name)
    else:
        break