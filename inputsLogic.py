import json
import threading
from pynput import keyboard
import pyautogui
from pynput.keyboard import Key
from PyQt5.QtCore import QObject, pyqtSignal

#I've used the singleton design pattern for this class so that there are never two running inputhandlers
class InputHandler(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    _instance = None

    def __new__(cls, *args, **kwargs): 
        if not cls._instance: 
            # This calls the __new__ method of the base class (object) to create a new instance of InputHandler
            cls._instance = super(InputHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'initialized'):
            self.currentActions = []
            self.specialkey_mapping = {
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
            self.initialized = True

    def keyPressed(self, key):
        try:
            print(f"Key down: {key.char}")
            self.currentActions.append(('keyboard', key.char))
        except AttributeError:
            if key == keyboard.Key.esc:
                return False
            print(f"Special key down: {key}")
            self.currentActions.append(('keyboard', str(key)))

    def keyReleased(self, key):
        print(f"Key up: {key}")

    def capture_inputs(self, duration, filePath):
        def stop_listener():
            listener.stop()
            print("Capture thread ended.")
            with open(filePath, 'w') as file:
                json.dump(self.currentActions, file)
            self.currentActions = []
            self.finished.emit()  # Emit finished signal when capture completes

        self.started.emit()  # Emit started signal when capture begins

        listener = keyboard.Listener(
            on_press=self.keyPressed,
            on_release=self.keyReleased
        )
        listener.start()

        timer = threading.Timer(duration, stop_listener)
        timer.start()

        listener.join()

    def replay_inputs(self):
        with open('actions.json', 'r') as file:
            self.currentActions = json.load(file)

        for action in self.currentActions:
            device, details = action
            if device == "keyboard":
                if details in self.specialkey_mapping:
                    pyautogui.press(self.specialkey_mapping[details])
                else:
                    pyautogui.press(details)
