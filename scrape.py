import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

SITE_KEY = '6LezG3omAAAAAGrXICTuXz0ueeMFIodySqJDboLT'
api_key = '147f2a193a2db639a49c64a00ed66cd5'
website_url = 'https://stars.ylopo.com/auth'
website_redirect_url = 'https://stars.ylopo.com/auth?redirect=/lead-detail/7675efb9-35d7-460f-b017-245e4d76e3a7'
dashboard_url = 'https://stars.ylopo.com/lead-detail/7675efb9-35d7-460f-b017-245e4d76e3a7'

# Create Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_experimental_option(
    "prefs", {
        # block image loading
        "profile.managed_default_content_settings.images": 2,
    }
)

def run_scrape():
    driver = webdriver.Chrome(options=options)
    driver.get(website_redirect_url)

    # input email in email field
    email_elem = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
    email_elem.clear()
    email_elem.send_keys("thenewmute21@gmail.com")

    # input passowrd in password field
    password_elem = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
    password_elem.clear()
    password_elem.send_keys("Ylopo*12")


    # by-pass recapcha
    print("Solving Captcha")
    solver = TwoCaptcha(api_key)
    response = solver.recaptcha(sitekey=SITE_KEY, url=website_url)
    code = response['code']
    print(f"Successfully solved the Captcha. The solve code is {code}")

    driver.implicitly_wait(20)

    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
    recaptcha_text_area = driver.find_element(By.ID, "g-recaptcha-response")
    recaptcha_text_area.clear()
    recaptcha_text_area.send_keys(code)

    # click the login button
    login_btn = driver.find_element(By.CLASS_NAME, "pb-button")
    login_btn.send_keys(Keys.RETURN)


    # Wait for the redirect to a new page after successful login
    wait = WebDriverWait(driver, 10).until(
        EC.url_to_be(dashboard_url)
    )

    # click on link button
    link_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/table/tbody/tr/td[9]/button')
    link_btn.click()

    # Wait for a short while to allow the copying to happen
    time.sleep(1)

    # Retrieve the copied text from the clipboard using pyperclip
    copied_text = pyperclip.paste()
    print("Copied link:", copied_text)

    driver.close()

    return copied_text