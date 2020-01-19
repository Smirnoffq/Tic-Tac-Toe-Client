from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LobbyWidget(QWidget):
    def __init__(self, parent=None):
        super(LobbyWidget, self).__init__(parent)
        self.parent = parent

        spacerItem = QSpacerItem(
            40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gameNameEditLine = QLineEdit()
        self.gameNameEditLine.setObjectName("gameNameEditLine")

        self.createGameButton = QPushButton()
        self.createGameButton.setObjectName("createGameButton")

        self.joinGameButton = QPushButton()
        self.joinGameButton.setObjectName("pushButton_2")

        self.gameNameLabel = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gameNameLabel.sizePolicy().hasHeightForWidth())
        self.gameNameLabel.setSizePolicy(sizePolicy)
        self.gameNameLabel.setMinimumSize(QSize(1, 0))
        self.gameNameLabel.setMaximumSize(QSize(16777215, 100))
        self.gameNameLabel.setObjectName("gameNameLabel")

        self.playersLabel = QLabel()
        self.playersLabel.setObjectName("playersLabel")

        self.gamesLabel = QLabel()
        self.gamesLabel.setObjectName("gamesLabel")

        self.errorLabel = QLabel()
        self.errorLabel.setObjectName("errorLabel")

        self.playersTable = QTableWidget()
        self.playersTable.setColumnCount(3)
        self.playersTable.setHorizontalHeaderLabels(
            "Name;Status;MMR".split(";"))
        self.playersTable.setEditTriggers(
            QTreeView.NoEditTriggers)  # turn off editable
        self.playersTableHeader = self.playersTable.horizontalHeader()
        self.playersTableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        self.playersTableHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        self.playersTableHeader.setSectionResizeMode(2, QHeaderView.Stretch)
        self.playersTable.setObjectName("playersTable")

        self.gamesTable = QTableWidget()
        self.gamesTable.setColumnCount(2)
        self.gamesTable.setHorizontalHeaderLabels("Name;Players".split(";"))
        self.gamesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gamesTable.setEditTriggers(
            QTreeView.NoEditTriggers)  # turn off editable
        self.gamesTableHeader = self.gamesTable.horizontalHeader()
        self.gamesTableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        self.gamesTableHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        self.gamesTable.setObjectName("gamesTable")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.playersLabel, 0, Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.playersTable)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.addWidget(self.gamesLabel, 0, Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.gamesTable)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.gameNameLabel)
        self.horizontalLayout.addWidget(self.gameNameEditLine)
        self.horizontalLayout.addWidget(self.createGameButton)
        self.horizontalLayout.addWidget(self.joinGameButton)
        self.horizontalLayout.addItem(spacerItem1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.errorLabel, 0, Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi()
        self.setLayout(self.gridLayout)

    def retranslateUi(self):
        self.gameNameLabel.setText("Nazwa gry:")
        self.createGameButton.setText("Stworz gre")
        self.joinGameButton.setText("Dolacz do gry")
        self.playersLabel.setText("Gracze")
        self.gamesLabel.setText("Gry")
        self.errorLabel.setText("")
