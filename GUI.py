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
        self.Prev_match = QTableWidget()
        self.Next_match = QTableWidget()
        self.setupUI()
        self.show()
    
    def setupUI(self):
        self.setGeometry(600, 200, 1400, 700)
        self.setWindowTitle('LoL 전적 검색기')
        
        # 좌측 위젯
        self.SummonerName = QLineEdit() # 소환사명 입력창
        self.SearchButton = QPushButton('전적 검색') # 검색 버튼
        self.PreviousButton = QPushButton('이전 페이지') # 이전 페이지 버튼
        self.NextButton = QPushButton('다음 페이지') # 다음 페이지 버튼
        self.ResultTable = QTableWidget() # 전적 검색 결과 출력용 테이블 위젯
        self.ResultTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ResultTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 표의 내용을 변경할 수 없도록 설정
        
        # 우측 위젯
        self.DetailTable = QTableWidget() # 게임 상세 정보 출력용 테이블 위젯
        self.DetailTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.DetailTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.win_rate_table = QTableWidget() # 같이 플레이한 소환사들과의 승률 출력용 테이블 위젯
        self.win_rate_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.win_rate_table.setEditTriggers(QAbstractItemView.NoEditTriggers)



        # 이벤트 추가
        self.SearchButton.clicked.connect(self.display_match)
        self.PreviousButton.clicked.connect(self.display_previous_match)
        self.NextButton.clicked.connect(self.display_next_match)
        self.ResultTable.cellClicked.connect(self.display_game_detail)

        # 그래프 캔버스 - 우측
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig) # 원 그래프 출력용 캔버스
        
        # 좌측 레이아웃
        leftLayout = QVBoxLayout()
        # 좌측 - 입력 및 검색 버튼
        leftLayout_Input = QHBoxLayout()
        leftLayout_Input.addWidget(self.SummonerName)
        leftLayout_Input.addWidget(self.SearchButton)
        # 좌측 - 결과 테이블
        leftLayout_Table = QVBoxLayout()
        leftLayout_Table.addWidget(self.ResultTable)
        # 좌측 - 이전 및 다음 페이지 버튼
        leftLayout_Button = QHBoxLayout()
        leftLayout_Button.addWidget(self.PreviousButton)
        leftLayout_Button.addWidget(self.NextButton)
        # 좌측 - 레이아웃 합치기
        leftLayout.addLayout(leftLayout_Input, stretch = 1)
        leftLayout.addLayout(leftLayout_Table, stretch = 1)
        leftLayout.addLayout(leftLayout_Button, stretch = 1)

        # 우측 레이아웃
        rightLayout = QVBoxLayout()
        
        # 우측 - 게임 상세 정보 레이아웃
        rightLayout_Detail = QVBoxLayout()
        rightLayout_Detail.addWidget(self.DetailTable)
        # 우측 - 승률 원그래프 레이아웃
        rightLayout_Fig = QHBoxLayout()
        rightLayout_Fig.addWidget(self.canvas, stretch = 1)
        rightLayout_Fig.addWidget(self.win_rate_table, stretch = 1)
        # 우측 - 레이아웃들 합치기
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

        # 해당하는 소환사가 없다면 입력창을 비운다.
        if self.l.valid_name == 0:
            self.SummonerName.clear()
        else:
            self.l.get_match_information()
            column_headers = ['승패', '챔피언', '게임모드','킬', '데스', '어시', 'KDA', '게임시간']
            temp_list = [0 for i in range(len(column_headers))]

            # 테이블 위젯을 사용하기 위해 행, 열 갯수를 설정한다.
            self.ResultTable.setRowCount(len(self.l.match_list))
            self.ResultTable.setColumnCount(len(column_headers))
            # Column 명을 지정한다.
            self.ResultTable.setHorizontalHeaderLabels(column_headers)
            row = 0
            
            for i in self.l.match_info_dict:
                temp_list[2] = self.l.match_info_dict[i]['info']['gameMode']
                temp_list[7] = str(self.l.match_info_dict[i]['info']['gameDuration'] // 60) + '분 ' + str(self.l.match_info_dict[i]['info']['gameDuration'] % 60) + '초'
                temp_list[0] = "승리" if self.l.game_detail_data[i][self.l.summoner_info['name']]['match_result'] else "패배"
                temp_list[1] = self.l.game_detail_data[i][self.l.summoner_info['name']]['champName']
                temp_list[3] = self.l.game_detail_data[i][self.l.summoner_info['name']]['kills']
                temp_list[4] = self.l.game_detail_data[i][self.l.summoner_info['name']]['deaths']
                temp_list[5] = self.l.game_detail_data[i][self.l.summoner_info['name']]['assists']
                temp_list[6] = self.l.game_detail_data[i][self.l.summoner_info['name']]['KDA']
                for k, v in enumerate(temp_list):
                    self.ResultTable.setItem(row, k, QTableWidgetItem(str(v)))
                    if temp_list[0] == '승리': # 셀의 색상 처리
                        self.ResultTable.item(row, k).setBackground(QColor(135,206,235))
                    else:
                        self.ResultTable.item(row, k).setBackground(QColor(240,128,128))
                row += 1
            self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
            self.ResultTable.resizeRowsToContents()                                         # 열 높이 조정
            self.display_figure()
            self.display_win_rate_teammate()

    def display_figure(self):
        self.fig.clear()
        ax = self.fig.add_subplot()
        ax.pie(x = [self.l.win_rate, 1 - self.l.win_rate], labels = ['Win', 'Lose'], autopct='%.2f%%', colors = ['skyblue','lightcoral'], startangle = 90)
        ax.axis('equal')
        self.canvas.draw()

    def display_game_detail(self):
        # game_detail_data = {match_id : {닉네임 : {Champion_Level, champName, kills, deaths, assists, KDA, Dealt_damage, CS, match_result, visionScore, summonerLevel, goldEarned}}}
        column_headers = ['닉네임', '레벨','챔피언','챔레벨','킬', '데스','어시','KDA','피해량','cs','시야점수','골드']
        self.DetailTable.setRowCount(10)
        self.DetailTable.setColumnCount(len(column_headers))
        self.DetailTable.setHorizontalHeaderLabels(column_headers)

        cur_match = self.l.match_list[self.ResultTable.currentRow()]
        temp_list = [0 for i in range(len(column_headers))]
        row = 0
        best_player = [0, 0]
        worst_player = [0, 1000]
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
            
            if self.l.game_detail_data[cur_match][i]['match_result']:
                if temp_list[7] == 'Perfect':
                    best_player[0] = row
                    best_player[1] = 100
                elif best_player[1] <= temp_list[7]:
                    best_player[0] = row
                    best_player[1] = temp_list[7]
            else:
                if worst_player[1] >= temp_list[7]:
                    worst_player[0] = row
                    worst_player[1] = temp_list[7]
            row += 1

        self.DetailTable.item(best_player[0], 0).setFont(QFont('Gulim', 9, QFont.Bold))
        self.DetailTable.item(worst_player[0], 0).setFont(QFont('Gulim', 9, QFont.Bold, italic = True))
        self.DetailTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
        self.DetailTable.resizeRowsToContents()
    
    def display_previous_match(self):
        if self.l.page == 0:
            return 0
        self.l.page -= 20
        self.display_match()
    
    def display_next_match(self):
        if self.l.page == 100:
            return 0
        self.l.page += 20
        self.display_match()

    def display_win_rate_teammate(self):
        column_headers = ['닉네임', '총 판수', '이긴 판수', '승률']
        player_count = 0
        player_name_list = []
        for k, v in self.l.play_with.items():
            if v['count'] >= 2:
                player_count += 1
                player_name_list.append(k)

        self.win_rate_table.setRowCount(player_count)
        self.win_rate_table.setColumnCount(len(column_headers))
        self.win_rate_table.setHorizontalHeaderLabels(column_headers)

        temp_list = [0 for i in range(len(column_headers))]
        row = 0
        for i in player_name_list:
            temp_list[0] = i
            temp_list[1] = self.l.play_with[i]['count']
            temp_list[2] = self.l.play_with[i]['win']
            temp_list[3] = round(self.l.play_with[i]['win'] / self.l.play_with[i]['count'] * 100, 2) 

            for k, v in enumerate(temp_list):
                # float형도 그냥 쓸 수 있도록 하는 부분임
                item = QTableWidgetItem(v)
                item.setData(Qt.DisplayRole, v)
                self.win_rate_table.setItem(row, k, item)
            row += 1
        self.win_rate_table.sortItems(1, order = Qt.DescendingOrder)
        self.win_rate_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.win_rate_table.resizeRowsToContents()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_W = WindowClass()
    sys.exit(app.exec_())