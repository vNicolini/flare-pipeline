import sys
from PyQt6.QtWidgets import QApplication
from flarelauncher.ui import FlareLauncher

def main():
    app = QApplication(sys.argv)
    window = FlareLauncher()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
