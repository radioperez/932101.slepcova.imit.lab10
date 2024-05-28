import sys
import random
import numpy as np
from numpy.random import default_rng
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
)
import time

class Team:
    name: int = None
    score: int = None
    def __init__(self, name):
        self.name = name
        self.score = None

def compete(teamA: Team, teamB: Team) -> Team:
    teamA.score = default_rng().poisson(2,1)[0]
    teamB.score = default_rng().poisson(2,1)[0]
    
    print(f'Команда {teamA.name} vs Команда {teamB.name}')
    print(f'{teamA.score} : {teamB.score}')
    if teamA.score == teamB.score: return compete(teamA, teamB)
    else: return teamA if teamA.score > teamB.score else teamB

def tournament(teams: list[Team]) -> Team:
    while len(teams) > 1:
        sideA = teams[::2]
        sideB = teams[1::2]
        lineup = list(zip(sideA, sideB))
        winners = []
        for teamA, teamB in lineup:
            winners.append(compete(teamA, teamB))
        teams = winners
    print(f'Победитель: Команда {teams[0].name}')
    return teams[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Чемпионат")
        self.resize(QSize(800,300))

        l = QGridLayout()
        self.starters: list[QLineEdit] = [QLineEdit("S0"), QLineEdit("S1"), QLineEdit("S2"), QLineEdit("S3"), QLineEdit("S4"), QLineEdit("S5"), QLineEdit("S6"), QLineEdit("S7")]
        l.addWidget(self.starters[0], 0, 0)
        l.addWidget(self.starters[1], 1, 0)
        l.addWidget(self.starters[2], 2, 0)
        l.addWidget(self.starters[3], 3, 0)

        l.addWidget(self.starters[4], 0, 6)
        l.addWidget(self.starters[5], 1, 6)
        l.addWidget(self.starters[6], 2, 6)
        l.addWidget(self.starters[7], 3, 6) 

        self.halffinal: list[QLineEdit] = [QLineEdit("H0"), QLineEdit("H1"), QLineEdit("H2"), QLineEdit("H3")]
        l.addWidget(self.halffinal[0], 0, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter)
        l.addWidget(self.halffinal[1], 2, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter)

        l.addWidget(self.halffinal[2], 0, 5, 2, 1, Qt.AlignmentFlag.AlignHCenter)
        l.addWidget(self.halffinal[3], 2, 5, 2, 1, Qt.AlignmentFlag.AlignHCenter)

        self.final: list[QLineEdit] = [QLineEdit("F0"), QLineEdit("F1")]
        l.addWidget(self.final[0], 0, 2, 4, 1, Qt.AlignmentFlag.AlignHCenter)
        l.addWidget(self.final[1], 0, 4, 4, 1, Qt.AlignmentFlag.AlignHCenter)

        self.winner = QLabel("W")
        l.addWidget(self.winner, 0, 3, 4, 1, Qt.AlignmentFlag.AlignHCenter)  

        start_button = QPushButton("СТАРТ")
        start_button.clicked.connect(self.tournament)

        layout = QVBoxLayout()
        layout.addLayout(l)
        layout.addWidget(start_button)

        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)
    def tournament(self):
        teams: list[Team] = [Team('ABC'), Team('DEF'), Team('GHI'), Team('JKL'), Team('MNO'), Team('PQR'), Team('STU'), Team('VWX')]
        for index, team in enumerate(teams):
            self.starters[index].setText(team.name)
        
        halffinalists = []
        sideA = teams[::2]
        sideB = teams[1::2]
        lineup = list(zip(sideA, sideB))
        for index, (teamA, teamB) in enumerate(lineup):
            team = compete(teamA, teamB)
            self.starters[index*2].setText(f'{teamA.name} | {teamA.score}')
            self.starters[index*2+1].setText(f'{teamB.name} | {teamB.score}')
            self.halffinal[index].setText(team.name)
            halffinalists.append(team)

        finalists = []
        sideA = halffinalists[::2]
        sideB = halffinalists[1::2]
        lineup = list(zip(sideA, sideB))
        for index, (teamA, teamB) in enumerate(lineup):
            team = compete(teamA, teamB)
            self.halffinal[index*2].setText(f'{teamA.name} | {teamA.score}')
            self.halffinal[index*2+1].setText(f'{teamB.name} | {teamB.score}')
            self.final[index].setText(team.name)
            finalists.append(team)
        
        win = compete(finalists[0], finalists[1])
        self.final[0].setText(f'{finalists[0].name} | {finalists[0].score}')
        self.final[1].setText(f'{finalists[1].name} | {finalists[1].score}')
        self.winner.setText(win.name)

        


random.seed()

app = QApplication(sys.argv)
app.setStyleSheet("QLineEdit {font-size: 20px; text-align: center;} QLabel {font-size: 48px;}")
main = MainWindow()
main.show()
app.exec()