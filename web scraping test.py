import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the sitemap
sitemap_url = "https://www.illinoislifespan.org/sitemap.xml"
sitemap_response = requests.get(sitemap_url)
sitemap_soup = BeautifulSoup(sitemap_response.text, 'xml')  # Use 'lxml' parser

# Extract URLs from the sitemap
urls = [loc.get_text() for loc in sitemap_soup.find_all('loc')]

# List to hold the scraped data
services = []

# Loop through each URL to scrape data
for url in urls:
    page_response = requests.get(url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    
    # Extract data from each page
    for service in page_soup.select('div.service-container'):  # Adjust based on HTML structure
        name = service.select_one('h3.service-name').get_text(strip=True)  # Adjust selector
        address = service.select_one('p.service-address').get_text(strip=True)  # Adjust selector
        services.append({'Name': name, 'Address': address})

# Save the data to a CSV file
df = pd.DataFrame(services)
df.to_csv('idd_services.csv', index=False)
print("Data scraped and saved to idd_services.csv")