import requests as req
import json
import time
from tqdm import tqdm
import pandas as pd

class League_of_Legend():
    def __init__(self, s_name):
        self.api_key = '내 api key'
        self.get_summoner_information(s_name)
        self.make_champion_name_key_dict()
        self.page = 0
        self.match_page = {}
        self.match_info_dict = {}

    def req_api(self, URL):
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})

        if res.status_code != 200:
            if res.status_code == 429:
                print(res.status_code)
                time.sleep(150)
                return res.status_code
            else:
                print(res.status_code)
                time.sleep(1)
                return res.status_code
        else:
            time.sleep(0.6)
            return res.json()
        
    def get_summoner_information(self, name):
        URL = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
        res = self.req_api(URL)
        if type(res) != int:
            self.valid_name = 1
            self.summoner_info = res
        else:
            self.valid_name = 0
            print('No such summoner')

    def get_champion_mastery(self):
        URL = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + self.summoner_info['id']
        res = self.req_api(URL)
        if type(res) != int:
            for i in range(3):
                print(self.champion_data['data'][self.champion_name_key_dict[str(res[i]['championId'])]]['name'], end=' ')
                


        
    # 챔피언의 키 값을 딕셔너리의 key로, 챔피언의 영문명을 value로 만들어서 관리한다.
    # Riot API에서는 champion을 다룰 때 챔피언의 이름보다 key로 요청은 주는 경우가 많아서 이렇게 지정한다.
    def make_champion_name_key_dict(self):
        self.champion_data = req.get('http://ddragon.leagueoflegends.com/cdn/11.23.1/data/ko_KR/champion.json').json()
        self.champion_name_key_dict = {self.champion_data['data'][k]['key']:self.champion_data['data'][k]['id'] for k in self.champion_data['data']}

    def get_match_list(self, start, count=1):
        URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + self.summoner_info['puuid'] + '/ids?start=' + str(start) + '&count=' + str(count)
        res = self.req_api(URL)
        if type(res) != int:
            self.match_list = res
        else:
            print('No Match Found')

    def get_match_information(self): # memorization을 활용하여 전 페이지로 이동시 추가 요청을 하지 않도록 추가할 것 / 11월 11일의 TIL 확인
        self.get_match_list(self.page)
        for i in tqdm(self.match_list):
            URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i
            res = self.req_api(URL)
            self.match_info_dict[i] = res
        
        # 나중에 gui 구성할 때 페이지로 정보 저장해서 memorization 활용
        # self.match_page[self.page] = self.match_info_dict

#         cnt = 0
#         for i in self.match_list:
#             print(f'''
# {cnt + 1}번째 판
# 게임모드 : {self.match_info_dict[i]["info"]["gameMode"]}
# 게임시간 : {str(round(self.match_info_dict[i]["info"]["gameDuration"] / 60, 2)) + "분"}
# 게임승패 : {"승리" if self.match_info_dict[i]["info"]["teams"][0]["win"] == True else "패배"}
# ''')
#             cnt += 1
    def visualize_match(self):
        for i in self.match_info_dict:
            game_details = []
            match_result = self.match_info_dict[i]['info']['teams'][0]['win']
            print("승리" if match_result else "패배")
            for j in self.match_info_dict[i]['info']['participants']:
                person_details = {}
                person_details['Name'] = j['summonerName']
                person_details['Champion_Level'] = j['champLevel']
                person_details['champName'] = j['championName']
                person_details['kills'] = j['kills']
                person_details['deaths'] = j['deaths']
                person_details['Assists'] = j['assists']
                person_details['KDA'] = round((j['kills'] + j['assists']) / j['deaths'], 2)
                person_details['Dealt_damage'] = j['totalDamageDealtToChampions']
                person_details['CS'] = j['totalMinionsKilled']
                game_details.append(person_details)
            df = pd.DataFrame(game_details)
            print(df)
