import socket
import keyboard
import time

HOST = "raspberrypi.local"
PORT = 8888  

class Kiosk:
    def __init__(self):
        self.card_text = ''
        self.no_text = ["enter", "shift", "space"]
        keyboard.on_press(self.key_press)
        keyboard.add_hotkey('enter', self.send_text_interruption)
        while True:
            time.sleep(1)

    def key_press(self, key):
        if key.name not in self.no_text:
            self.card_text += key.name
        if key.name == "space":
            self.card_text += " "
        if key.name == "%":
            self.card_text = ''

    def send_text_interruption(self):
        # format string before sending
        unwanted_chars = ["?", "/", "5"]
        text_to_send = self.card_text
        for item in unwanted_chars:
            text_to_send = text_to_send.replace(item, "")
        text_to_send = text_to_send.upper()
        
        print("Sending card data to display:",text_to_send)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(str.encode(text_to_send))
                data = s.recv(1024)
                self.card_text = ''
        except Exception as e: 
            print(e)
            print("Error sending card data to display")

if __name__ == "__main__":
    print("Starting kiosk daemon")
    kiosk = Kiosk()
