from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

def get_random_proxy():
    try:
        response = requests.get("https://www.proxy-list.download/api/v1/get?type=http", timeout=5)
        proxies = response.text.strip().split("\r\n")
        selected = random.choice(proxies)
        return {
            "http": f"http://{selected}",
            "https": f"http://{selected}"
        }
    except Exception as e:
        print("Proxy fetch error:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    reel_url = None

    if request.method == "POST":
        reel_url = request.form.get("reel_url")
        proxy = get_random_proxy()

        if proxy and reel_url:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
                requests.head(reel_url, proxies=proxy, headers=headers, timeout=5)
                print(f"Proxy used: {proxy['http']}")
            except Exception as e:
                print("Proxy failed:", e)

    return render_template("index.html", reel_url=reel_url)

app.run(host='0.0.0.0', port=81)
