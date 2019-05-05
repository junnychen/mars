from splinter import Browser
from bs4 import BeautifulSoup

def scrape():
    browser = Browser("chrome", executable_path = "/usr/local/bin/chromedriver", headless=True)

    scraped_data = {}

    # scrape latest news

    browser.visit('https://mars.nasa.gov/news/')
    news_soup = BeautifulSoup(browser.html, 'html.parser')

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    slide = news_soup.select_one('ul.item_list .slide')
    news_title = slide.find("div", class_='content_title').text
    news_p = slide.find("div", class_='article_teaser_body').text

    scraped_data['mars_news'] = {
        'title': news_title,
        'paragraph': news_p
    }

    # scrape featured image 

    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    full_img = browser.find_link_by_partial_text('FULL IMAGE')
    full_img.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    img_soup = BeautifulSoup(browser.html, 'html.parser')
    main_image = img_soup.find("img", class_="main_image")
    featured_image_url = 'https://www.jpl.nasa.gov' + main_image.get('src')

    scraped_data['featured_image_url'] = featured_image_url

    # done

    browser.quit()

    return scraped_data
