from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
import subprocess

def launch_app_with_rez(rez_package: str, command: str):
    full_command = f"rez env {rez_package} -- {command}"
    subprocess.Popen(full_command, shell=True)

class Ui_MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('background-color: #2E2E2E; color: #FFFFFF;')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        for app in self.config['applications']:
            button = QPushButton(app['name'])
            button.setIcon(QIcon(app['icon']))
            button.setStyleSheet('QPushButton { background-color: #444444; color: #FFFFFF; }')
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(self.show_context_menu)
            layout.addWidget(button)
    
    def show_context_menu(self, position):
        button = self.sender()
        menu = QMenu(self)

        for app in self.config['applications']:
            if app['name'] == button.text():
                for env in app['environment']:
                    action = QAction(env['name'], self)
                    action.triggered.connect(lambda checked, rez_package=env['rez_package'], command=env['command']: self.handle_action_triggered(checked, rez_package, command))
                    menu.addAction(action)

        menu.exec(button.mapToGlobal(position))
  
    def handle_action_triggered(self, checked, rez_package, command):
        launch_app_with_rez(rez_package, command)