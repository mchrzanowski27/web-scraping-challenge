#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ##NASA Mars News
    
    #Visit Mars News page
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    #Get the lastest news title
    news_title = soup.find("div", class_="content_title").text

    #Get the latest news paragraph text
    news_p = soup.find("div", class_= "article_teaser_body").text

    ##JPL Mars Space Images - Featured Image

    #Visit Space Images page
    space_img_url = "https://spaceimages-mars.com/"
    browser.visit(space_img_url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    #Get URL for current featured image
    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = space_img_url + relative_image_path   

    ##Mars Facts

    #Visit Mars Facts page
    table_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(table_url)

    #Get the facts table
    facts_df = tables[0]

    #Convert the data to HTML
    html_table = facts_df.to_html(index = False, header = False)

    #Get rid of extra white space
    mars_facts_html = html_table.replace('\n', '')

    ##Mars Hemispheres

    #Visit Mars Hemispheres page
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    #Get hemisphere titles and image urls
    hemisphere_img_urls = []
    names = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]
    for name in names:
        browser.find_by_tag("a").links.find_by_partial_text(name).click()

        html = browser.html
        soup = BeautifulSoup(html, 'lxml')

        hemi_title = soup.find("h2", class_="title").text
        title = hemi_title.replace("Enhanced", "")

        img = soup.find("div", class_="downloads")
        image_url = img.find_all('a')[0]["href"]
        img_url = hemispheres_url + image_url
        
        hemisphere_img_urls.append({"Title": title, "Image_URL": img_url})
        
        browser.links.find_by_partial_text('Back').click()
        time.sleep(2)

    #Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html,
        "hemisphere_img_urls": hemisphere_img_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data