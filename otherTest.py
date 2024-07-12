from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QPushButton, QLineEdit, QTextEdit, QComboBox, QLabel
import sys
import winreg
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        # Tab 1 widgets
        self.browseButton1 = self.findChild(QPushButton, 'browseButton1')
        self.filePathLineEdit1 = self.findChild(QLineEdit, 'filePathLineEdit1')
        self.captureButton = self.findChild(QPushButton, 'captureButton')
        self.createFileButton = self.findChild(QPushButton, 'createFileButton')
        self.textEditZone = self.findChild(QTextEdit, 'textEditZone')
        self.filePathLineEdit1.setReadOnly(True)

        # Tab 2 widgets
        self.browseButton2 = self.findChild(QPushButton, 'browseButton2')
        self.filePathLineEdit2 = self.findChild(QLineEdit, 'filePathLineEdit2')
        self.appComboBox = self.findChild(QComboBox, 'appComboBox')
        self.appLabel = self.findChild(QLabel, 'replayLabel')

        self.browseButton1.clicked.connect(self.open_file_search)
        self.captureButton.clicked.connect(self.capture_button_click)
        self.populateAppComboBox()

    def capture_button_click(self):
        if self.filePathLineEdit1.text() == "Select a file":
            reply = QMessageBox.information(self, "Popup","Doing so will create a new file, please choose a destination", QMessageBox.Cancel|QMessageBox.Ok, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                self.create_new_file()
        else:
            QMessageBox.critical(self, "Popup","Doing so will delete everything that's in the selected file, do you want to ignore or cancel the delete ?", QMessageBox.Ignore|QMessageBox.Cancel, QMessageBox.Cancel)

    def create_new_file(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Create New File", "", "Json Files (*.json);;All Files (*)", options=options)
        if filePath:
            try:
                with open(filePath, 'w') as file:
                    #file.write("")
                    pass
                self.filePathLineEdit1.setText(filePath)
                #self.displayJsonContent(filePath)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file:\n{str(e)}")

    def displayJsonContent(self, filePath):
        try:
            with open(filePath, 'r') as file:
                data = json.load(file)
                json_str = json.dumps(data, indent=4)
                self.textEditZone.setPlainText(json_str)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON file:\n{str(e)}")

    def open_file_search(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "JSON Files (*.json);;All Files (*)", options=options)
        print(filePath)
        if filePath:
            print("filepath ok")
            self.filePathLineEdit1.setText(filePath)
            self.displayJsonContent(filePath)

    def populateAppComboBox(self):
        apps = self.get_installed_apps()
        self.appComboBox.addItems(apps)

    def get_installed_apps(self):
        apps = []
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for reg_path in reg_paths:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    sub_key = winreg.OpenKey(reg_key, sub_key_name)
                    try:
                        app_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        if app_name:
                            apps.append(app_name)
                    except EnvironmentError:
                        continue
            except WindowsError:
                continue
        print(apps)
        return apps


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
