from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase3"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return mars_data


if __name__ == "__main__":
    app.run()
