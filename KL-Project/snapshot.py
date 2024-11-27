import os
from PIL import ImageGrab
import time


screenshot_folder = os.path.join(os.environ['appdata'], "SS")


if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

def capture_screenshot():

    img = ImageGrab.grab()
    
    # Get the current timestamp to create a unique filename
    timestamp = str(int(time.time()))
    img_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
    
    
    img.save(img_path, "PNG")
    print(f"Screenshot saved as {img_path}")

def periodic_screenshot_capture():
    while True:
        capture_screenshot()
        time.sleep(10)  # Capture a screenshot every 10 seconds

if __name__ == "__main__":
    periodic_screenshot_capture()
