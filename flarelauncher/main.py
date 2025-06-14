import sys
import yaml
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from ui import Ui_MainWindow
from tray_icon import SystemTrayIcon

class ApplicationLauncher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.load_config()
        self.init_ui()
        self.init_tray_icon()

    def load_config(self):
        with open('../flare-launcher-config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

    def init_ui(self):
        self.main_window = Ui_MainWindow(self.config)
        app_icon = QIcon("icons/icon-512.png")
        self.main_window.setWindowIcon(app_icon)
        self.main_window.setWindowTitle('Flare DCC Launcher')
        self.main_window.show()

    def init_tray_icon(self):
        self.tray_icon = SystemTrayIcon(QIcon('icons/icon-512.png'), self.main_window)
        self.tray_icon.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == '__main__':
    launcher = ApplicationLauncher()
    launcher.run()