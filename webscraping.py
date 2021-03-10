from selenium import webdriver
from bs4 import BeautifulSoup

def get_vod_channel(video_id):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(r"E:\Google\Chrome\chromedriver.exe", options=options)
    URL = f"https://www.twitch.tv/videos/{video_id}"
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    channel_name = soup.find('h1', class_ = 'tw-c-text-base tw-font-size-4 tw-line-height-heading tw-semibold tw-title').contents[0]
    return channel_name