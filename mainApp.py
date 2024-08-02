from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QPushButton, QLineEdit, QTextEdit, QComboBox, QLabel
import sys
import winreg
import json
import os
from inputsLogic import InputHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.currentReplayAppPath = ""

        self.inputHandler = InputHandler()._instance
        # Tab 1 widgets
        self.browseButton1 = self.findChild(QPushButton, 'browseButton1')
        self.filePathLineEdit1 = self.findChild(QLineEdit, 'filePathLineEdit1')
        self.captureButton = self.findChild(QPushButton, 'captureButton')
        self.createFileButton = self.findChild(QPushButton, 'createFileButton')
        self.textEditZone = self.findChild(QTextEdit, 'textEditZone')
        self.recordingLabel = self.findChild(QLabel, "recordingLabel")
        self.emptyButton = self.findChild(QPushButton, 'emptyButton')
        self.refreshButton = self.findChild(QPushButton, 'refreshButton')
        self.recordingLabel.setVisible(False)
        self.filePathLineEdit1.setReadOnly(True)
        self.textEditZone.setReadOnly(True)

        # Tab 2 widgets
        self.browseButton2 = self.findChild(QPushButton, 'browseButton2')
        self.browseButton3 = self.findChild(QPushButton, 'browseButton3')
        self.replayButton = self.findChild(QPushButton, "replayButton")
        self.filePathLineEdit2 = self.findChild(QLineEdit, 'filePathLineEdit2')
        self.appComboBox = self.findChild(QComboBox, 'appComboBox')
        self.appLabel = self.findChild(QLabel, 'replayLabel')

        self.filePathLineEdit2.setReadOnly(True)


        self.browseButton1.clicked.connect(lambda: self.open_file_search(self.filePathLineEdit1))
        self.browseButton2.clicked.connect(lambda: self.open_file_search(self.filePathLineEdit2))
        self.browseButton3.clicked.connect(self.open_app_search)
        self.captureButton.clicked.connect(self.capture_button_click)
        self.createFileButton.clicked.connect(self.create_new_file)
        self.emptyButton.clicked.connect(self.empty_file)
        self.refreshButton.clicked.connect(self.refreshFile)
        self.replayButton.clicked.connect(self.replay_button_clicked)

        self.inputHandler.started.connect(self.startRecording)
        self.inputHandler.finished.connect(lambda: self.recordingLabel.setText("Stopped recording"))

        self.populateAppComboBox()


    def refreshFile(self):
        if self.filePathLineEdit1.text() == "Select a file":
            QMessageBox.information(self, "Error", "Cannot refresh if no file is currently selected")
        else:
            print(self.file_is_empty())
            if self.file_is_empty():
                QMessageBox.information(self, "No preview available", "This file is empty")
            else:
                self.displayJsonContent(self.filePathLineEdit1.text())
                QMessageBox.information(self, "Information", "File preview refreshed")

    def startRecording(self):
        self.recordingLabel.setText("Currently recording") 
        self.recordingLabel.setVisible(True)

    def file_is_empty(self):
        file_path = self.filePathLineEdit1.text()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read().strip() #strip removes every whitespace at the beginning and end of the file
                return content == "" or  content == "{}"
        return True

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

    def capture_button_click(self):
        if self.filePathLineEdit1.text() == "Select a file":
            reply = QMessageBox.information(self, "Popup","Doing so will create a new file, please choose a destination", QMessageBox.Cancel|QMessageBox.Ok, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                self.create_new_file()
        else:
            if not self.file_is_empty():
                reply = QMessageBox.critical(self, "Popup","You must select an empty file", QMessageBox.Ok)
            else:
                self.recordingLabel.setVisible(True)
                self.inputHandler.capture_inputs(5, self.filePathLineEdit1.text())
                self.displayJsonContent(self.filePathLineEdit1.text())
                self.recordingLabel.setVisible(False)

    def displayJsonContent(self, filePath):
        try:
            with open(filePath, 'r') as file:
                data = json.load(file)
                json_str = json.dumps(data, indent=4)
                self.textEditZone.setPlainText(json_str)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON file:\n{str(e)}")

    def open_app_search(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Application", "", "Executable Files (*.exe);", options=options)
        if filePath:
            self.currentReplayAppPath = filePath
            app_name = os.path.basename(filePath)
            self.appComboBox.addItem(app_name)
            self.appComboBox.setCurrentText(app_name)

    def open_file_search(self, line_edit):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "JSON Files (*.json);;All Files (*)", options=options)
        print(filePath)
        if filePath:
            line_edit.setText(filePath)
            if line_edit == self.filePathLineEdit1 and not self.file_is_empty():
                self.displayJsonContent(filePath)

    def empty_file(self):
        file_path = self.filePathLineEdit1.text()

        if file_path == "Select a file":
            QMessageBox.information(self, "Error", "No file selected to empty.")
            return
        elif self.file_is_empty():
            QMessageBox.information(self, "Already empty", "This file is already empty")
            return
        try:
            with open(file_path, 'w') as file:
                file.write("")
            QMessageBox.information(self, "Success", "JSON file has been emptied.")
            self.displayJsonContent(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to empty JSON file:\n{str(e)}")

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
    
    def replay_button_clicked(self):
        app_name = self.appComboBox.currentText()
        if self.currentReplayAppPath != "":
            self.inputHandler.replay_inputs(self.filePathLineEdit2.text(), self.currentReplayAppPath)
        else:
            QMessageBox.critical(self, "Error", "Application path not found")
    


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
