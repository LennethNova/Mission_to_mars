# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Set up master splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#This will be the function
# We're telling Python that we'll be using the browser variable we defined outside the function
def mars_news(browser):

# This will be inserted into a function
# Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


# HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    
#     slide_elem = news_soup.select_one('div.list_text')
#     slide_elem.find('div', class_='content_title')
# # Use the parent element to find the first `a` tag and save it as `news_title`
#     news_title = slide_elem.find('div', class_='content_title').get_text()
# # Use the parent element to find the paragraph text
#     news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None  
    # Return to indicate python that the function finished
    return news_title, news_p


# ### Featured Image
def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # img_url_rel

    except AttributeError:
        return None
    
   # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    return img_url

# ### Facts and BaseException
# scrape the entire table with Pandas
# By specifying an index of 0, we're telling Pandas to pull only
# the first table it encounters, or the first item in the list
def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

# Convert to html
# Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# Close browser
#browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


