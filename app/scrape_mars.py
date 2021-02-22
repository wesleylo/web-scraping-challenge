# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/node_modules/chromedriver/bin/chromedriver'}
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    # URL of page to scrape
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Convert html to soup
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_data = {}

    # collect latest news title
    news_title = soup.select_one('div.content_title a').text #!
    mars_data['news_title'] = news_title

    # find the paragraph text of the lastest news article
    results = soup.find("div", class_="list_text") # find div
    news_paragraph = results.find("div", class_="article_teaser_body").text #!
    mars_data['news_paragraph'] = news_paragraph

    ## JPL Feature Image ##

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16837_hires.jpg'
    browser.visit(url)

    # Parse the resulting html with soup and find image url
    html = browser.html
    img_soup = bs(html, 'html.parser')
    img_src = img_soup.select_one('img').get("src") #!
    mars_data['img_src'] = img_src



    ## Mars Facts ##

    mars_facts_df = pd.read_html('http://space-facts.com/mars/')
    mars_facts_df = mars_facts_df[0] # read table for mars

    mars_facts_df.columns = ["Fact", "Mars"]
    mars_facts_df.set_index("Fact", inplace=True) #!
    mars_data['mars_facts'] = mars_facts_df.to_html(classes="dataframe, table, table-bordered, table-hover")

    ## Hemispheres ##

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # get list of links to all of the enhanced hemisphere pages
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_urls=[]

    hemi_links = browser.find_by_tag("h3") # enhanced links


    for i in range(len(hemi_links)):
        # hemisphere = {}
        
        hem_title = browser.find_by_css("h3")[i].text
        
        browser.find_by_css("h3")[i].click()
        
        image = browser.links.find_by_text('Sample').first
        hem_img_url = image["href"]

        hem_dict = {
            'title:': hem_title,
            'img_url': hem_img_url
        }
        
        hemisphere_urls.append(hem_dict) #!
        mars_data['hemisphere_urls'] = hemisphere_urls

        browser.back()



    # Stop webdriver and return data
    browser.quit()
    return mars_data



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape())
