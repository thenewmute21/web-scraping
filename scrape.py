from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

SITE_KEY = '6LezG3omAAAAAGrXICTuXz0ueeMFIodySqJDboLT'
api_key = '147f2a193a2db639a49c64a00ed66cd5'
base_url = 'https://stars.ylopo.com/auth'

# Create Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_experimental_option(
    "prefs", {
        # block image loading
        "profile.managed_default_content_settings.images": 2,
    }
)

def run_scrape(email, password, website_url):
    dashboard_url = base_url + urlparse(website_url).query.split('=')[1] #construct base url

    driver = webdriver.Chrome(options=options)
    driver.get(website_url)

    # input email in email field
    email_elem = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
    email_elem.clear()
    email_elem.send_keys(email)

    # input passowrd in password field
    password_elem = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
    password_elem.clear()
    password_elem.send_keys(password)


    # by-pass recapcha
    print("Solving Captcha")
    solver = TwoCaptcha(api_key)
    response = solver.recaptcha(sitekey=SITE_KEY, url=base_url)
    code = response['code']
    print(f"Successfully solved the Captcha. The solve code is {code}")

    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
    recaptcha_text_area = driver.find_element(By.ID, "g-recaptcha-response")
    recaptcha_text_area.clear()
    recaptcha_text_area.send_keys(code)

    # click the login button
    login_btn = driver.find_element(By.CLASS_NAME, "pb-button")
    login_btn.send_keys(Keys.RETURN)
    print('successfully logged in')


    # Wait for the redirect to a new page after successful login
    wait = WebDriverWait(driver, 10).until(
        EC.url_to_be(dashboard_url)
    )

    # Retrieve the copied text from the clipboard using pyperclip

    # Execute JavaScript to send the request from the webpage and store the copied link in a variable
    copied_link_script = """
    return fetch("https://stars.ylopo.com/api/1.0/lead/46706799/encryptedLink?personId=46706799&runSearch=true&savedSearchId=55891023")
        .then(response => response.json())
        .then(data => data.shortLink)
        .catch(error => console.error('Error:', error));
    """
    copied_link = driver.execute_script("return (function() { " + copied_link_script + " })()")

    print("Copied link:", copied_link)

    driver.close()

    return copied_link