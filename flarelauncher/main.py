import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGroupBox, QScrollArea, QMenu, QGridLayout, QVBoxLayout, QSystemTrayIcon
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QSize
import yaml

class MainWindow(QMainWindow):
    APP_TITLE = "Flare DCC Launcher"
    ICON_PATH = "icons/flare-launcher.png"
    TRAY_TOOLTIP = "Flare Launcher"

    def __init__(self):
        super().__init__()

        # Set window Title
        self.setWindowTitle(self.APP_TITLE)

        # Set window icon
        app_icon = QIcon(self.ICON_PATH)
        self.setWindowIcon(app_icon)

        # Set dark theme using stylesheet
        self.set_style_sheet()

        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Load configuration from YAML file
        self.load_config()

        # Add categories and buttons based on the configuration
        self.add_categories_from_config()

        # Set default size of the main window
        self.resize(450, 650)

        # Create system tray icon
        self.create_tray_icon()

        # Hide the main window initially
        self.hide()

    def load_config(self):
        with open('../flare-launcher-config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

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

    def add_categories_from_config(self):
        departments = {}
        for app in self.config['applications']:
            department = app['department']
            if department not in departments:
                departments[department] = []
            departments[department].append(app)

        for department, apps in departments.items():
            button_specs = []
            for app in apps:
                actions = []
                for env in app['environment']:
                    action_text = env['name']
                    callback = self.create_launch_function(env['rez_package'], env['command'])
                    actions.append((action_text, callback))
                button_specs.append((app['name'], app['icon'], actions))
            self.add_category(department, *button_specs)

    def create_launch_function(self, rez_package, command):
        def launch_function():
            full_command = f"pwsh -NoExit -Command rez-env {rez_package} -- {command}"
            subprocess.Popen(full_command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return launch_function

    def add_category(self, title, *button_specs):
        group_box = QGroupBox(title)
        layout = QGridLayout()

        for idx, (button_text, icon_path, actions) in enumerate(button_specs):
            row = idx // 2
            col = idx % 2
            self.add_button(button_text, icon_path, actions, layout, row, col)

        group_box.setLayout(layout)

        # Add the group box to a scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(group_box)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(scroll_area)

    def add_button(self, text, icon_path, actions, layout, row, col):
        button = QPushButton(text)
        if icon_path and not QIcon(icon_path).isNull():
            # Set the icon to a medium size
            icon = QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(QSize(48, 48))  # Adjust this value as needed for your desired icon size

        # Create context menu
        menu = QMenu()
        for action_text, callback in actions:
            action = menu.addAction(action_text)
            action.triggered.connect(callback)

        button.setMenu(menu)
        layout.addWidget(button, row, col)  # Add to the calculated position in grid

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)

        # Set tray icon (use appropriate path for your application icon)
        icon = QIcon(self.ICON_PATH)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip(self.TRAY_TOOLTIP)

        # Create a menu for the system tray
        tray_menu = QMenu()

        # Add "Exit" action to quit the application
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(app.quit)
        tray_menu.addAction(exit_action)

        # Set context menu to show only when right-clicking
        self.tray_icon.setContextMenu(tray_menu)

        # Connect activated signal for showing/hiding the main window
        self.tray_icon.activated.connect(self.show_main_window)

        self.tray_icon.show()

    def closeEvent(self, event):
        if not self.isHidden():
            event.ignore()
            self.hide()  # Hide the window instead of closing it

    def show_main_window(self, reason):
        # Only trigger when left-clicking on the tray icon
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden() or not self.isVisible():
                self.showNormal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())