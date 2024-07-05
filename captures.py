#import pyautogui
#import pyinputplus as pyip
from pynput import keyboard, mouse
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
import threading
#import json

class MyWindow(QMainWindow): #extends from the QMainWindow class
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 1920,1080)
        self.setWindowTitle('Max App')
        self.initUI()

    def initUI(self):
        label = QtWidgets.QLabel(self) #since mywindow inherits from qmainwindow, calling self is like calling a QMainWindow (and win is one)
        label.setText('test label')
        label.move(200,200)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("button")
        b1.clicked.connect(lambda:capture_inputs(5))


def keyPressed(key):
    try:
        print(f"Key down: {key.char}")
    except AttributeError:
        if(key==keyboard.Key.esc):
            return False
        print(f"Special key down: {key}")

def keyReleased(key):
    print(f"Key up: {key}")

def capture_inputs(duration):
    def stop_listener():
        listener.stop()
        print("Capture thread ended.")
    # with keyboard.Listener(
    #         on_press=keyPressed   #on_press gives the parameter, no need for parenthesis when writing keyPressed
    #         #,on_release=keyReleased
    #         ) as listener:
    #   listener.join()  #join blocks the program until pynput is done listening
    listener = keyboard.Listener(
        on_press=keyPressed,
        on_release=keyReleased
    )
    listener.start()

    timer = threading.Timer(duration, stop_listener)

    timer.start()

    listener.join()
    

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
#capture_inputs()