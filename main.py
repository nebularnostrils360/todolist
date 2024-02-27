"""
ToDoList Application.
Created by Pushkar, Harshit, and Aditya.
"""

import accessories
import sys

class Main(accessories.QMainWindow):
    def __init__(self):
        super().__init__()
        self.loading = accessories.SplashScreen()
        self.loading.load_signal.connect(self.initLogin)
        
    def initLogin(self):
        self.init = accessories.Login()
        self.init.listclicked.connect(self.dbinit)
    
    def dbinit(self):
        self.username = self.init.username
        self.dbconn = accessories.dbhelper(self.username)
        self.init.close()
        self.todolist = accessories.ToDoList(self.username, self.dbconn)

app = accessories.QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())
