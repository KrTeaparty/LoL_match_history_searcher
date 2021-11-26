import requests as req
import json
import time
from tqdm import tqdm
import riot_function as rf


while(1):
    summoner_name = input('정보를 검색할 소환사명 입력 (검색 종료를 원할시 q입력) : ')

    if summoner_name == 'q':
        break

    l_class = rf.League_of_Legend(summoner_name)

    if l_class.valid_name == 0:
        continue

    while(1):
        menu = int(input('''
메뉴를 골라주세요.

1. 전적 검색
2. 챔피언 숙련도 보기
3. 종료
'''))
        if menu == 1:
            l_class.get_match_information()
            l_class.visualize_match()
        elif menu == 2:
            l_class.get_champion_mastery()
        else:
            break