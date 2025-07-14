import os
import requests
import urllib.parse

class OCRRunner:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.api_str = 'api/v1' # TODO: Make this configurable

    def process_screenshot(self, image_type, image_path):
        image_path_encoded = urllib.parse.quote(os.path.abspath(image_path))

        # Send screenshot to backend service for OCR processing
        try:
            with open(image_path, 'rb') as image:
                response = requests.post(
                    f"{self.api_base_url}/{self.api_str}/ocr/{image_type}/{image_path_encoded}", 
                )
                return response.json()
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            return None