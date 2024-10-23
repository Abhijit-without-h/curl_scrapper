from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Update this path to match the location of your Chromedriver
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

def extract_curl_and_responses(driver):
    # Wait for the page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.sidebar"))
    )

    # Get the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all 'Example Request' and 'Example Response' sections
    example_sections = soup.find_all('div', class_=['example-response'])

    curl_commands = []
    response_bodies = []

    for section in example_sections:
        code_snippet = section.find('code', class_='language-shell')
        if code_snippet:
            command = code_snippet.get_text().strip()
            if command.lower().startswith('curl'):
                curl_commands.append(command)
                print(f"Curl Command: {command}")

        # Find the response body within the section
        response_body = section.find('code', class_='language-json')
        if response_body:
            body = response_body.get_text().strip()
            response_bodies.append(body)
            print(f"Response Body: {body}")

    return curl_commands, response_bodies

if __name__ == "__main__":
    # Initialize the Chrome driver
    chrome_service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_service)

    # Navigate to the target URL
    url = "https://rapidapi.com/rockapis-rockapis-default/api/linkedin-data-api/playground/apiendpoint_1d2ead16-5039-4883-ac25-390fa57edf94"
    driver.get(url)

    # Extract curl commands and response bodies 
    curl_commands, response_bodies = extract_curl_and_responses(driver)

    # Keep the browser open for observation
    print("Press Enter to close the browser...")
    input()

    # Close the browser
    driver.quit()