from flask import Flask, send_file
import os
import threading
import time
import requests

app = Flask(__name__)

# Serve the index.html file from the "public" directory
@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "public", "index.html"))

# Function to ping the server
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
        time.sleep(sleep_time)
        try:
            # Replace with your actual server URL
            response = requests.get('http://your_server_url_here', timeout=10)
            print(f"Pinged server with response: {response.status_code}")
        except requests.RequestException as e:
            if isinstance(e, requests.Timeout):
                print("Couldn't connect to the site URL..!")
            else:
                print(e)

# Start the Flask server
if __name__ == "__main__":
    # Start the ping function in a separate thread
    ping_thread = threading.Thread(target=ping_server)
    ping_thread.daemon = True
    ping_thread.start()

    # Start the Flask app
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
