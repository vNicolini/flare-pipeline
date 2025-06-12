# ui_main.py
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QComboBox, QListWidgetItem
from PyQt6.QtGui import QIcon
import yaml
import subprocess
import sys

def launch_app_with_rez(rez_package: str, command: str):
    full_command = f"rez env {rez_package} -- {command}"
    subprocess.Popen(full_command, shell=True)

class FlareLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flare - VFX Launcher")
        self.resize(500, 350)

        self.layout = QVBoxLayout()
        self.department_combo = QComboBox()
        self.list_widget = QListWidget()
        self.launch_button = QPushButton("Launch Selected")

        self.layout.addWidget(QLabel("Select Department:"))
        self.layout.addWidget(self.department_combo)
        self.layout.addWidget(QLabel("Select Application to Launch:"))
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.launch_button)
        self.setLayout(self.layout)

        self.load_departments()
        self.department_combo.currentIndexChanged.connect(self.load_applications)
        self.launch_button.clicked.connect(self.launch_selected_app)

    def load_departments(self):
        with open("flare-launcher-config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print("Loaded config:", config)  # Debug line

            departments = set()
            for app in config.get("applications", []):
                department = app.get("department")
                if department:
                    departments.add(department)

            self.department_combo.addItems(["All"] + sorted(departments))

    def load_applications(self):
        selected_department = self.department_combo.currentText()
        with open("flare-launcher-config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print("Loaded config:", config)  # Debug line

            # Ensure we're getting the correct structure
            self.apps = []
            for app in config.get("applications", []):
                if selected_department == "All" or app.get("department") == selected_department:
                    self.apps.append(app)

            self.list_widget.clear()
            for app in self.apps:
                print("App:", app)  # Debug line to inspect each app

                item_text = f"{app['name']} - {app['description']}"
                item = QListWidgetItem(item_text)

                icon_path = os.path.join(os.path.dirname(__file__), app.get("icon"))
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