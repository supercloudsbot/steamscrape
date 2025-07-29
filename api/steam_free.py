from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/steam/free")
def get_steam_free():
    url = "https://store.steampowered.com/search/?maxprice=free&specials=1&ndl=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    games = []
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("a.search_result_row")[:5]
    for item in items:
        title = item.select_one(".title").text.strip()
        link = item["href"]
        appid = link.split("/app/")[1].split("/")[0]
        image = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
        games.append({"title": title, "url": link, "image": image, "price": "Free"})
    return {"games": games}
