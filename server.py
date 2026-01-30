from flask import Flask
import threading
import time
from fetch_news import fetch_news

app = Flask(__name__)

def worker():
    while True:
        fetch_news()
        time.sleep(1800)  # 30 minutes

@app.route("/")
def health():
    return "India Pulse backend running"

if __name__ == "__main__":
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=10000)
