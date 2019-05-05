from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/scrape")
def scrape():
    scraped_data = scrape_mars.scrape()
    mongo.db.scrapped.update({}, scraped_data, upsert=True)
    return "success! now go back to /"

@app.route("/")
def index():
    mars = mongo.db.scrapped.find_one()
    return render_template("index.html", news=mars["mars_news"], image=mars["featured_image_url"])

if __name__ == "__main__":
    app.run()
