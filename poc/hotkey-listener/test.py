from pynput import keyboard
import subprocess

from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer

import pygetwindow as gw
import pyautogui
from PIL import ImageGrab

pressed = set()

COMBINATIONS = [
    {
        "keys": [
            {keyboard.Key.cmd, keyboard.KeyCode(char="o")},
            {keyboard.Key.cmd, keyboard.KeyCode(char="O")},
        ],
    },
]

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None
    
def screenshot_specific_window(window_title, output_filename="window_screenshot.png"):
    """
    Takes a screenshot of a specific window and saves it to a file.

    Args:
        window_title (str): The title of the window to capture.
        output_filename (str): The name of the file to save the screenshot.
    """
    try:
        target_window = gw.getWindowsWithTitle(window_title)
        if not target_window:
            print(f"Window with title '{window_title}' not found.")
            return

        target_window = target_window[0] # Get the first matching window

        # Get window coordinates
        left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height
        right = left + width
        bottom = top + height

        # Capture the entire screen
        screenshot = pyautogui.screenshot()

        # Crop the screenshot to the target window's region
        cropped_screenshot = screenshot.crop((left, top, right, bottom))

        # Save the cropped screenshot
        cropped_screenshot.save(output_filename)
        print(f"Screenshot of '{window_title}' saved as '{output_filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")

def on_press(key):
    pressed.add(key)
    print(pressed)
    for c in COMBINATIONS:
        for keys in c["keys"]:
            if keys.issubset(pressed):
                windowTitle = getForegroundWindowTitle()
                screenshot_specific_window(windowTitle, 'output/window_screenshot.png')

def on_release(key):
    if key in pressed:
        pressed.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
