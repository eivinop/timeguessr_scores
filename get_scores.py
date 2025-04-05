import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import os
from dotenv import load_dotenv

load_dotenv('secrets.env')

# URL of the website
url = "https://timeguessr.com/finalscoredaily"  

# Login URL and credentials
login_url = "https://timeguessr.com/login"  

credentials = {
    'username': os.getenv('timeguessr_username'), 
    'password': os.getenv('timeguessr_password')   
}

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-notifications')

service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Log in using Selenium
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(credentials['username'])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(credentials['password'], Keys.RETURN)



    driver.get("https://timeguessr.com")  

    # Wait for the cookies consent popup to appear and click the "Consent" button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Daily'))).click()
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'fc-button.fc-cta-consent.fc-primary-button')) 
        )
        cookies_button.click()
        print("Cookies consent popup dismissed.")
    except Exception as e:
        print(f"No cookies consent popup found or failed to dismiss: {e}")

    # Play a round of the game
    for i in range(5):


        map = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mk-map-node-element')))
        map.click()
        # Wait for the "Make guess" button to be clickable and click it
        time.sleep(5)
        make_guess_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'makeGuess')))
        make_guess_button.click()
        print("Guess made.")

        # Wait for the next round to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nextRound'))).click()
        time.sleep(1)



    # Wait for the "leaderboard" button to be clickable and click it
    leaderboard_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'viewStatsButton')))  # Replace with the actual button ID
    leaderboard_button.click()
    print("Leaderboard button clicked.")
    time.sleep(5)

    # Get the page source after the leaderboard loads
    html_content = driver.page_source

finally:
    driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the leaderboard table
leaderboard_table = soup.find('table', id='myTable')

# Extract the rows from the table body
rows = leaderboard_table.find('tbody').find_all('tr')

# Parse the leaderboard data
leaderboard = []
for row in rows:
    rank = row.find('td', class_='cell-number').text.strip()
    username = row.find('td', class_='username').text.strip()
    score = row.find('td', class_='score').text.strip()
    leaderboard.append({'rank': rank, 'username': username, 'score': score})

# Print the leaderboard
for entry in leaderboard:
    print(f"Rank: {entry['rank']}, Username: {entry['username']}, Score: {entry['score']}")