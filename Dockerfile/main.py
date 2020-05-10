from selenium import webdriver
from flask import Flask, send_file
import time
import chromedriver_binary  # Adds chromedriver binary to path

app = Flask(__name__)

# The following options are required to make headless Chrome
# work in a Docker container
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--ignore-certificate-errors')

fish_website = 'http://99.189.176.224'

@app.route('/')
def home_page():
    return 'Welcome to Dad\'s Fish Tank API'

def push_button(action):
    with webdriver.Chrome(chrome_options=chrome_options) as browser:
        browser.get(fish_website)
        # give time for page to load.  5 to 7 seconds is minimum. Doing 10 to be safe
        time.sleep(10)
        # click video first to display buttons
        video = browser.find_element_by_xpath('//img[@class="camera"]')
        video.click()
        # determine the action to execute
        if action == "on":
            xpath = '//div[@class="button icon camera-action-button mouse-effect light-on" and @title="turn light on"]'
        elif action == "feed":
            xpath = '//div[@class="button icon camera-action-button mouse-effect preset preset1" and @title="preset 1"]'
        else:  # divert any other actions to safe action of light off
            xpath = '//div[@class="button icon camera-action-button mouse-effect light-off" and @title="turn light off"]'
        # click the button to initiate action
        button = browser.find_element_by_xpath(xpath)
        button.click()
        return ("", 200, None)

# API to turn light on
@app.route('/on')
def light_on():
    return push_button("on")

# API to turn light off
@app.route('/off')
def light_off():
    return push_button("off")

# API to feed fish
@app.route('/feed')
def feed_fish():
    return push_button("feed")