import json
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file for Amazon credentials
load_dotenv()

# Define the driver path
driver_path = "C:/Users/shanm/Desktop/amazon/drivers/chromedriver.exe"

def create_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU
    options.add_argument('--log-level=3')  # Suppress logging
    options.add_argument('--silent')  # Run in silent mode

    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

def amazon_login(driver, phone, password):
    try:
        logging.info("Navigating to Amazon signin page")
        driver.get("https://amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        logging.info("Signin page loaded successfully")

        # Enter phone number
        phone_input = driver.find_element(By.ID, "ap_email")
        phone_input.send_keys(phone)
        logging.info("Entered phone number")
        
        # Click continue
        driver.find_element(By.ID, "continue").click()
        logging.info("Clicked continue")

        # Wait for password input to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        logging.info("Password input loaded successfully")

        # Enter password
        password_input = driver.find_element(By.ID, "ap_password")
        password_input.send_keys(password)
        logging.info("Entered password")

        # Click sign-in
        driver.find_element(By.ID, "signInSubmit").click()
        logging.info("Clicked sign in")

        # Check for CAPTCHA presence and switch to non-headless mode if detected
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-box"))
            )
            logging.info("CAPTCHA detected. Please solve the CAPTCHA manually.")
            # Save cookies to reuse in non-headless mode
            cookies = driver.get_cookies()
            driver.quit()

            # Open browser in non-headless mode for CAPTCHA solving
            driver = create_driver(headless=False)
            driver.get("https://www.amazon.in/ap/signin")
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()

            # Re-enter credentials in non-headless mode
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            phone_input = driver.find_element(By.ID, "ap_email")
            phone_input.send_keys(phone)
            driver.find_element(By.ID, "continue").click()

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_input = driver.find_element(By.ID, "ap_password")
            password_input.send_keys(password)
            driver.find_element(By.ID, "signInSubmit").click()

            input("Press Enter after solving the CAPTCHA and logging in manually...")

            # Save cookies again after CAPTCHA is solved
            cookies = driver.get_cookies()

            # Quit non-headless mode and switch back to headless mode
            driver.quit()
            driver = create_driver(headless=True)
            driver.get("https://www.amazon.in")
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()

        except:
            logging.info("No CAPTCHA detected")

        # Wait for successful login
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        )
        logging.info("Logged in successfully")
        return driver
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        driver.save_screenshot("login_error_screenshot.png")
        with open("login_error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise

def scrape_product_details(driver, product_column):
    soup = BeautifulSoup(product_column.get_attribute('innerHTML'), 'html.parser')
    products = soup.find_all('div', class_='zg-grid-general-faceout')
    product_details_list = []

    for product in products:
        try:
            # Extract product name
            name = product.find('div', {'class': '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1'}).get_text(strip=True)
        except AttributeError:
            name = 'N/A'

        try:
            # Extract product review
            review = product.find('span', {'class': 'a-icon-alt'}).get_text(strip=True)
        except AttributeError:
            review = 'N/A'

        try:
            # Extract product price
            price = product.find('span', {'class': '_cDEzb_p13n-sc-price_3mJ9Z'}).get_text(strip=True)
        except AttributeError:
            price = 'N/A'

        try:
            # Extract product link
            link = product.find('a', {'class': 'a-link-normal'})['href']
        except TypeError:
            link = 'N/A'

        product_details = {
            'Product Name and Description': name,
            'Review': review,
            'Price': price,
            'Product Link': f'https://www.amazon.in{link}' if link != 'N/A' else link
        }

        product_details_list.append(product_details)

    return product_details_list

def scrape_best_seller_products(driver, category_url):
    driver.get(category_url)

    try:
        logging.info(f"Navigating to best seller category: {category_url}")
        product_column = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "p13n-desktop-grid")))
        logging.info("Found the product column")

        product_details_list = scrape_product_details(driver, product_column)
        return product_details_list

    except Exception as e:
        logging.error(f"An error occurred while scraping best seller products: {e}")
        driver.save_screenshot("error_screenshot.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return []

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Data saved to {filename}")

def main():
    phone = os.getenv("PHONE")
    password = os.getenv("PASSWORD")
    
    if phone is None or password is None:
        logging.error("Phone or password environment variable is not set. Please check your .env file.")
        return

    category_urls = [
        "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
        "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0",
        "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_nav_books_0",
       " https://www.amazon.in/gp/bestsellers/toys/ref=zg_bs_nav_toys_0",
        "https://www.amazon.in/gp/bestsellers/apparel/ref=zg_bs_nav_apparel_0",
        "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0",
        "https://www.amazon.in/gp/bestsellers/home/ref=zg_bs_nav_home_0",
        "https://www.amazon.in/gp/bestsellers/hpc/ref=zg_bs_nav_hpc_0",
    ]
    
    driver = create_driver(headless=True)

    all_product_details = {}

    try:
        driver = amazon_login(driver, phone, password)
        
        for category_url in category_urls:
            category_name = category_url.split('/')[4]  # Extract category from URL
            product_details_list = scrape_best_seller_products(driver, category_url)
            all_product_details[category_name] = product_details_list
        
        save_to_json(all_product_details, "all_best_sellers.json")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()