import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading

# Custom HTTP handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

# Function to start the server
def execute_server():
    PORT = 4000
    try:
        with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
            print("Server running at http://localhost:{}".format(PORT))
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.shutdown()

# Function to validate password and send messages
def send_messages():
    # Read the password from file
    try:
        with open('password.txt', 'r') as file:
            saved_password = file.read().strip()
    except FileNotFoundError:
        print("[-] Password file not found!")
        sys.exit()

    # Validate the password with the online source
    try:
        online_password = requests.get('https://pastebin.com/raw/TcQPZaW8', timeout=10).text.strip()
        if saved_password != online_password:
            print('[-] WRONG PASSWORD! TRY AGAIN.')
            sys.exit()
    except requests.RequestException as e:
        print(f"[-] Failed to validate password online: {e}")
        sys.exit()

    # Load tokens from file
    try:
        with open('token.txt', 'r') as file:
            tokens = [token.strip() for token in file.readlines()]
    except FileNotFoundError:
        print("[-] Token file not found!")
        sys.exit()

    # Display the number of tokens
    print(f"[+] Number of tokens loaded: {len(tokens)}")

    # Load conversation ID from file (if needed)
    try:
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()
            print(f"[+] Conversation ID: {convo_id}")
    except FileNotFoundError:
        print("[!] Conversation file not found. Continuing without it.")

    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings()

    # Perform actions with tokens (Placeholder for actual logic)
    for token in tokens:
        print(f"[+] Using token: {token}")
        # Example request (replace with your logic)
        try:
            response = requests.get("https://example.com", headers={"Authorization": f"Bearer {token}"}, timeout=5)
            print(f"[+] Token Response: {response.status_code}")
        except requests.RequestException as e:
            print(f"[-] Error using token {token}: {e}")

# Start the server and message sending in separate threads
if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=execute_server, daemon=True)
    server_thread.start()

    # Start the send messages function
    send_messages()
