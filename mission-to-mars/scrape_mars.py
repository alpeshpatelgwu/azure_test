import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Define Mission to Mars Dictionary to be imported into Mongo
mars_data = {}

def scrape_mars_news():
    browser = init_browser()

    # Visit NASA Mars News Page 
    url_nasa = 'https://mars.nasa.gov/news'
    browser.visit(url_nasa)

    time.sleep(1)

    # Scrape page into Soup
    html_nasa = browser.html
    soup = bs(html_nasa, "html.parser")

    # Find the latest date, news title, and teaser
    news_date = soup.body.find('div', class_='list_date').text
    news_title = soup.body.find('div', class_='content_title').find('a').text
    news_teaser = soup.find('div', class_='article_teaser_body').text

    # Create a dictionary for Mars News
    mars_data['news_date'] = news_date
    mars_data['news_title'] = news_title
    mars_data['news_teaser'] = news_teaser

    browser.quit()

    return mars_data



def scrape_featured_img():
    browser = init_browser()

    # JPL Mars Space Images URL Definition
    url_jpl_featured_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl_featured_img)

    # Scrape JPL Mars page into Soup
    html_jpl = browser.html
    soup = bs(html_jpl, "html.parser")

    # Find the featured image url
    featured_image_url = soup.find('article')['style']
    featured_image_url.find("('")
    featured_image_url.find("')")
    img_link_parsed = featured_image_url[21+len("('"):75]

    #Combine the main url and featured image url 
    url_jpl = 'https://www.jpl.nasa.gov'
    url_img_featured = url_jpl + img_link_parsed

    # Create dictionary for featured iamge
    mars_data['url_img_featured'] = url_img_featured

    browser.quit()

    return mars_data





def scrape_mars_weather():

    browser = init_browser()

    # Mars Weather URL Definition
    url_mweather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mweather)

    # Scrape Mars Weather page into Soup
    html_marsweather = browser.html
    soup = bs(html_marsweather, "html.parser") 

    # Find the current tweets
    mars_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Loop through to find the weather related tweet
    mars_weather = []
    for tweet in mars_tweets:
        weather_tweet = tweet.find('p').text
        #if 'sol' and 'pressure' in weather_tweet:
        if 'sol' in weather_tweet:
            mars_weather.append(weather_tweet)
            print(weather_tweet)
        else:
            pass
    mars_weather_tweet = mars_weather[0]

    # Create dictionary for mars weather
    mars_data['mars_weather_tweet'] = mars_weather_tweet

    browser.quit()

    return mars_data
        

def scrape_mars_facts():
        browser = init_browser()


        # Mars Facts URL Definition
        url_mfacts = 'https://space-facts.com/mars/'
        browser.visit(url_mfacts)

        # Scrape the website to get the facts
        mars_facts = pd.read_html(url_mfacts)

        # After looking through the facts, index 0 is where our information
        # is located.  Put that into a data frame
        mars_df = mars_facts[0]
        mars_df.columns = ['Description', 'Unit Values']
        mars_df.set_index('Description', inplace=True)

        # Convert the data frame into a table
        mars_html_table = mars_df.to_html()
        mars_html_table.replace('\n', '')
        mars_df.to_html('mars_table.html')

        # Create dictionary for mars facts
        mars_data['mars_facts'] = mars_html_table

        browser.quit()
        
        return mars_data


def scrape_mars_hemisphere():
    
    browser = init_browser()

    # Mars Hemispheres URL Definition
    url_mhemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_mhemispheres)

    # Scrape Mars Hemispheres into Soup
    html_mhemispheres = browser.html
    soup = bs(html_mhemispheres, 'html.parser')

    # Scrape the page using BS4 to find information on hemispheres
    soup.body.find_all('div', class_='item')
    items = soup.body.find_all('div', class_='item')

    # Store the main USGS Astrogeology link
    url_main = 'https://astrogeology.usgs.gov'

    # Create a list to hold Hemisphere title and image 
    hemisphere_img_url = []

    # Run through a loop to get to all the pages and get image link/title
    for i in items:
        title = i.find('h3').text
        url_visit = i.find('div', class_='description').find('a')['href']

        # Visit the site for each hemisphere
        browser.visit(url_main + url_visit)

        # HTML Object of individual hemisphere information website 
        hemisphere_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( hemisphere_html, 'html.parser')
        
        # Capture the link of the full size image 
        full_img_url = url_main + soup.find('img', class_='wide-image')['src']
        
        # Append information into a list of dictionaries 
        hemisphere_img_url.append({"title" : title, "img_url" : full_img_url})
    
    #Print the consolidated list of images in Hemisphere
    hemisphere_img_url

    # Create dictionary for Mars hemispheres
    mars_data['hemi_img_url'] = hemisphere_img_url

    browser.quit()

    return mars_data

