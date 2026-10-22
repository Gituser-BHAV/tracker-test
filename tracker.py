import os
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def check_amazon_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Selectors can change; standard Amazon price classes:
        price_element = soup.find("span", class_="a-price-whole")
        if price_element:
            price_text = price_element.get_text().replace(',', '').replace('.', '').strip()
            return int(price_text)
    except Exception as e:
        print(f"Error checking Amazon: {e}")
    return None

def check_flipkart_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Flipkart dynamic pricing row
        price_element = soup.find("div", class_="Nx9w7j")  # Note: Flipkart classes obfuscate frequently
        if not price_element:
            price_element = soup.find("div", class_="_30jeq3") # Fallback older class
            
        if price_element:
            price_text = price_element.get_text().replace('₹', '').replace(',', '').strip()
            return int(price_text)
    except Exception as e:
        print(f"Error checking Flipkart: {e}")
    return None

if __name__ == "__main__":
    # Example Target URLs (passed via GitHub Repository Secrets or hardcoded)
    amazon_url = os.getenv("AMAZON_PRODUCT_URL", "YOUR_DEFAULT_AMAZON_URL")
    flipkart_url = os.getenv("FLIPKART_PRODUCT_URL", "YOUR_DEFAULT_FLIPKART_URL")
    
    print("--- Starting Price Check ---")
    if "amazon" in amazon_url:
        amzn_price = check_amazon_price(amazon_url)
        print(f"Amazon Price: ₹{amzn_price}" if amzn_price else "Failed to parse Amazon Price")
        
    if "flipkart" in flipkart_url:
        fk_price = check_flipkart_price(flipkart_url)
        print(f"Flipkart Price: ₹{fk_price}" if fk_price else "Failed to parse Flipkart Price")
        
    # TODO: Add alert/notification threshold logic here (e.g., Email or Telegram Bot notification)
