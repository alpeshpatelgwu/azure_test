from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to Establish Monogo Connection
mongo = PyMongo(app, uri="mongodb+srv://gwu_data_class:gwu_data@mission-to-mars-nja70.azure.mongodb.net/test?retryWrites=true")



#Route to render index.html template using data from Mongo

@app.route("/")
def home():

    #Find one record of data from mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return data found to template (index.html) and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger scraping the mars data function

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mongo.db.mars_data
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_featured_img()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemisphere()
    #mars_data.update({}, mars_data, upsert=True)
    
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'

if __name__ == "__main__":
    app.run(debug=True)
