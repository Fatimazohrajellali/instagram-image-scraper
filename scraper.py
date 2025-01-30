# Imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget

# Specify the path to chromedriver.exe
from selenium.webdriver.chrome.service import Service

driver_path = "E:\\driver\\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open Instagram
driver.get("http://www.instagram.com")

# Login to Instagram
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

username.clear()
username.send_keys("ton_nom_utilisateur")
password.clear()
password.send_keys("ton_mot_de_passe")

# Click login button
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# Click "Not now" button to skip saving login info
not_now = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Plus tard")]'))).click()

# Search for a hashtag
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Saisie de la recherche']")))
searchbox.clear()

# Define the hashtag to search
keyword = "#football"
searchbox.send_keys(keyword)

# Wait for the search results
time.sleep(2)

# Click on the hashtag result
hashtag_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{keyword[1:]}')]")))
hashtag_link.click()

# Wait for the page to load
time.sleep(3)

# 📌 **Download images from the hashtag page**
dest_loc = r'C:\Users\INKA\Desktop\testscrap'  

# Create the directory if it doesn't exist
os.makedirs(dest_loc, exist_ok=True)

import time

time.sleep(5)  # Attendre 5 secondes pour charger les images
images = driver.find_elements(By.XPATH, "//img[contains(@class, 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3')]")

if not images:
    print(" Aucune image trouvée ! Vérifiez que l'élément XPath est correct.")
else:
    print(f" {len(images)} images trouvées, extraction en cours...")


# Store images
my_images = set()

while True:
    for image in images:
        source = image.get_attribute('src')
        my_images.add(source)

    # Scroll down to load more images
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Get newly loaded images
    images = driver.find_elements(By.XPATH, "//img[@class='_aagw']")
    
    # Stop when we have enough images
    if len(my_images) > 10:
        break

# **Download the images**
for image in my_images:
    wget.download(image, dest_loc)

print(f"{len(my_images)} images downloaded successfully to {dest_loc}")
