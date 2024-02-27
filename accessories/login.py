"""
Login window module for the todolist.
"""

import sys
import pickle
import os
from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QLineEdit, QLabel, QVBoxLayout, QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class styles:
    red_button = """background-color: #ee0000;
                    border-radius: 5%; 
                    border: 2px solid #cc0000;
                    padding: 1px;"""
    normal_button = """background-color: #e9e9e9;
                        border-radius: 5%;
                        border: 2px solid #c9c9c9;
                        padding: 1px;"""
    text_entry = """background-color: #e9e9e9;
                    border-radius: 5%; 
                    border: 2px solid #c9c9c9;"""
    bg_color = "background-color: #9BD2F1;"

    list_widget = """background-color: #e9e9e9;
                    border-radius: 5%;"""

class Login(QWidget):
    """
    Create the login Window for the ToDolist app.
    """

    listclicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        self.loginwindow = QWidget()
        self.loginwindow.setWindowTitle("Login")

        self.adduserwindow = QWidget()
        self.adduserwindow.setWindowTitle("Add a New User")
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.loginwindow)
        self.stack.addWidget(self.adduserwindow)

        self.stack.setGeometry(400, 200, 400, 230)
        self.stack.setStyleSheet(styles.bg_color)

        self.initializeLogin()
        self.initializeAddUser()
        
        self.stack.show()
    
    def initializeLogin(self):
        # layout for the login screen
        login_layout = QVBoxLayout()

        arial = lambda x: QFont("Arial", x)
        
        # welcome label
        label = QLabel("Welcome")
        label.setFont(arial(22))

        # Check for usernames in databases        
        listdir = os.listdir("./databases")
        self.loginwindow.names = list((name.split(".")[0] for name in listdir))
        # log stores user passes
        if "log" in self.loginwindow.names:
            self.loginwindow.names.remove("log")
        
        # list for user names that is the main content
        # for the window
        self.loginwindow.list_names = QListWidget()
        self.loginwindow.list_names.setStyleSheet(styles.list_widget)

        self.loginwindow.list_names.setAlternatingRowColors(True)
        for name in self.loginwindow.names:
            list_item = QListWidgetItem()
            list_item.setText(name)
            self.loginwindow.list_names.addItem(list_item)

        self.loginwindow.list_names.activated.connect(self.userpass)

        # setting up buttons
        add_button = QPushButton("Add new user")
        add_button.setStyleSheet(styles.normal_button)
        add_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        close_button = QPushButton("Close")
        close_button.setStyleSheet(styles.red_button)
        close_button.clicked.connect(self.stack.close)

        butt_layout = QHBoxLayout()
        butt_layout.addWidget(add_button)
        butt_layout.addWidget(close_button)

        login_layout.addWidget(label)
        login_layout.addWidget(self.loginwindow.list_names)
        login_layout.addStretch()
        login_layout.addLayout(butt_layout)
        self.loginwindow.setLayout(login_layout)

    def initializeAddUser(self):
        # User form
        adduser_layout = QVBoxLayout()
        name_label = QLabel("Enter the name of the user.")
        self.adduserwindow.name = QLineEdit()
        self.adduserwindow.name.setStyleSheet(styles.text_entry)

        pass_label = QLabel("Enter a new password for the user.")
        self.adduserwindow.password = QLineEdit()
        self.adduserwindow.password.setEchoMode(QLineEdit.Password)
        self.adduserwindow.password.setStyleSheet(styles.text_entry)

        # buttons
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet(styles.normal_button)
        submit_button.clicked.connect(self.createNewUser)
        close_button = QPushButton("Back")
        close_button.setStyleSheet(styles.red_button)
        close_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        butt_layout = QHBoxLayout()
        butt_layout.addWidget(submit_button)
        butt_layout.addWidget(close_button)

        # set up the window
        adduser_layout.addStretch(1)
        adduser_layout.addWidget(name_label)
        adduser_layout.addWidget(self.adduserwindow.name)
        adduser_layout.addWidget(pass_label)
        adduser_layout.addWidget(self.adduserwindow.password)
        adduser_layout.addStretch(2)
        adduser_layout.addLayout(butt_layout)
        self.adduserwindow.setLayout(adduser_layout)
    
    def createNewUser(self):
        username = self.adduserwindow.name.text()
        password = self.adduserwindow.password.text()
        response = QMessageBox()
        if username in self.loginwindow.names:
            response.critical(self.stack, "Error: User Already exists", f"User {username} already exists.", QMessageBox.Ok)
        else:
            with open(f"./databases/log", "ab+") as binfil:
                pickle.dump(f"{username}:{password}", binfil)

            file = open(f"./databases/{username}.db", "w")
            file.close()
            new_item = QListWidgetItem(username)
            self.loginwindow.list_names.addItem(new_item)
            self.stack.setCurrentIndex(0)
            self.loginwindow.repaint()
    
    def userpass(self, username):
        inputDialog = QInputDialog()
        password, ok = inputDialog.getText(self.loginwindow, "Password", "Enter your password.", QLineEdit.Password)
        self.username = username.data().split(":")[0]
        
        response = QMessageBox()

        binfile = open("./databases/log", "rb+")
        while True:
            try:
                userinfo = pickle.load(binfile)
            except EOFError:
                break

            if username.data() == userinfo.split(":")[0]:
                self.userinfo = userinfo
                break

        if ok:
            if password == self.userinfo.split(":")[1]:
                response.information(self.loginwindow, "Success", "Authentication Successful", 
                                    QMessageBox.Ok)
                self.listclicked.emit()
            else:
                response.critical(self.loginwindow, "Wrong Password", 
                                "The password you entered was wrong", QMessageBox.Ok)
                self.userpass(username)
    
    def close(self):
        self.stack.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    sys.exit(app.exec_())
