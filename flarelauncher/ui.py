from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenu, QLabel, QGridLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QSize
import subprocess

def launch_app_with_rez(rez_package: str, command: str):
    full_command = f"rez env {rez_package} -- {command}"
    subprocess.Popen(full_command, shell=True)

class Ui_MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        # Set dark theme using stylesheet
        self.set_style_sheet()    
    
    def set_style_sheet(self):
        stylesheet = """
        QMainWindow {
            background-color: #2e3440;
            color: #d8dee9;
        }
        QPushButton {
            background-color: #3b4252;
            border: 1px solid #4c566a;
            padding: 5px;
            border-radius: 3px;
            color: #d8dee9;
        }
        QPushButton:hover {
            background-color: #434c5e;
        }
        QGroupBox {
            border: 1px solid #4c566a;
            margin-top: 0.5em;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 2px 5px;
            color: #8fbcbb;
        }
        """
        self.setStyleSheet(stylesheet)

    def init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout(central_widget)

        # Group applications by department
        grouped_apps = {}
        for app in self.config['applications']:
            department = app['department']
            if department not in grouped_apps:
                grouped_apps[department] = []
            grouped_apps[department].append(app)

        # Create UI elements for each department
        
        row = 0
        
        num_columns = 2 # Define the number of columns
        
        for department, apps in grouped_apps.items():
            department_label = QLabel(department)
            department_label.setStyleSheet('font-weight: bold;')
            layout.addWidget(department_label, row, 0, 1, num_columns)
            row += 1

            col = 0
            for app in apps:
                button_layout = QVBoxLayout()

                button = QPushButton()
                button.setIcon(QIcon(app['icon']))

                # Increase icon size
                button.setIconSize(QSize(48, 48))
                button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

                # Connect both right-click and left-click to show_context_menu
                button.customContextMenuRequested.connect(self.show_context_menu)
                button.clicked.connect(lambda _, pos=button.pos(): self.show_context_menu(pos))

                button_layout.addWidget(button)

                app_name = QLabel(app['name'])
                app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
                app_name.setStyleSheet('color: #FFFFFF;')
                button_layout.addWidget(app_name)

                layout.addLayout(button_layout, row, col)
                col += 1
                if col >= num_columns:
                    col = 0
                    row += 1
            if col != 0:
                row += 1
    
    def show_context_menu(self, position):
        button = self.sender()
        menu = QMenu(self)
        button_text = button.text().strip()  # Ensure no leading/trailing whitespace
        print(f"Showing context menu for button: '{button_text}'")

        for app in self.config['applications']:
            app_name = app['name'].strip()  # Ensure no leading/trailing whitespace
            print(f"Checking application: '{app_name}'")
            if app_name == button_text:
                for env in app['environment']:
                    action = QAction(env['name'], self)
                    action.triggered.connect(lambda checked, rez_package=env['rez_package'], command=env['command']: self.handle_action_triggered(checked, rez_package, command))
                    menu.addAction(action)
                    print(f"Added action: {env['name']}")

        menu.exec(button.mapToGlobal(position))
  
    def handle_action_triggered(self, checked, rez_package, command):
        launch_app_with_rez(rez_package, command)