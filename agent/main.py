from hotkey_listener import HotkeyListener
from ocr_runner import OCRRunner
import logging
from PIL import Image
import pystray
import queue
import signal
import threading
import time

# Set up logging to file since we won't have console
logging.basicConfig(
    filename='fifa_analytics.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Agent:
    def __init__(self):
        self.screenshot_queue = queue.Queue()                                   # Initialize a queue to handle screenshot processing
        self.listener = HotkeyListener(                                         # Initialize the HotkeyListener to capture screenshots
            on_screenshot_token=lambda path: self.screenshot_queue.put(path)
        )
        self.ocr_runner = OCRRunner()                                           # Initialize the OCRRunner to process screenshots
        self.icon = self.create_tray_icon()                                     # Create the system tray icon
        self.running = True                                                     # Initialize the running flag
        
    def process_queue(self):
        while self.running:
            try:
                screenshot_path = self.screenshot_queue.get(timeout=1.0)        # 1 second timeout
                try:
                    # TODO: Replace hardcoded image type with appropriate image type
                    result = self.ocr_runner.process_screenshot('matchfacts-summary', screenshot_path)
                    # TODO: Handle result (log success, notify user etc)
                finally:
                    self.screenshot_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error processing screenshot: {e}")

    def create_tray_icon(self):
        # Create system tray icon
        image = Image.open("assets/soccer_ball_flat.png")
        menu = pystray.Menu(
            pystray.MenuItem("Status: Active", self.toggle_active),
            pystray.MenuItem("Open Dashboard", self.open_dashboard),
            pystray.MenuItem("Settings", self.open_settings),
            pystray.MenuItem("Exit", self.signal_handler)
        )
        return pystray.Icon("FIFA Match Analytics", image, "FIFA Match Analytics", menu)
    
    def toggle_active(self):
        # Toggle hotkey listening
        pass
        
    def open_dashboard(self):
        # Open web dashboard in browser
        import webbrowser
        webbrowser.open('http://localhost:8000')
        
    def open_settings(self):
        # Open settings window
        pass
        
    def signal_handler(self):
        self.running = False
        
    def run(self):
        logging.info("Agent starting...")

        # Set up signal handlers
        signal.signal(signal.SIGINT, lambda s, f: self.signal_handler())
        signal.signal(signal.SIGTERM, lambda s, f: self.signal_handler())

        # Start the queue processor thread
        queue_thread = threading.Thread(daemon=True, target=self.process_queue)
        queue_thread.start()

        # Start the listener and icon in non-blocking ways
        self.listener.start()
        self.icon.run_detached()

        # Keep the main thread running with a control flag
        while self.running:
            time.sleep(1)

        # Clean up
        logging.info("Agent stopping...")
        self.icon.stop()
        self.listener.stop()

if __name__ == '__main__':
    agent = Agent()
    agent.run()