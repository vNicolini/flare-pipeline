import os
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGroupBox, QScrollArea, QMenu, QGridLayout, QVBoxLayout, QSystemTrayIcon, QHBoxLayout, QDialog, QTextEdit, QLabel, QComboBox, QFileDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QSize
import yaml

class MainWindow(QMainWindow):
    APP_TITLE = "Flare DCC Launcher"
    ICON_PATH = os.path.join(os.path.dirname(__file__), "icons", "flare-launcher.png")  # Ensure this path is correct
    TRAY_TOOLTIP = "Flare Launcher"
    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..")  # Directory containing YAML configuration files
    DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "flare-launcher-config.yaml")  # Default configuration file

    def __init__(self):
        super().__init__()

        # Initialize the config file path
        self.config_file_path = os.path.abspath(self.DEFAULT_CONFIG)

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

        # Wrap the central widget in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(scroll_area)

        # Add buttons to the top-right corner
        self.add_config_buttons()

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
        with open(self.config_file_path, 'r') as file:
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

        # Add the group box to the main layout
        self.layout.addWidget(group_box)

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

        return button

    def set_uniform_button_size(self, buttons):
        max_width = max(button.sizeHint().width() for button in buttons)
        max_height = max(button.sizeHint().height() for button in buttons)

        for button in buttons:
            button.setFixedSize(max_width, max_height)

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

    def show_config_window(self):
        config_dialog = QDialog(self)
        config_dialog.setWindowTitle("Configuration File")

        # Get the absolute path of the config file
        config_path = os.path.abspath(self.config_file_path)

        # Create a text edit to display the config file contents
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        # Load the config file contents
        with open(config_path, 'r') as file:
            config_contents = file.read()
            text_edit.setPlainText(config_contents)

        # Create a label to display the config file path
        path_label = QLabel(f"Config File Path: {config_path}")

        # Set the layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(path_label)  # Add the path label at the top
        layout.addWidget(text_edit)
        config_dialog.setLayout(layout)

        # Show the dialog
        config_dialog.exec()

    def add_config_buttons(self):
        # Create a layout for the top-right corner
        top_layout = QHBoxLayout()
        top_layout.addStretch()

        # Add the "Show Config" button
        config_button = QPushButton("Show Config")
        config_button.clicked.connect(self.show_config_window)
        top_layout.addWidget(config_button)

        # Add the "Change Config" dropdown menu
        self.config_dropdown = QComboBox()
        self.config_dropdown.addItem("Browse...")
        self.load_config_files()
        self.config_dropdown.setCurrentText(os.path.basename(self.DEFAULT_CONFIG))
        self.config_dropdown.currentIndexChanged.connect(self.on_config_selected)
        top_layout.addWidget(self.config_dropdown)

        # Add the "Refresh" button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_ui)
        top_layout.addWidget(refresh_button)

        # Add the top layout to the main layout
        self.layout.insertLayout(0, top_layout)

    def load_config_files(self):
        if os.path.exists(self.CONFIG_DIR):
            for file_name in os.listdir(self.CONFIG_DIR):
                if file_name.endswith('.yaml'):
                    self.config_dropdown.addItem(file_name)

    def on_config_selected(self, index):
        selected_text = self.config_dropdown.currentText()
        if selected_text == "Browse...":
            self.browse_config_file()
        else:
            self.config_file_path = os.path.join(self.CONFIG_DIR, selected_text)
            self.refresh_ui()

    def browse_config_file(self):
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Configuration File", "", "YAML Files (*.yaml);;All Files (*)", options=options)

        if file_name:
            self.config_file_path = file_name
            self.refresh_ui()

    def refresh_ui(self):
        # Clear the existing layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Reload the configuration
        self.load_config()

        # Add categories and buttons based on the new configuration
        self.add_categories_from_config()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())