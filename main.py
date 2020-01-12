from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TicTacToeLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initInterface()

    def initInterface(self):
        self.layout = QVBoxLayout()
        firstHBox = QHBoxLayout()
        secondHBox = QHBoxLayout()
        thirdHBox = QHBoxLayout()

        xImg = QPixMap("tic-tac-toe-X.png")
        oImg = QPixMap("tic-tac-toe-O.png")

        firstHBox.addWidget(QPushButton("test"))
        
        self.layout.addLayout(firstHBox)



class TicTacToe(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setCentralWidget(TicTacToeLayout())
        # print(QFile.exists('refresh.png'))
        self.setWindowIcon(QIcon('tic-tac-toe-logo.png'))
        self.setWindowTitle('Tic Tac Toe Game')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(627, 470))
        self.setMaximumSize(QSize(627, 470))
        menubar = self.menuBar()
        menubar.addMenu('File')
        menubar.addMenu('Settings')
        toolbar = self.addToolBar('test')
        icon1 = QAction(QIcon("tic-tac-toe-X.png"), "icon1", self)
        icon2 = QAction(QIcon("tic-tac-toe-O.png"), "icon2", self)
        toolbar.addAction(icon1)
        toolbar.addAction(icon2)
    
        self.show()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = TicTacToe()
    sys.exit(app.exec())
