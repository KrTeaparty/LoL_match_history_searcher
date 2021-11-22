import requests as req
import json
import time
from tqdm import tqdm
import riot_function as rf


while(1):
    summoner_name = input('정보를 검색할 소환사명 입력 (검색 종료를 원할시 q입력) : ')
    l_class = rf.League_of_Legend(summoner_name)

    if summoner_name == 'q':
        break

    if l_class.valid_name == 0:
        continue

    while(1):
        menu = int(input('''
메뉴를 골라주세요.

1. 레벨 보기
2. 챔피언 숙련도 보기
3. 종료
'''))
        if menu == 1:
            l_class.get_info_by_summoner_name()
        elif menu == 2:
            l_class.get_champion_mastery()
        else:
            break