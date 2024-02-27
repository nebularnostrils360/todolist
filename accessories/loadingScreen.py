import sys
import time
from PyQt5.QtWidgets import QApplication, QPushButton, QProgressBar, QLabel, QFrame, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

class SplashScreen(QWidget):
    load_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('To-do List')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.counter = 0
        self.n = 300 
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loading)
        self.timer.start(5)
        
        self.initUI()
        self.show()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.frame = QFrame(self)
        layout.addWidget(self.frame)
        
        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)
        self.labelTitle.setText("To-do List")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        
        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Working on task #1</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)
        
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)
        
        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('Loading')
        
    def loading(self):
        self.progressBar.setValue(self.counter)
        
        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Working on task #2</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Working on task #3</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.load_signal.emit()
            self.close()
        
        self.counter += 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QLabel#LabelTitle {
            color: white;
            font-size: 30px;
        }
        
        QLabel#LabelDesc {
            color: white;
            font-size: 20px;
        }
        
        QLabel#LabelLoading {
            color: white;
            font-size: 20px;
        }
    ''')
    
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
    
