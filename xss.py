import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Color codes
RED = '\033[91m'
BLUE = '\033[94m'
END_COLOR = '\033[0m'

# Function to read URLs from a file
def read_urls_from_file(filename):
    try:
        with open(filename, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]
            return urls
    except Exception as e:
        print(f"{RED}Error reading URLs from file: {e}{END_COLOR}")
        return []

# Function to read XSS payloads from a file
def read_payloads_from_file(filename):
    try:
        with open(filename, 'r') as file:
            payloads = file.readlines()
            payloads = [payload.strip() for payload in payloads]
            return payloads
    except Exception as e:
        print(f"{RED}Error reading payloads from file: {e}{END_COLOR}")
        return []

# Function to test XSS with Selenium
def test_xss_with_selenium(url, payload):
    # Replace 'Gxss' with the XSS payload
    test_url = url.replace("Gxss", payload)

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless if you don't want a GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(test_url)
        time.sleep(2)  # Wait for the page to load

        # Check for alert
        try:
            alert = driver.switch_to.alert
            if alert:
                print(f"{RED}Alert box triggered in {test_url}: {alert.text}{END_COLOR}")
                alert.accept()  # Close the alert
        except Exception:
            print(f"{BLUE}No alert box in {test_url}{END_COLOR}")
    except Exception as e:
        print(f"{RED}Error testing XSS in {test_url}: {e}{END_COLOR}")
    finally:
        driver.quit()

# Main function
def main():
    parser = argparse.ArgumentParser(description='Test for XSS vulnerabilities.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='Input URL')
    group.add_argument('-uL', '--url-list', help='Input URL list file')

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-p', '--payload', help='Input payload')
    group2.add_argument('-pL', '--payload-list', help='Input payload list file')

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.url_list:
        urls = read_urls_from_file(args.url_list)

    if args.payload:
        payloads = [args.payload]
    elif args.payload_list:
        payloads = read_payloads_from_file(args.payload_list)

    for url in urls:
        for payload in payloads:
            test_xss_with_selenium(url, payload)

if __name__ == "__main__":
    main()
