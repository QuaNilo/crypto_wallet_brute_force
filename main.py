import random
import string

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def save_recovery_seed(word):
    try:
        is_cracked = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div[1]/p[2]')
        if is_cracked.is_displayed():
            time.sleep(1)
            with open("recovery_seed.txt", "w", encoding="utf-8") as f:
                for word in range(1, 24):
                    word_field = driver.find_element(By.XPATH,
                                                     f"/html/body/div[2]/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div[{word}]/p[2]")
                    print(word_field.text)
                    f.write(f"{word_field.text}\n")
            driver.close()
    except NoSuchElementException:
        print(f"Element is not present for word: {word}")

def generate_wordlist(num_words, min_length, max_length):
    wordlist = []

    special_chars = ""

    for _ in range(num_words):
        length = random.randint(min_length, max_length)
        word = ''.join(random.choices(string.ascii_lowercase + special_chars, k=length))

        # Ensure at least one uppercase letter and one special character
        word = list(word)
        word[random.randint(0, length - 1)] = random.choice(string.ascii_uppercase)
        index = random.randint(1,19)
        while index in [6,13]:
            index = random.randint(1,19)
        word[index] = str(random.randint(0,9))
        word[6] = "-"
        word[13] = "-"
        wordlist.append(''.join(word))

    return wordlist
print("Finding Wordlist ...")
try:
    with open('wordlist_temp.txt', 'r') as f:
        wordlist = f.read().splitlines()
except Exception as e:
    print(f"Generating wordlist...")
    wordlist = generate_wordlist(1000, 20, 20)
    with open("wordlist_temp.txt", "w", encoding="utf-8") as f:
        for word in wordlist:
            f.write(f"{word}\n")
    print(f"Generated wordlist...")

# extension_id = input("Extension ID : ").strip()
# google_chrome_path = input("Google Chrome Path : ").strip()
# extension_path = input("Extension Path : ").strip()
# user_data_dir = input("Chrome User Data : ").strip()
extension_id = "gafhhkghbfjjkeiendhlofajokpaflmk"
google_chrome_path = "/usr/bin/chromium"
extension_path = "~/.config/chromium/Default/Extensions/gafhhkghbfjjkeiendhlofajokpaflmk/1.17.2_0/"
user_data_dir = "/home/quanilo/.config/chromium"

# Setup Chrome options
chrome_options = Options()
chrome_options.binary_location = google_chrome_path
# **Headless Mode**
# chrome_options.add_argument('--headless')  # This will run Chrome in headless mode (no UI)
# chrome_options.add_argument('--disable-gpu')  # This is needed for some environments to run headlessly
# chrome_options.add_argument('--no-sandbox')  # Required in some environments, like Docker or CI servers

chrome_options.add_argument(f'--user-data-dir={user_data_dir}')  # Specify the User Data directory
chrome_options.add_argument(f'--profile-directory=Default')  # Specify the profile (use 'Default' or another profile name)
chrome_options.add_argument(f'--load-extension={extension_path}')



# Set up the WebDriver
print(f"Opening browser...")
driver = webdriver.Chrome(options=chrome_options)
print(f"Opened browser!")
# Open the Chrome extension URL
driver.get(f"chrome-extension://{extension_id}/app.html#/settings")
time.sleep(5)
print(f"Navigated to extension!")

# Find the button and click it (adjust the selector if needed)
try:
    print(f"Spamming recovery now...")
    button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[2]' )  # Replace with actual XPath
    button.click()
    time.sleep(3)
except Exception as e:
    print(f"Error finding or clicking button: {e}")


# Find the form input field (adjust selector)
input_field = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div/form/div/div/div/input')  # Replace with actual XPath

for word in wordlist:
    try:
        input_field.clear()  # Clear the input field before typing the new word
        input_field.send_keys(word)
        # Find and click the submit button (adjust the selector)
        submit_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div/div[3]/button')  # Replace with actual XPath
        submit_button.click()
        # time.sleep(0.05)
        save_recovery_seed(word)
    except Exception as e:
        save_recovery_seed(word)

    # Wait for form submission (adjust as needed)
input("Press Enter to close the browser...")
driver.close()