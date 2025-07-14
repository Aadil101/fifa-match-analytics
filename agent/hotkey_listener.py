from pynput import keyboard
from screenshot_capture import screenshot_specific_window, get_foreground_window_title

class HotkeyListener:
    def __init__(self, on_screenshot_token=None):
        self.pressed = set()
        self.combinations = [ # TODO: Allow customization of hot key
            {
                "keys": [
                    {keyboard.Key.cmd, keyboard.KeyCode(char="o")},
                    {keyboard.Key.cmd, keyboard.KeyCode(char="O")},
                ],
            },
        ]
        self.listener = None
        self.on_screenshot_token = on_screenshot_token

    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
    
    def stop(self):
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
        self.pressed.add(key)
        for c in self.combinations:
            for keys in c["keys"]:
                if keys.issubset(self.pressed):
                    window_title = get_foreground_window_title()
                    screenshot_path = 'output/window_screenshot.png' # TODO: Use temporary directory
                    screenshot_specific_window(window_title, screenshot_path)
                    if self.on_screenshot_token:
                        self.on_screenshot_token(screenshot_path)


    def on_release(self, key):
        if key in self.pressed:
            self.pressed.remove(key)
