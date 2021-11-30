import riot_function as rf
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
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
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle('LoL 전적 검색기')
        
        self.SummonerName = QLineEdit()
        self.ResetButton = QPushButton('초기화')
        self.SearchButton = QPushButton('전적 검색')
        self.MasteryButton = QPushButton('숙련도 확인')
        self.ResultTable = QTableWidget()
        self.StatusLabel = QLabel()

        # 이벤트 추가
        self.SearchButton.clicked.connect(self.display_match)
        self.MasteryButton.clicked.connect(self.display_mastery)

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
        rightLayout_Button.addWidget(self.ResetButton)
        rightLayout_Button.addWidget(self.SearchButton)
        rightLayout_Button.addWidget(self.MasteryButton)
        rightLayout_Fig.addWidget(self.StatusLabel)
        rightLayout_Fig.addWidget(self.canvas)
        rightLayout.addLayout(rightLayout_Button)
        rightLayout.addLayout(rightLayout_Fig)

        # 전체 레이아웃
        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        
        self.setLayout(layout)


    def display_match(self):
        # 이전에 가지고 온 소환사 정보가 있으면 다시 가져오지 않고 기존 소환사 정보 사용
        if self.l.valid_name == 1:
            pass
        else:
            self.l.get_summoner_information(self.SummonerName.text())

        if self.l.valid_name == 0:
            self.StatusLabel.setText('해당하는 소환사가 없습니다.')
            self.SummonerName.clear()
        else:
            self.StatusLabel.setText(self.l.summoner_info['name'] + '님의 전적을 검색합니다.') # 이 부분이 작동하는지 모르겠음
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
                row += 1
            self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # column 너비 조정
            self.ResultTable.resizeRowsToContents()                                         # 열 높이 조정
            self.display_figure()
            self.StatusLabel.setText(self.l.summoner_info['name'] + '님의 전적 검색이 완료되었습니다.')

    def display_mastery(self):
        if self.l.valid_name == 1:
            pass
        else:
            self.l.get_summoner_information(self.SummonerName.text())

        if self.l.valid_name == 0:
            self.StatusLabel.setText('해당하는 소환사가 없습니다.')
            self.SummonerName.clear()
        else:
            self.StatusLabel.setText(self.l.summoner_info['name'] + '님의 숙련도를 가져오고 있습니다.')
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
            self.StatusLabel.setText(self.l.summoner_info['name'] + '님의 숙련도를 가져왔습니다.')
    
    def display_figure(self):
        ax = self.fig.add_subplot()
        ax.pie(x = [self.l.win_rate, 1 - self.l.win_rate], labels = ['Win', 'Lose'], autopct='%.2f%%', colors = ['skyblue','lightcoral'], startangle = 90)
        ax.axis('equal')
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_W = WindowClass()
    sys.exit(app.exec_())