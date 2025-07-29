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
            try:
                title = item.select_one(".title").text.strip()
                link = item["href"]
                appid = link.split("/app/")[1].split("/")[0]
                image = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"

                # Ambil harga sebelum diskon jika tersedia
                price_tag = item.select_one(".search_price")
                if price_tag:
                    price_text = price_tag.get_text(strip=True).replace("Free", "").strip()
                    if price_text:
                        original_price = price_text.split('$')[0].strip()  # atau sesuaikan dengan mata uang lain
                    else:
                        original_price = "???"
                else:
                    original_price = "???"

                games.append({
                    "title": title,
                    "url": link,
                    "image": image,
                    "price": original_price if original_price else "???",
                    "platform": "Steam"
                })
            except Exception as e:
                print(f"⚠️ Error parsing game: {e}")
                continue

        return jsonify(games)

    except Exception as e:
        return jsonify({"error": str(e)})