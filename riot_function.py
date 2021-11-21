import requests as req
import json

def get_info_by_summoner_name(s_name):
    if not(s_name):
        print('소환사명을 입력해주세요.')
        return 0

    api_key = '내 api 키'

    URL = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + s_name
    res = req.get(URL, headers = {'X-Riot-Token': api_key})
    if res.status_code == 200:
        resobj = json.loads(res.text)
        print('소환사명 : ', resobj["name"])
        print('소환사레벨 : ', resobj['summonerLevel'])
        cmobj = get_champion_mastery(resobj['id'], api_key)
        cnt = 0
        for i in cmobj:
            if cnt == 3:
                break
            print('챔피언 id : ' + str(i['championId']))
            print('챔피언 level : ' + str(i['championLevel']))
            print('챔피언 점수 : ' + str(i['championPoints']))
            cnt += 1
    else:
        print('No summoner')

def get_champion_mastery(s_id, api_key):
    URL = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + s_id
    res = req.get(URL, headers = {'X-Riot-Token': api_key})
    return json.loads(res.text)