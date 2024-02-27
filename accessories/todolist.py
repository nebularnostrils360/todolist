"""
Main window module for todolist.
"""

import sys
import datetime
# import dbclass

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QSpinBox, QLineEdit, QTextEdit, QComboBox, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
    user_label = "border: 1px solid black; font-weight: bold;"
    default_grey = "background-color: #e9e9e9;"

class ToDoList(QWidget):
    count = 0
    def __init__(self, username, dbconnection):
        self.dbconn = dbconnection
        self.username = username
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        self.mainwindow = QWidget()
        self.mainwindow.setWindowTitle(f"{self.username}'s To-Do list")

        self.taskcreationwindow = QWidget()
        self.taskcreationwindow.setWindowTitle("Create a new task")

        self.displaywindow = QWidget()
        self.displaywindow.setWindowTitle("Task Details")

        self.stack = QStackedWidget()
        self.stack.addWidget(self.mainwindow)
        self.stack.addWidget(self.taskcreationwindow)
        self.stack.addWidget(self.displaywindow)

        self.stack.setGeometry(400, 200, 400, 400)
        self.stack.setStyleSheet(styles.bg_color)
    
        self.mainwindowSetUp()
        self.taskcreationwindowSetUp()
        self.displaywindowSetUp()

        self.stack.show()
    
    def mainwindowSetUp(self):
        main_layout = QVBoxLayout()
        username_label = QLabel(f"{self.username.upper()}")
        username_label.setStyleSheet(styles.user_label)
        username_label.setAlignment(Qt.AlignCenter)
        username_label.setMaximumHeight(20)
        arial = lambda x: QFont("Arial", x)
        title_label = QLabel("Your to do list.")
        title_label.setFont(arial(24))

        self.mainwindow.create_button = QPushButton("+")
        self.mainwindow.create_button.setStyleSheet(styles.normal_button)
        self.mainwindow.create_button.setMinimumWidth(40)
        self.mainwindow.create_button.clicked.connect(self.initializeTaskCreation)

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(title_label)
        top_layout.addStretch(2)
        top_layout.addWidget(self.mainwindow.create_button)
        top_layout.addStretch(1)

        tasks = [task[0:2] for task in self.dbconn.display()]
    
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(styles.list_widget)
        self.task_list.setAlternatingRowColors(True)

        for task in tasks:
            task_item = QListWidgetItem(f"[{task[0]}] >  {task[1]}")
            self.task_list.addItem(task_item)

        self.task_list.activated.connect(self.initializedisplaywindow)

        main_layout.addWidget(username_label)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.task_list)
        self.mainwindow.setLayout(main_layout)
    
    def initializeTaskCreation(self):
        current_date = str(datetime.datetime.now()).split()[0]
        curr_year, _, _ = current_date.split("-")

        self.taskcreationwindow.name.setText("")
        self.taskcreationwindow.year.setValue(int(curr_year))
        self.taskcreationwindow.desc.setText("")

        self.taskcreationwindow.update_button.setVisible(False)
        self.taskcreationwindow.create_button.setVisible(True)

        self.stack.setCurrentIndex(1)
        self.taskcreationwindow.repaint()

    def taskcreationwindowSetUp(self):

        title = QLabel("Create a To-do")
        title.setFont(QFont("Arial", 24))
        title.setAlignment(Qt.AlignCenter)

        name_label = QLabel("Name")
        self.taskcreationwindow.name = QLineEdit()
        self.taskcreationwindow.name.setStyleSheet(styles.text_entry)

        due_date_label = QLabel("Due Date")
        
        self.taskcreationwindow.year = QSpinBox()
        self.taskcreationwindow.year.setStyleSheet(styles.default_grey)
        self.taskcreationwindow.year.setRange(2010, 3000)

        months = ("Unset", "January", "February", 
                 "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",)
        self.taskcreationwindow.month = QComboBox()
        self.taskcreationwindow.month.setStyleSheet(styles.default_grey)
        self.taskcreationwindow.month.addItems(months)


        self.taskcreationwindow.date = QSpinBox()
        self.taskcreationwindow.date.setStyleSheet(styles.default_grey)
        self.taskcreationwindow.date.setRange(1, 31)

        description_label = QLabel("Description")
        self.taskcreationwindow.desc = QTextEdit()
        self.taskcreationwindow.desc.setStyleSheet(styles.text_entry)
        
        self.taskcreationwindow.create_button = QPushButton("Create")
        self.taskcreationwindow.create_button.setStyleSheet(styles.normal_button)
        self.taskcreationwindow.create_button.clicked.connect(self.submitAction)

        self.taskcreationwindow.update_button = QPushButton("Update")
        self.taskcreationwindow.update_button.setStyleSheet(styles.normal_button)
        # update_button.clicked.connect(self.updateAction)

        back_button = QPushButton("Back")
        back_button.setStyleSheet(styles.red_button)
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.taskcreationwindow.create_button)
        button_layout.addWidget(self.taskcreationwindow.update_button)
        button_layout.addWidget(back_button)

        name_row = QHBoxLayout()
        date_row = QHBoxLayout()
        date_entry_box = QHBoxLayout()
        name_row.addWidget(name_label)
        name_row.addWidget(self.taskcreationwindow.name)

        date_row.addWidget(due_date_label)
        date_entry_box.addWidget(self.taskcreationwindow.date)
        date_entry_box.addWidget(self.taskcreationwindow.month)
        date_entry_box.addWidget(self.taskcreationwindow.year)
        date_row.addLayout(date_entry_box)

        desc_box = QVBoxLayout()
        desc_box.addWidget(description_label)
        desc_box.addWidget(self.taskcreationwindow.desc)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(name_row)
        layout.addLayout(date_row)
        layout.addLayout(desc_box)
        layout.addLayout(button_layout)

        self.taskcreationwindow.setLayout(layout)
         
    def initializeUpdateWindow(self, task):  
        current_date = str(datetime.datetime.now()).split()[0]
        curr_year, _, _ = current_date.split("-")

        task = self.displaywindow.task_info
        self.taskcreationwindow.name.setText(task[1])
        if task[4]:
            self.taskcreationwindow.year.setValue(int(task[4].split("-")[0]))
        else:
            self.taskcreationwindow.year.setValue(int(curr_year))
        
        if task[4]:
            self.taskcreationwindow.month.setCurrentIndex(int(task[4].split("-")[1]))
        else:
            self.taskcreationwindow.month.setCurrentIndex(0)
        
        if task[4]:
            self.taskcreationwindow.date.setValue(int(task[4].split("-")[2]))
        else:
            self.taskcreationwindow.date.setValue(1)

        self.taskcreationwindow.desc.setText(task[2])

        self.taskcreationwindow.create_button.setVisible(False)
        self.taskcreationwindow.update_button.setVisible(True)
    
        self.stack.setCurrentIndex(1)
        self.taskcreationwindow.repaint()

    def submitAction(self):
        name = self.taskcreationwindow.name.text()
        datey = int(self.taskcreationwindow.year.text())
        datem = self.taskcreationwindow.month.currentIndex()
        dated = int(self.taskcreationwindow.date.text())
        desc = self.taskcreationwindow.desc.toPlainText()

        datestr = None
        if datem:
            datestr = f"{datey}-" \
                      + "{:02d}-".format(datem) \
                      + "{:02d}".format(dated)

        response = QMessageBox()

        if name:
            response.information(self.taskcreationwindow, "Task Created.", "The Task has been created.", QMessageBox.Ok, QMessageBox.Ok)
            self.dbconn.create(name, desc, datestr)
            self.stack.close()
            self.stack.setCurrentIndex(0)
            self.initializeUI()
        else:
            response.critical(self.taskcreationwindow, "Name Required!", "Please enter a name for the to-do.", QMessageBox.Ok, QMessageBox.Ok)

    def initializedisplaywindow(self, task):
        self.task = task
        taskdetail = task.data().split()
        taskdetail.remove(">")

        taskId = taskdetail[0][1:-1]
        taskname = " ".join(taskdetail[1:])

        self.displaywindow.task_info = self.dbconn.getTaskInfo(taskId)
        self.displaywindow.task_title.setText(f"{self.displaywindow.task_info[1]}")

        self.displaywindow.desc.setText(f"{self.displaywindow.task_info[2]}")
        self.displaywindow.created_on.setText(f"{self.displaywindow.task_info[3]}")

        if self.displaywindow.task_info[4]:
            self.displaywindow.due_date.setText(f"{self.displaywindow.task_info[4]}")
        else:
            self.displaywindow.due_date.setText("Not set")            

        if self.displaywindow.task_info[5]:
            self.displaywindow.compl_date.setText(f"{self.displaywindow.task_info[5]}")
            self.displaywindow.mark_compl_but.setDisabled(True)
        else:
            self.displaywindow.compl_date.setText("Not yet completed")
            self.displaywindow.mark_compl_but.setDisabled(False)

        self.stack.setCurrentIndex(2)
        self.displaywindow.repaint()

    def displaywindowSetUp(self):
        task_title_label = QLabel("Task title")
        self.displaywindow.task_title = QLabel("---example---")
        self.displaywindow.task_title.setFont(QFont("Arial", 22))
        self.displaywindow.task_title.setStyleSheet(styles.text_entry)

        desc_label = QLabel("Description")
        self.displaywindow.desc = QLabel("--example--")
        self.displaywindow.desc.setMinimumHeight(100)
        # self.displaywindow.desc.setMaximumWidth(400)
        self.displaywindow.desc.setAlignment(Qt.AlignTop)
        self.displaywindow.desc.setWordWrap(True)
        self.displaywindow.desc.setStyleSheet(styles.text_entry)

        created_on_label = QLabel("Created on")
        self.displaywindow.created_on = QLabel("--example--")
        self.displaywindow.created_on.setStyleSheet(styles.text_entry)

        created_on_layout = QHBoxLayout()
        created_on_layout.addWidget(created_on_label)
        created_on_layout.addWidget(self.displaywindow.created_on)

        due_date_label = QLabel("Due on")
        self.displaywindow.due_date = QLabel("Not Set")
        self.displaywindow.due_date.setStyleSheet(styles.text_entry)

        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(due_date_label)
        due_date_layout.addWidget(self.displaywindow.due_date)    

        compl_date_label = QLabel("Completed on")
        self.displaywindow.compl_date = QLabel("Not Yet Completed")
        self.displaywindow.compl_date.setStyleSheet(styles.text_entry)

        compl_date_layout = QHBoxLayout()
        compl_date_layout.addWidget(compl_date_label)
        compl_date_layout.addWidget(self.displaywindow.compl_date)

        upper_button_layout = QHBoxLayout()
        edit_task_but = QPushButton("Edit Task")
        edit_task_but.clicked.connect(self.initializeUpdateWindow)

        self.displaywindow.mark_compl_but = QPushButton("Mark as Completed")
        self.displaywindow.mark_compl_but.clicked.connect(self.completeAction)
        
        upper_button_layout.addWidget(edit_task_but)
        upper_button_layout.addWidget(self.displaywindow.mark_compl_but)

        lower_button_layout = QHBoxLayout()
        delete_but = QPushButton("Delete this task")
        delete_but.clicked.connect(self.deleteAction)
        back_but = QPushButton("Back")
        back_but.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back_but.setStyleSheet(styles.red_button)
        lower_button_layout.addWidget(delete_but)
        lower_button_layout.addWidget(back_but)

        layout = QVBoxLayout()
        layout.addWidget(task_title_label)
        layout.addWidget(self.displaywindow.task_title)
        layout.addWidget(desc_label)
        layout.addWidget(self.displaywindow.desc)
        layout.addLayout(created_on_layout)
        layout.addLayout(due_date_layout)
        layout.addLayout(compl_date_layout)
        layout.addLayout(upper_button_layout)
        layout.addLayout(lower_button_layout)
        self.displaywindow.setLayout(layout)

    def deleteAction(self):
        warning = QMessageBox()
        response = warning.warning(self.displaywindow, "Warning", "Are you sure you want to delete this task? This action can't be undone.", QMessageBox.Yes, QMessageBox.No)
        if response == QMessageBox.Yes:
            self.dbconn.delete(self.displaywindow.task_info[0])
            self.task_list.reset()
           
            self.task_list.takeItem(self.task.row())
            self.mainwindow.repaint()
            self.displaywindow.close()
            self.stack.setCurrentIndex(0)
    
    def completeAction(self):
        self.dbconn.mark_complete(self.displaywindow.task_info[0])
        current_date = str(datetime.datetime.now()).split()[0]
        self.displaywindow.mark_compl_but.setDisabled(True)
        self.displaywindow.mark_compl_but.setText("Completed")
        self.displaywindow.compl_date.setText(current_date)
        self.displaywindow.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = ToDoList("harry", dbclass.dbhelper("harry"))
    sys.exit(app.exec_())