from flask import Flask, send_file
import os
import threading
import time
import requests

# Flask app initialization
app = Flask(__name__, static_folder='public')

# Serve the index.html file
@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, "index.html"))

# Function to ping the server
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
        time.sleep(sleep_time)
        try:
            response = requests.get('http://127.0.0.1:3000', timeout=10)  # Replace with your actual server URL
            print(f"Pinged server with response: {response.status_code}")
        except requests.RequestException as e:
            if isinstance(e, requests.Timeout):
                print("Couldn't connect to the site URL..!")
            else:
                print(f"Error occurred: {e}")

# Start the Flask server
if __name__ == "__main__":
    # Start pinging in a separate thread
    ping_thread = threading.Thread(target=ping_server, daemon=True)
    ping_thread.start()

    # Run Flask app
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
