
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setup_menu()

    def setup_menu(self):
        menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.parent.show)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.parent.close)

        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(quit_action)

        self.setContextMenu(menu)