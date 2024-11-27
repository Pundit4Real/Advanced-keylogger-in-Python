import os
import time
from PIL import ImageGrab

# Folder path for screenshots
screenshot_folder = os.path.join(os.environ['appdata'], "KL")

# Function to capture a single screenshot
def capture_screenshot():
    timestamp = int(time.time())
    screenshot_filename = f"screenshot_{timestamp}.png"
    img = ImageGrab.grab()
    img_path = os.path.join(screenshot_folder, screenshot_filename)
    img.save(img_path, "PNG")
    return img_path

# Capture screenshots periodically
def periodic_screenshot_capture(interval=1):
    while True:
        capture_screenshot()
        time.sleep(interval)  # Interval in seconds

if __name__ == "__main__":
    periodic_screenshot_capture()
