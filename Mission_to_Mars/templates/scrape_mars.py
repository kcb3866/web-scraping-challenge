from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import pandas as pd

def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    title_text, paragraph_text = mars_news(browser)

    # Run scraping functions and store result in dictionary
    data = {
        "news_title": title_text,
        "news_paragraph": paragraph_text,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # stop browser
    browser.quit()
    return data

def mars_news(browser):
    url = 'https:/redplanetscience.com'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    try:
        results = soup.select_one('div.list_text')
        title_text = results.find('div', class_= "content_title").get_text()
        paragraph_text = results.find('div', class_= 'article_teaser_body').get_text()

    
    browser.quit()
    return results, title_text, paragraph_text

def featured_image():
    featured_image_url = 'https://spaceimages-mars.com/'

    browser.visit(featured_image_url)

    full_button_element = browser.find_by_tag('button')[1]

    html = browser.html
    img_soup = bs(html, "html.parser")

    img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')

    img_url = f"https://spaceimages-mars.com/{img_url_rel}"

    browser.quit()
    return img_url

def facts():
    mars_df= pd.read_html('https://space-facts.com/mars/')[0]

    mars_df.columns= ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    html_table = mars_df.to_html('table.html')

    return html_table

def hemispheres():
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')
    print(links)

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        print(sample_elem)
        hemisphere['img_url'] = sample_elem['href']
        
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        
        # Finally, we navigate backwards
        browser.back()

    browser.quit()

    return hemisphere_image_urls, hemisphere