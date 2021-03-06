import requests as req
import json
import time
from tqdm import tqdm
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class League_of_Legend():
    def __init__(self):
        self.api_key = '내 API Key'
        self.valid_name = 0
        self.make_champion_name_key_dict()
        self.page = 0
        self.match_info_dict = {}

    # URL을 받으면 해당 URL로 api 요청을 한다.
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

    def get_champion_mastery(self):
        URL = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + self.summoner_info['id']
        res = self.req_api(URL)
        if type(res) != int:
            self.champ_mastery = res
                

    # 챔피언의 키 값을 딕셔너리의 key로, 챔피언의 영문명을 value로 만들어서 관리한다.
    # Riot API에서는 champion을 다룰 때 챔피언의 이름보다 key로 요청은 주는 경우가 많아서 이렇게 지정한다.
    def make_champion_name_key_dict(self):
        self.champion_data = req.get('http://ddragon.leagueoflegends.com/cdn/11.23.1/data/ko_KR/champion.json').json()
        self.champion_name_key_dict = {self.champion_data['data'][k]['key']:{'en':self.champion_data['data'][k]['id'], 'ko':self.champion_data['data'][k]['name']} for k in self.champion_data['data']}

    def get_match_list(self, start, count):
        URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + self.summoner_info['puuid'] + '/ids?start=' + str(start) + '&count=' + str(count)
        res = self.req_api(URL)
        if type(res) != int:
            self.match_list = res
        else:
            print('No Match Found')

    def get_match_information(self):
        self.get_match_list(self.page, 20)
        self.match_info_dict = {}
        for i in self.match_list:
            URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i
            res = self.req_api(URL)
            self.match_info_dict[i] = res
        self.make_match_data()
        self.calculate_win_rate()
        self.who_played_with()
        

    # 데이터 전처리 함수로 조금 더 개선하자
    # 데이터 전처리라고 하지만 정말 이게 필요할까?
    # 한 종류의 데이터를 너무 쪼개놔서 복잡하게 된 것 같은 느낌이 든다.
    # 현재 코드를 보니까 안쓰는게 더 나을지도 모른다. 개선할 방법을 찾아보자.
    def make_match_data(self):
        self.game_detail_data = {}
        for i in self.match_info_dict:
            game_details = {}
            for j in self.match_info_dict[i]['info']['participants']:
                person_details = {}
                person_details['Champion_Level'] = j['champLevel']
                person_details['champName'] = self.champion_name_key_dict[str(j['championId'])]['ko']
                person_details['kills'] = j['kills']
                person_details['deaths'] = j['deaths']
                person_details['assists'] = j['assists']
                if j['deaths'] == 0:
                    person_details['KDA'] = 'Perfect'
                else:
                    person_details['KDA'] = round((j['kills'] + j['assists']) / j['deaths'], 2)
                person_details['Dealt_damage'] = j['totalDamageDealtToChampions']
                person_details['CS'] = j['totalMinionsKilled']
                person_details['match_result'] =  j['win']
                person_details['visionScore'] = j['visionScore']
                person_details['summonerLevel'] = j['summonerLevel']
                person_details['goldEarned'] = j['goldEarned']

                game_details[j['summonerName']] = person_details
            self.game_detail_data[i] = game_details

    def calculate_win_rate(self):
        total_win = 0
        for i in self.match_info_dict:
            if self.game_detail_data[i][self.summoner_info['name']]['match_result']:
                total_win += 1
        self.win_rate = total_win / len(self.match_list)
    
    def who_played_with(self):
        self.play_with = {}
        for i in self.match_info_dict:
            for v in self.game_detail_data[i]:
                if (self.game_detail_data[i][v]['match_result'] == self.game_detail_data[i][self.summoner_info['name']]['match_result']) and (v != self.summoner_info['name']):
                    if v in self.play_with:
                        self.play_with[v]['count'] += 1
                    else:
                        self.play_with[v] = {}
                        self.play_with[v]['count'] = 1
                        self.play_with[v]['win'] = 0

                    if self.game_detail_data[i][v]['match_result']:
                        self.play_with[v]['win'] += 1


