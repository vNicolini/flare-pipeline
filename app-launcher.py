import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGroupBox, QScrollArea, QMenu, QGridLayout, QVBoxLayout, QSystemTrayIcon
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App Launcher")

        # Set dark theme using stylesheet
        self.set_style_sheet()

        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Add collapsible categories with buttons

        self.add_category("Modeling / Rigging / Animation / Layout",
                            ("3ds Max 2023.2.2", "C:/Program Files/Autodesk/3ds Max 2023/icons/icon_main.ico",
                            [("3ds Max", self.launch_max23)]),
                            ("3ds Max 2025.3", "C:/Program Files/Autodesk/3ds Max 2025/icons/icon_main.ico",
                            [("3ds Max", self.launch_max25)]),
                            ("Maya 2025.3", "C:/Program Files/Autodesk/Maya2025/icons/mayaico.png",
                            [("Maya 2025.3", self.launch_maya25),
                            ("RenderMan 26.3", self.launch_maya25_Prman263),
                            ("MtoA 5.5.2.0 (Core 7.4.2.0)", self.launch_maya25_Arnold5520)]))

        self.add_category("CFX / FX / Environment",
                            ("Houdini 20.5.445", "C:/Program Files/Side Effects Software/Houdini 20.5.445/houdini/python3.11libs/bookish/static/editor/favicon.ico",
                            [("Core", self.launch_houdini205445_core),
                            ("FX", self.launch_houdini205445_fx)]))

        self.add_category("Texturing",
                            ("Substance Painter 11.0.1", "C:/Program Files/Adobe/Adobe Substance 3D Painter/resources/python-doc/_static/pt_appicon_256.png",
                            [("Substance Painter",self.launch_substancePainter)]),

                            ("Mari 7.1v2", "C:/Program Files/Mari7.1v2/Bundle/Media/Icons/Mari.png",
                            [("Mari NC", self.launch_mari_nc),
                            ("Mari", self.launch_mari)]))

        self.add_category("Assembly / LookDev / Lighting",
                            ("Gaffer 1.5.14.0", "C:/Program Files/Gaffer/1.5.14.0/graphics/GafferLogoMini.png",
                            [("RenderMan 26.3", self.launch_gaffer15140_Prman263),
                            ("Arnold Core 7.4.2.0", self.launch_gaffer15140_Arnold7420),
                            ("Arnold Core 7.4.2.0 and RenderMan 26.3", self.launch_gaffer15140_Arnold7420_Prman263)]),

                            ("Maya 2025.3", "C:/Program Files/Autodesk/Maya2025/icons/mayaico.png",
                            [("RenderMan 26.3", self.launch_maya25_Prman263),
                            ("MtoA 5.5.2.0 (Core 7.4.2.0)", self.launch_maya25_Arnold5520)]))

        self.add_category("Compositing / Editing / Review",
                        ("Nuke 15.2v1", "C:/Program Files/Nuke15.2v1/plugins/icons/NukeApp256.png",
                            [("NC", self.launch_nuke1521_nc),
                            ("NC Nuke Studio", self.launch_nukeStudio1521_nc),
                            ("NC NukeX", self.launch_nukeX1521_nc)]),
                        ("Hiero 15.2v1", "C:/Program Files/Nuke15.2v1/Documentation/PythonDevGuide/Nuke/Hiero/_static/Hiero128.png",
                            [("Hiero", self.launch_hiero1521),
                            ("Hiero Player", self.launch_hieroPlayer1521)]),
                        ("Syntheyes 2024", "C:/Program Files/BorisFX/SynthEyes 2024/syntheyes_icon_alpha.png",
                            [("Syntheyes", self.launch_syntheyes)]),
                        ("OpenRV", "F:/Pipeline/Utilities/Executables/OpenRV/1.0.0/OpenRV_icon.png",
                            [("OpenRV", self.launch_openrv)]))

        # Set default size of the main window
        self.resize(450, 650)

        # Create system tray icon
        self.create_tray_icon()
        
        # Hide the main window initially
        self.hide()

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
        icon = QIcon("F:/Pipeline/Utilities/Executables/Launcher/icons/favicon.ico")
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("App Launcher")
    
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


    def launch_gaffer15140_Prman263(self):
        command = "pwsh -NoExit -Command rez-env gaffer_software==1.5.14.0 renderman_gaffer_plugin==26.3 -- gaffer"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_gaffer15140_Arnold7420(self):
        command = "pwsh -NoExit -Command rez-env gaffer_software==1.5.14.0 arnold_core_plugin==7.4.2.0 -- gaffer"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_gaffer15140_Arnold7420_Prman263(self):
        command = "pwsh -NoExit -Command rez-env gaffer_software==1.5.14.0 arnold_core_plugin==7.4.2.0 renderman_gaffer_plugin==26.3 -- gaffer"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_maya25(self):
        command = "pwsh -NoExit -Command rez-env maya_software==2025.3 -- maya"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_maya25_Prman263(self):
        command = "pwsh -NoExit -Command rez-env maya_software==2025.3 renderman_maya_plugin==26.3 -- maya"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_maya25_Arnold5520(self):
        command = "pwsh -NoExit -Command rez-env maya_software==2025.3 arnold_maya_plugin==5.5.2.0 -- maya"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_max23(self):
        command = "pwsh -NoExit -Command rez-env 3dsmax_software==2023.2.2 -- 3dsmax"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_max25(self):
        command = "pwsh -NoExit -Command rez-env 3dsmax_software==2025.3 -- 3dsmax"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_houdini205445_core(self):
        command = "pwsh -NoExit -Command rez-env houdini_software==20.5.445 -- houdinicore"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_houdini205445_fx(self):
        command = "pwsh -NoExit -Command rez-env houdini_software==20.5.445 -- houdinifx"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_nuke1521_nc(self):
        command = "pwsh -NoExit -Command rez-env nuke_software==15.2.1 -- nuke15.2 --nc"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_nukeStudio1521_nc(self):
        command = "pwsh -NoExit -Command rez-env nuke_software==15.2.1 -- nuke15.2 --studio --nc"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_nukeX1521_nc(self):
        command = "pwsh -NoExit -Command rez-env nuke_software==15.2.1 -- nuke15.2 --nukex --nc"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_hiero1521(self):
        command = "pwsh -NoExit -Command rez-env nuke_software==15.2.1 -- nuke15.2 --hiero"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_hieroPlayer1521(self):
        command = "pwsh -NoExit -Command rez-env nuke_software==15.2.1 -- nuke15.2 --player"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_syntheyes(self):
        command = "pwsh -NoExit -Command rez-env syntheyes_software -- SynthEyes64"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_openrv(self):
        command = "pwsh -NoExit -Command rez-env openrv_software -- rv.exe"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_substancePainter(self):
        command = "pwsh -NoExit -Command rez-env substancePainter_software -- 'Adobe Substance 3D Painter'"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_mari_nc(self):
        command = "pwsh -NoExit -Command rez-env mari_software -- Mari7.1v2 --nc -platform windows:nowmpointer"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def launch_mari(self):
        command = "pwsh -NoExit -Command rez-env mari_software -- Mari7.1v2 -platform windows:nowmpointer"
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())