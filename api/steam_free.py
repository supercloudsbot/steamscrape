from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/steam/free")
def get_steam_free():
    url = "https://store.steampowered.com/search/?maxprice=free&specials=1&ndl=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    games = []

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("a.search_result_row")

        for item in items[:5]:
            title = item.select_one(".title").text.strip()
            link = item["href"]
            appid = link.split("/app/")[1].split("/")[0]
            image = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"

            games.append({
                "title": title,
                "url": link,
                "image": image,
                "price": "Free",
                "platform": "Steam"
            })

        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)})
