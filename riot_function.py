import requests as req
import json

class League_of_Legend():
    def __init__(self, s_name):
        self.api_key = '내 API 키'
        self.summoner_name = s_name
        self.make_champion_name_key_dict()

        URL = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + self.summoner_name
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        if res.status_code == 200:
            self.valid_name = 1
            resobj = json.loads(res.text)
            self.encrypted_id = resobj['id']
        else:
            self.valid_name = 0

    def get_info_by_summoner_name(self):
        URL = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + self.summoner_name
        res = req.get(URL, headers = {'X-Riot-Token': self.api_key})
        if res.status_code == 200:
            resobj = json.loads(res.text)
            print('소환사레벨 : ', resobj['summonerLevel'])
            self.encrypted_id = resobj['id']      
        else:
            print('No summoner')

    def get_champion_mastery(self):
        URL = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + self.encrypted_id
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

