#import pyautogui
#import pyinputplus as pyip
from pynput import keyboard, mouse
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
#import time
#import json


def keyPressed(key):
    try:
        print(f"Key down: {key.char}")
    except AttributeError:
        if(key==keyboard.Key.esc):
            return False
        print(f"Special key down: {key}")

def keyReleased(key):
    print(f"Key up: {key}")

def capture_inputs():
    with keyboard.Listener(
            on_press=keyPressed   #on_press gives the parameter, no need for parenthesis when writing keyPressed
            #,on_release=keyReleased
            ) as listener:
        listener.join()  #join blocks the program until pynput is done listening

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100,100, 1920,1080)
    win.setWindowTitle('Max App')

    label = QtWidgets.QLabel(win)
    label.setText('test label')
    label.move(200,200)

    win.show()
    sys.exit(app.exec_())

window()
capture_inputs()