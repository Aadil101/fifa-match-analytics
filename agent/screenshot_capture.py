from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
import pygetwindow as gw
import pyautogui

def get_foreground_window_title() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    return buf.value if buf.value else None

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

        # Get the first matching window
        target_window = target_window[0]

        # Get window coordinates
        left, top = target_window.left, target_window.top
        width, height = target_window.width, target_window.height
        right, bottom = left + width, top + height

        # Capture the entire screen
        screenshot = pyautogui.screenshot()

        # Crop the screenshot to the target window's region
        cropped_screenshot = screenshot.crop((left, top, right, bottom))

        # Save the cropped screenshot
        cropped_screenshot.save(output_filename)
        print(f"Screenshot of '{window_title}' saved as '{output_filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")