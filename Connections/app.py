from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
from datetime import date

# Import the client
import sys
sys.path.insert(1, '../Client')
import client

# Driver path // Switch for mac/windows
#driver_path = "../chromedriver-mac-x64/chromedriver"
driver_path = "../chromedriver-win64/chromedriver.exe"

# Enable performance logging
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

# Set up Service
service = Service(executable_path=driver_path)

# Options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create chrome instance
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.nytimes.com/games/connections')

# Format today's date to get the json file
today = str(date.today())
url = "https://www.nytimes.com/svc/connections/v2/" + today + ".json"

# Get request to the url to get the json values for the current connections
categories = client.getConnectionsData(url)

# Wait until the page has loaded to click play
playButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="moment-btn-play"]'))
)
playButton.click()
print("Play button clicked")

# Now wait until the x can be clicked for the 
xButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'i[class="pz-icon pz-icon-close"]'))
)
xButton.click()
print("X Button clicked")

# Wait for everything to render appropriately
time.sleep(1)

# Loop through the categories and select each word accordingly
for category in categories:
    for word in category:
        selectorString = 'label[data-flip-id="'+ word + '"]'
        try:
            currWordCheckbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selectorString))
            )

            if not currWordCheckbox.is_selected():
                currWordCheckbox.click()
                print("Checked " + word)
            else:
                print("Already checked " + word)
        except Exception as e:
            print("Error:", e)
        
    # Then click the submit button
    submitButton = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="submit-btn"]')
    submitButton.click()
    # Wait until the animation is over
    time.sleep(2)

# Sleep to see what's going on
time.sleep(20)

# Quit the driver
driver.quit()