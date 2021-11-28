import riot_function as rf
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

Main_Window = uic.loadUiType('Main_window.ui')[0]

class WindowClass(QMainWindow, Main_Window):
    def __init__(self):
        super().__init__()
        self.l = rf.League_of_Legend()
        self.setupUi(self)
        self.SearchButton.clicked.connect(self.display_match)
        self.MasteryButton.clicked.connect(self.display_mastery)
        self.show()
    
    def setupUI(self):
        self.setupUi(self)

    def display_match(self):
        # 이전에 가지고 온 소환사 정보가 있으면 다시 가져오지 않고 기존 소환사 정보 사용
        if self.l.valid_name == 1:
            pass
        else:
            self.l.get_summoner_information(self.SummonerName.text())

        if self.l.valid_name == 0:
            self.ResultTable.setItem(0, 0, QTableWidgetItem("해당하는 소환사가 없습니다."))
            self.SummonerName.clear()
        else:
            self.l.get_match_information(self.l.summoner_info['name'])
            column_headers = ['승패', '챔피언', '게임모드','킬', '데스', '어시', 'KDA', '게임시간']
            self.l.make_match_data()
            temp_list = [0 for i in range(len(column_headers))]

            self.ResultTable.setRowCount(len(self.l.match_list))
            self.ResultTable.setColumnCount(len(column_headers))
            self.ResultTable.setHorizontalHeaderLabels(column_headers)
            row = 0
            # 어차피 이렇게 가져올거면 그냥 애초에 각 게임의 상세 내역을 visualize_match 함수로 만들어 버리는 것은 어떤가?
            # 그러면 쓸모 없이 안보는 게임의 상세 내역도 처리해서 비효율적이지 않을까?
            for i in self.l.match_info_dict:
                temp_list[2] = self.l.match_info_dict[i]['info']['gameMode']
                temp_list[7] = str(self.l.match_info_dict[i]['info']['gameDuration'] // 60) + '분 ' + str(self.l.match_info_dict[i]['info']['gameDuration'] % 60) + '초'
                for j in self.l.game_detail_data[i]:
                    if j.lower() == self.SummonerName.text().lower():
                        temp_list[0] = "승리" if self.l.game_detail_data[i][j]['match_result'] else "패배"
                        temp_list[1] = self.l.game_detail_data[i][j]['champName']
                        temp_list[3] = self.l.game_detail_data[i][j]['kills']
                        temp_list[4] = self.l.game_detail_data[i][j]['deaths']
                        temp_list[5] = self.l.game_detail_data[i][j]['assists']
                        temp_list[6] = self.l.game_detail_data[i][j]['KDA']
                print(temp_list)
                for k, v in enumerate(temp_list):
                    self.ResultTable.setItem(row, k, QTableWidgetItem(str(v)))
                row += 1
            self.ResultTable.resizeColumnsToContents()
            self.ResultTable.resizeRowsToContents()

    def display_mastery(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_W = WindowClass()
    sys.exit(app.exec_())

        




"""
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
"""