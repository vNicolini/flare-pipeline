import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QListWidgetItem
from PyQt6.QtGui import QIcon
import yaml
import os
import subprocess

def launch_app_with_rez(rez_package: str, command: str):
    full_command = f"rez env {rez_package} -- {command}"
    subprocess.Popen(full_command, shell=True)

class FlareLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flare - VFX Launcher")
        self.resize(500, 350)

        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.launch_button = QPushButton("Launch Selected")

        self.layout.addWidget(QLabel("Select Application to Launch:"))
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.launch_button)
        self.setLayout(self.layout)

        self.load_applications()
        self.launch_button.clicked.connect(self.launch_selected_app)

    def load_applications(self):
        with open("flare-launcher-config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print("Loaded config:", config)  # Debug line

            # Ensure we're getting the correct structure
            self.apps = config.get("applications", [])

            for app in self.apps:
                print("App:", app)  # Debug line to inspect each app

                item_text = f"{app['name']} - {app['description']}"
                item = QListWidgetItem(item_text)

                icon_path = app.get("icon")
                if icon_path and os.path.exists(icon_path):
                    print(f"Icon found at: {icon_path}")
                    item.setIcon(QIcon(icon_path))
                else:
                    print(f"Icon not found at: {icon_path}")

                self.list_widget.addItem(item)


    def launch_selected_app(self):
        index = self.list_widget.currentRow()
        if index >= 0:
            app = self.apps[index]
            launch_app_with_rez(app["rez_package"], app["command"])

def main():
    app = QApplication(sys.argv)
    window = FlareLauncher()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    app = QApplication(sys.argv)
    window = FlareLauncher()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()