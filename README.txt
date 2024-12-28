Amazon Best Sellers Scraper

Description:

This Python-based scraper is designed to extract detailed information from Amazon's Best Sellers section, focusing on products with discounts greater than 50%. The scraper performs authentication, handles CAPTCHA challenges, and retrieves data for products in 10 different categories. The extracted information is then stored in a structured format (CSV/JSON).

Key Features:

Authentication:

The scraper uses valid Amazon credentials to log in. If a CAPTCHA is encountered, the script will pause and allow the user to complete the CAPTCHA manually before resuming the scraping process.
Data Collection:

Scrape top-selling products in 10 categories (for example: Kitchen, Shoes, Computers, Electronics, etc.).
For each product, collect the following details:
Product Name
Product Price
Product Rating
Product Description

Error Handling:

The scraper includes robust error handling to deal with interruptions, page load issues, or missing data during the scraping process.
Data Storage:

The collected data is stored in either a CSV or JSON file format for easy access and further analysis.
Headless Mode with CAPTCHA Handling:

The scraper runs headlessly (without opening a browser window), but if a CAPTCHA challenge is encountered, the browser window opens for manual interaction. After solving the CAPTCHA, the script resumes from where it left off.
Requirements:
Python 3.x
Selenium
ChromeDriver or GeckoDriver (based on browser choice)
WebDriver Manager (optional for automatic driver management)
Pandas (for data storage in CSV format)
JSON (for storing data in JSON format)
Valid Amazon Account Credentials (for authentication)
Technical Specifications:
The script uses Selenium for web automation to interact with Amazon’s pages.
The script performs scraping on the Best Seller's page and navigates to category pages to extract details.
Error handling is implemented using try-except blocks to prevent crashes during scraping and log any issues for troubleshooting.
Data is stored in a structured CSV or JSON format for easy data analysis.
Installation Instructions
Install Required Libraries: Install the necessary Python packages using pip:

bash
Copy code
pip install selenium pandas webdriver-manager
Download and Set Up WebDriver: Ensure you have a compatible WebDriver for your browser (Chrome or Firefox). If using Chrome, download the appropriate version of ChromeDriver or use WebDriver Manager for automatic management.

Configure Credentials: Set your Amazon login credentials in the script, ensuring you have access to an Amazon account that can authenticate.

Usage Instructions
Run the Script: Execute the scraper script:

bash
Copy code
python amazon_scraper.py
Authentication:

On the first run, the scraper will open a browser window for you to log in with your Amazon credentials.
If CAPTCHA appears, the browser window will stay open for you to complete it manually. Once done, the script will continue the scraping process.
Data Storage:

The data will be saved in either CSV or JSON format, as specified in the script.
Example URLs
Amazon Best Sellers: https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2
Category URLs:
Kitchen:https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0
Shoes:https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0
Computers:https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0
Electronics:https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0
Script Flow
Login: The script logs into Amazon using provided credentials.
Captcha Handling: If a CAPTCHA is detected, it opens a browser window for manual intervention.
Navigate Best Sellers: The script navigates through Amazon's Best Sellers page and iterates through product categories.
Scrape Data: It scrapes detailed product information for the top 1500 best-selling products in each category.
Store Data: After scraping, the results are stored in a CSV or JSON file.
Error Handling
The script will log any issues encountered during the scraping process:

Login Failures: Invalid credentials or CAPTCHA issues will be logged.
Page Load Failures: If a page doesn't load correctly, an error message will be shown and the scraper will retry.
Data Issues: Missing or incomplete product information will be logged and skipped.
Notes
Ensure you comply with Amazon's Terms of Service when scraping their website. This script is intended for educational purposes and personal use only.
Running the scraper on a large scale or too frequently may lead to IP bans or account restrictions from Amazon.
