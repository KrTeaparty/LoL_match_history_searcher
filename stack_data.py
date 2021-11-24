import riot_function as rf
import requests as req
import json
from tqdm import tqdm
import time

class save_lol_data(rf.League_of_Legend):
    def __init__(self):
        self.api_key = '내 api key'
        self.page = 0
        self.match_info_dict = {}

    def get_match_information(self): # 나중에 GUI로 만들 때는 League_of_Legend class의 함수에서 출력 부분을 없애서 사용할 것이므로 그때는 삭제 가능
        self.get_match_list(self.page)
        for i in tqdm(self.match_list):
            URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i
            res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
            if res.status_code == 429:
                time.sleep(120)
                URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i
                res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
            resobj = json.loads(res.text)
            self.match_info_dict[i] = resobj

    def get_challenger_matches(self):
        URL = 'https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-gueue/RANKED_SOLO_5x5'
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        challenger_info = json.loads(res.text)
        print(challenger_info)
        challenger_name = [i['summonerName'] for i in challenger_info['entries']]
        for i in tqdm(challenger_name):
            self.get_summoner_information(i)
            self.get_match_information()
        print(len(self.match_info_dict))






if __name__ == '__main__':
    sld = save_lol_data()
    sld.get_challenger_matches()
    