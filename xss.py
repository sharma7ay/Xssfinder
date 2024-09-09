import argparse
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Color codes
RED = '\033[91m'
BLUE = '\033[94m'
END_COLOR = '\033[0m'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_urls_from_file(filename):
    """Read URLs from a specified file."""
    try:
        with open(filename, 'r') as file:
            urls = [url.strip() for url in file.readlines()]
            return urls
    except FileNotFoundError:
        logging.error(f"{RED}File not found: {filename}{END_COLOR}")
        return []
    except Exception as e:
        logging.error(f"{RED}Error reading URLs from file: {e}{END_COLOR}")
        return []

def read_payloads_from_file(filename):
    """Read XSS payloads from a specified file."""
    try:
        with open(filename, 'r') as file:
            payloads = [payload.strip() for payload in file.readlines()]
            return payloads
    except FileNotFoundError:
        logging.error(f"{RED}File not found: {filename}{END_COLOR}")
        return []
    except Exception as e:
        logging.error(f"{RED}Error reading payloads from file: {e}{END_COLOR}")
        return []

def test_xss_with_selenium(url, payload):
    """Test the specified URL with the provided XSS payload."""
    test_url = url.replace("Gxss", payload)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(test_url)
        # Wait for alert to be present
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        logging.info(f"{RED}Alert box triggered in {test_url}: {alert.text}{END_COLOR}")
        alert.accept()
    except Exception as e:
        logging.info(f"{BLUE}No alert box in {test_url} or error occurred: {e}{END_COLOR}")
    finally:
        driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Test for XSS vulnerabilities.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='Input URL')
    group.add_argument('-uL', '--url-list', help='Input URL list file')

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-p', '--payload', help='Input payload')
    group2.add_argument('-pL', '--payload-list', help='Input payload list file')

    args = parser.parse_args()

    urls = [args.url] if args.url else read_urls_from_file(args.url_list)
    payloads = [args.payload] if args.payload else read_payloads_from_file(args.payload_list)

    for url in urls:
        for payload in payloads:
            test_xss_with_selenium(url, payload)

if __name__ == "__main__":
    main()