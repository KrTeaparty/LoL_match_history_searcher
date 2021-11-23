import requests as req
import json
import time
from tqdm import tqdm

class League_of_Legend():
    def __init__(self, s_name):
        self.api_key = '내 api key'
        self.get_summoner_information(s_name)
        self.make_champion_name_key_dict()
        self.page = 0
        self.match_page = {}
        self.match_info_dict = {}
        
    def get_summoner_information(self, name):
        URL = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        print(res.status_code)
        if res.status_code == 200:
            self.valid_name = 1
            resobj = json.loads(res.text)
            self.summoner_info = resobj     
        else:
            self.valid_name = 0
            print('No such summoner')

    def get_champion_mastery(self):
        URL = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + self.summoner_info['id']
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        if res.status_code == 200:
            resobj = json.loads(res.text)
            with open('./riot_data/champion.json', 'r', encoding = 'utf-8') as f:
                champion_js = f.read()
                champion_info = json.loads(champion_js)

            for i in range(3):
                print(champion_info['data'][self.champion_name_key_dict[str(resobj[i]['championId'])]]['name'], end=' ')
                


        
    # 챔피언의 키 값을 딕셔너리의 key로, 챔피언의 영문명을 value로 만들어서 관리한다.
    # Riot API에서는 champion을 다룰 때 챔피언의 이름보다 key로 요청은 주는 경우가 많아서 이렇게 지정한다.
    def make_champion_name_key_dict(self):
        with open('./riot_data/champion.json', 'r', encoding = 'utf-8') as f:
            champion_js = f.read()
            champion_info = json.loads(champion_js)
        self.champion_name_key_dict = {champion_info['data'][k]['key']:champion_info['data'][k]['id'] for k in champion_info['data']}

    def get_match_list(self, start, count=20):
        URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + self.summoner_info['puuid'] + '/ids?start=' + str(start) + '&count=' + str(count)
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        if res.status_code == 200:
            self.match_list = json.loads(res.text)
        else:
            print('No Match Found')

    def get_match_information(self): # memorization을 활용하여 전 페이지로 이동시 추가 요청을 하지 않도록 추가할 것 / 11월 11일의 TIL 확인
        self.get_match_list(self.page)
        for i in tqdm(self.match_list):
            URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i
            res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
            resobj = json.loads(res.text)
            self.match_info_dict[i] = resobj
        
        # 나중에 gui 구성할 때 페이지로 정보 저장해서 memorization 활용
        # self.match_page[self.page] = self.match_info_dict

        cnt = 0
        for i in self.match_list:
            print(f'''
{cnt + 1}번째 판
게임모드 : {self.match_info_dict[i]["info"]["gameMode"]}
게임시간 : {str(round(self.match_info_dict[i]["info"]["gameDuration"] / 60, 2)) + "분"}
게임승패 : {"승리" if self.match_info_dict[i]["info"]["teams"][0]["win"] == True else "패배"}
''')
            cnt += 1

    def next_page(self):
        self.page += 1