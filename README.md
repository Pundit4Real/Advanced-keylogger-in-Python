# **Keylogger and Data Collector Project**

A Python-based multi-threaded application for capturing system data, keystrokes, Wi-Fi passwords, screenshots, and clipboard content, then securely encrypting the collected information and optionally emailing it.

---

## **Features**
- **Keylogger**: Tracks all keystrokes and logs them into a file.
- **System Information**: Captures basic computer information such as system specs and OS details.
- **Wi-Fi Passwords**: Extracts stored Wi-Fi credentials from the system.
- **Clipboard Copying**: Collects current clipboard content.
- **Screenshot Capture**: Periodically takes screenshots of the screen.
- **Encryption**: Encrypts the collected data to ensure security.
- **Email Sending**: Sends all collected and encrypted data to a specified email address periodically.
- **Concurrent Execution**: Uses multi-threading for efficient operation and simultaneous task execution.

---

---

## **Setup and Installation**

### **1. Prerequisites**
Ensure you have the following installed:
- Python 3.9+
- `pip` (Python package manager)

### **2. Clone the Repository**
Clone the repository to your local system:

    git clone https://github.com/your-username/keylogger-data-collector.git
    cd keylogger-data-collector

### **3. Install Dependencies**
Install the required Python libraries listed in `requirements.txt`:

        pip install -r requirements.txt


### **4. Configure Email Settings**
Update the `send_email.py` file with your email credentials:

        email_address = "your-email@gmail.com"  
        email_password = "your-email-app-password"
        recipient_email = "recipient-email@gmail.com"

Note: Use an app-specific password for Gmail or ensure the email service allows less secure apps.

### **5. Run the Program**
Run the program using:

        python main.py

### **How It Works**

- **Keylogger**: Captures keystrokes and saves them in a file within a designated directory.
  
- **System Data Collection**:
  - Captures system information and saved Wi-Fi passwords.
  - Reads the clipboard's current content.
  
- **Screenshots**: Periodically captures screenshots and saves them to a designated folder.
  
- **Encryption**: Encrypts all collected files before sending them via email.
  
- **Email Sending**: Periodically sends the collected and encrypted data to the configured email address.


### **Modules and Components**

1. **data_collection.py**
   - Handles:
     - Capturing system information.
     - Running the keylogger.
     - Extracting Wi-Fi passwords.
     - Reading clipboard content.

2. **screenshot_capture.py**
   - Captures periodic screenshots and stores them in a folder.

3. **send_email.py**
   - Packages and sends data files to an email.
   - Detects network connectivity before attempting to send emails.
   - Queues unsent data for later delivery when connectivity is restored.

4. **cryptography/encrypt_and_decrypt.py**
   - Encrypts collected files before emailing them.
   - Decrypts files for local review (if needed).

