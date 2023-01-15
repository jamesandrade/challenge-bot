import os
import re
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', "https://webscraper.io")
payload = []
def makepayload(i):
    title = i.find('a', {'class': 'title'}).text
    title = title.replace("...", "")
    if "Lenovo" in title:
        price = i.find('h4', {'class': 'pull-right price'}).text
        price = float(price.replace("$", ""))
        description = i.find('p', {'class': 'description'}).text
        reviews = i.find('p', {'class': 'pull-right'}).text
        reviews = reviews.replace(" reviews", "")
        img = i.find('img', {'class': 'img-responsive'}).get('src')
        rating = str(i.find('div', {'class': 'ratings'}).find_all('p'))
        rating = re.search('data-rating="(.+?)"', rating)
        if rating:
            rating = rating.group(1)
        else:
            rating = 0

        payload.append({
            "title": title,
            "price": price,
            "description": description,
            "reviews": reviews,
            "img": URL+img,
            "rating": rating
        })

def sort(payload):
    newlist = sorted(payload, key=lambda k: k['price'])
    return newlist

app = Flask(__name__)
@app.route("/")
def summary():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        page = navegador.new_page()
        page.goto(f"{URL}/test-sites/e-commerce/allinone/computers/laptops")
        soup = BeautifulSoup(str(page.content()), 'html.parser')
        for i in soup.find_all('div', {'class': 'thumbnail'}):
            makepayload(i)
    newPayload = sort(payload)
    return jsonify(newPayload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)