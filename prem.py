import requests
import time
import sys
import os
import threading
from platform import system
import http.server
import socketserver

# Custom HTTP Handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

# Start HTTP Server
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Clear terminal screen
def clear_screen():
    os.system('cls' if system() == 'Windows' else 'clear')

# Print separator line
def print_separator():
    print('-' * 50)

# Send Messages Logic
def send_messages():
    try:
        # Load passwords
        with open('password.txt', 'r') as file:
            correct_password = file.read().strip()

        # Password verification
        entered_password = input("Enter the password: ").strip()
        if entered_password != correct_password:
            print('[-] WRONG PASSWORD. TRY AGAIN.')
            sys.exit()

        # Load tokens
        with open('token.txt', 'r') as file:
            tokens = [token.strip() for token in file.readlines()]
        if not tokens:
            print("[-] No tokens found in 'token.txt'.")
            sys.exit()

        # Load conversation ID
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        # Load messages
        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()
        with open(text_file_path, 'r') as file:
            messages = [msg.strip() for msg in file.readlines()]

        # Load hater's name
        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()

        # Load speed
        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())

        # HTTP Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0)',
            'Accept': '*/*'
        }

        # Sending messages
        clear_screen()
        print_separator()
        print("[+] STARTING MESSAGE SENDING PROCESS")
        print_separator()

        for index, message in enumerate(messages):
            token = tokens[index % len(tokens)]  # Rotate tokens
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

# Main Function
def main():
    # Start HTTP server in a separate thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # Start sending messages
    send_messages()

if __name__ == '__main__':
    main()
