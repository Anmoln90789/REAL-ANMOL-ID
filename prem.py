import requests
import time
import sys
import os
import threading
from platform import system
import http.server
import socketserver

# कस्टम HTTP हैंडलर
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

# HTTP सर्वर शुरू करें
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# टर्मिनल स्क्रीन साफ़ करें
def clear_screen():
    os.system('cls' if system() == 'Windows' else 'clear')

# विभाजक रेखा प्रिंट करें
def print_separator():
    print('-' * 50)

# संदेश भेजने की लॉजिक
def send_messages():
    try:
        # पासवर्ड लोड करें
        with open('password.txt', 'r') as file:
            correct_password = file.read().strip()

        # पासवर्ड सत्यापन
        entered_password = input("Enter the password: ").strip()
        if entered_password != correct_password:
            print('[-] WRONG PASSWORD. TRY AGAIN.')
            sys.exit()

        # टोकन लोड करें
        with open('token.txt', 'r') as file:
            tokens = [token.strip() for token in file.readlines()]
        if not tokens:
            print("[-] No tokens found in 'token.txt'.")
            sys.exit()

        # बातचीत आईडी लोड करें
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        # संदेश लोड करें
        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()
        with open(text_file_path, 'r') as file:
            messages = [msg.strip() for msg in file.readlines()]

        # हेटर का नाम लोड करें
        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()

        # गति लोड करें
        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())

        # HTTP हेडर्स
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0)',
            'Accept': '*/*'
        }

        # संदेश भेजना शुरू करें
        clear_screen()
        print_separator()
        print("[+] STARTING MESSAGE SENDING PROCESS")
        print_separator()

        for index, message in enumerate(messages):
            token = tokens[index % len(tokens)]  # टोकन घुमाएँ
            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
            parameters = {'access_token': token, 'message': f"{haters_name} {message}"}

            try:
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    print(f"[+] MESSAGE {index + 1} SENT: {message}")
                    print(f"  - Time: {current_time}")
                else:
                    print(f"[x] FAILED TO SEND MESSAGE {index + 1}: {message}")
                    print(f"  - Error: {response.text}")
            except Exception as e:
                print(f"[!] ERROR SENDING MESSAGE {index + 1}: {e}")

            print_separator()
            time.sleep(speed)

        print("[+] ALL MESSAGES SENT SUCCESSFULLY.")

    except FileNotFoundError as e:
        print(f"[-] File not found: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

# मुख्य फ़ंक्शन
def main():
    # HTTP सर्वर को एक अलग थ्रेड में शुरू करें
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # संदेश भेजना शुरू करें
    send_messages()

if __name__ == '__main__':
    main()
