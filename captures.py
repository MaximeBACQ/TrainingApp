#import pyautogui
#import pyinputplus as pyip
from pynput import keyboard, mouse
from pynput.keyboard import Key
import pyautogui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
import threading
import json
import winreg

currentActions = []

specialkey_mapping = {  #because pyautogui can't handle pynput's special keys
    Key.enter: 'enter',
    Key.space: 'space',
    Key.backspace: 'backspace',
    Key.tab: 'tab',
    Key.esc: 'esc',
    Key.shift: 'shift',
    Key.ctrl_l: 'ctrl',
    Key.ctrl_r: 'ctrl',
    Key.alt_l: 'alt',
    Key.alt_r: 'alt',
    Key.up: 'up',
    Key.down: 'down',
    Key.left: 'left',
    Key.right: 'right',
    Key.delete: 'delete',
    Key.home: 'home',
    Key.end: 'end',
    Key.page_up: 'pageup',
    Key.page_down: 'pagedown'
}

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
        currentActions.append(('keyboard', str(key)))
    except AttributeError:
        if(key==keyboard.Key.esc):
            return False
        print(f"Special key down: {key}")
        currentActions.append(('keyboard', str(key)))



def keyReleased(key):
    print(f"Key up: {key}")

def capture_inputs(duration):
    global currentActions
    def stop_listener():
        global currentActions
        listener.stop()
        print("Capture thread ended.")
        with open('actions.json', 'w') as file:
            json.dump(currentActions, file)
        currentActions = []
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
    
def replay_inputs():
    with open('actions/actions.json', 'r') as file:
        currentActions = json.load(file)

    for action in currentActions:
        device, details = action
        if device == "keyboard":
            key = eval(details)
            if isinstance(key,str):
                pyautogui.press(key)
            elif key in specialkey_mapping:
                pyautogui.press(specialkey_mapping[key])



def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

# window()
capture_inputs(10)
replay_inputs()