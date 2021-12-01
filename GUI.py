import riot_function as rf
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.l = rf.League_of_Legend()
        self.setupUI()
        self.show()
    
    def setupUI(self):
        #self.setupUi(self)
        self.setGeometry(600, 200, 1400, 700)
        self.setWindowTitle('LoL 전적 검색기')
        
        self.SummonerName = QLineEdit()
        self.ResetButton = QPushButton('초기화')
        self.SearchButton = QPushButton('전적 검색')
        self.MasteryButton = QPushButton('숙련도 확인')
        self.ResultTable = QTableWidget()
        self.ResultTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ResultTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 표의 내용을 변경할 수 없도록 설정
        self.DetailTable = QTableWidget()

        # 이벤트 추가
        self.SearchButton.clicked.connect(self.display_match)
        self.MasteryButton.clicked.connect(self.display_mastery)
        self.ResultTable.cellClicked.connect(self.display_game_detail)

        # 그래프 캔버스
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)      
        
        # 좌측 레이아웃
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.SummonerName)
        leftLayout.addWidget(self.ResultTable)
        

        # 우측 레이아웃
        rightLayout = QVBoxLayout()
        rightLayout_Button = QHBoxLayout()
        rightLayout_Fig = QVBoxLayout()
        rightLayout_Detail = QVBoxLayout()
        # 우측 - 버튼 레이아웃
        rightLayout_Button.addWidget(self.ResetButton)
        rightLayout_Button.addWidget(self.SearchButton)
        rightLayout_Button.addWidget(self.MasteryButton)
        # 우측 - 게임 상세 정보 레이아웃
        rightLayout_Detail.addWidget(self.DetailTable)
        # 우측 - 승률 원그래프 레이아웃
        rightLayout_Fig.addWidget(self.canvas)
        # 우측 - 레이아웃들 합치기
        rightLayout.addLayout(rightLayout_Button, stretch = 1)
        rightLayout.addLayout(rightLayout_Fig, stretch = 1)
        rightLayout.addLayout(rightLayout_Detail, stretch = 1)

        # 전체 레이아웃
        layout = QHBoxLayout()
        layout.addLayout(leftLayout, stretch = 1)
        layout.addLayout(rightLayout, stretch = 1)
        
        self.setLayout(layout)


    def display_match(self):
        # 이전에 가지고 온 소환사 정보가 있으면 다시 가져오지 않고 기존 소환사 정보 사용
        if self.l.valid_name == 1:
            pass
        else:
            self.l.get_summoner_information(self.SummonerName.text())

        if self.l.valid_name == 0:
            # 새로운 창을 띄워서 에러메세지가 나오도록 변경할 것
            self.SummonerName.clear()
        else:
            self.l.get_match_information(self.l.summoner_info['name'])
            column_headers = ['승패', '챔피언', '게임모드','킬', '데스', '어시', 'KDA', '게임시간']
            temp_list = [0 for i in range(len(column_headers))]

            self.ResultTable.setRowCount(len(self.l.match_list))
            self.ResultTable.setColumnCount(len(column_headers))
            self.ResultTable.setHorizontalHeaderLabels(column_headers)
            row = 0
            
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
                #print(temp_list)
                for k, v in enumerate(temp_list):
                    self.ResultTable.setItem(row, k, QTableWidgetItem(str(v)))
                    if temp_list[0] == '승리': # 표의 색상 처리
                        self.ResultTable.item(row, k).setBackground(QColor(135,206,235))
                    else:
                        self.ResultTable.item(row, k).setBackground(QColor(240,128,128))
                row += 1
            self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
            self.ResultTable.resizeRowsToContents()                                         # 열 높이 조정
            self.display_figure()

    def display_mastery(self):
        if self.l.valid_name == 1:
            pass
        else:
            self.l.get_summoner_information(self.SummonerName.text())

        if self.l.valid_name == 0:
            # 마찬가지로 에러 창을 띄우도록 변경
            self.SummonerName.clear()
        else:
            self.l.get_champion_mastery()
            column_headers = ['챔피언', '숙련도 레벨', '숙련도 점수']

            self.ResultTable.setRowCount(len(self.l.champ_mastery))
            self.ResultTable.setColumnCount(len(column_headers))
            self.ResultTable.setHorizontalHeaderLabels(column_headers)

            for i in range(len(self.l.champ_mastery)):
                self.ResultTable.setItem(i, 0, QTableWidgetItem(self.l.champion_name_key_dict[str(self.l.champ_mastery[i]['championId'])]['ko']))
                self.ResultTable.setItem(i, 1, QTableWidgetItem(str(self.l.champ_mastery[i]['championLevel'])))
                self.ResultTable.setItem(i, 2, QTableWidgetItem(str(self.l.champ_mastery[i]['championPoints'])))
            self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
            self.ResultTable.resizeRowsToContents()                                         # 열 높이 조정
    
    def display_figure(self):
        ax = self.fig.add_subplot()
        ax.pie(x = [self.l.win_rate, 1 - self.l.win_rate], labels = ['Win', 'Lose'], autopct='%.2f%%', colors = ['skyblue','lightcoral'], startangle = 90)
        ax.axis('equal')
        self.canvas.draw()

    def display_game_detail(self): # 숙련도 확인하고 행을 선택하면 그에 해당하는 경기 데이터를 출력하는 버그가 있음
        # game_detail_data = {match_id : {닉네임 : {Champion_Level, champName, kills, deaths, assists, KDA, Dealt_damage, CS, match_result, visionScore, summonerLevel, goldEarned}}}
        column_headers = ['닉네임', '레벨','챔피언','챔레벨','킬', '데스','어시','KDA','피해량','cs','시야점수','골드']
        self.DetailTable.setRowCount(10)
        self.DetailTable.setColumnCount(len(column_headers))
        self.DetailTable.setHorizontalHeaderLabels(column_headers)

        cur_match = self.l.match_list[self.ResultTable.currentRow()]
        temp_list = [0 for i in range(len(column_headers))]
        row = 0
        for i in self.l.game_detail_data[cur_match]:
            temp_list[0] = i
            temp_list[1] = self.l.game_detail_data[cur_match][i]['summonerLevel']
            temp_list[2] = self.l.game_detail_data[cur_match][i]['champName']
            temp_list[3] = self.l.game_detail_data[cur_match][i]['Champion_Level']
            temp_list[4] = self.l.game_detail_data[cur_match][i]['kills']
            temp_list[5] = self.l.game_detail_data[cur_match][i]['deaths']
            temp_list[6] = self.l.game_detail_data[cur_match][i]['assists']
            temp_list[7] = self.l.game_detail_data[cur_match][i]['KDA']
            temp_list[8] = self.l.game_detail_data[cur_match][i]['Dealt_damage']
            temp_list[9] = self.l.game_detail_data[cur_match][i]['CS']
            temp_list[10] = self.l.game_detail_data[cur_match][i]['visionScore']
            temp_list[11] = self.l.game_detail_data[cur_match][i]['goldEarned']

            for k, v in enumerate(temp_list):
                self.DetailTable.setItem(row, k, QTableWidgetItem(str(v)))
                if self.l.game_detail_data[cur_match][i]['match_result']: # 표의 색상 처리
                    self.DetailTable.item(row, k).setBackground(QColor(135,206,235))
                else:
                    self.DetailTable.item(row, k).setBackground(QColor(240,128,128))
            row += 1
        self.DetailTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
        self.DetailTable.resizeRowsToContents()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_W = WindowClass()
    sys.exit(app.exec_())