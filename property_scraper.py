import requests
from bs4 import BeautifulSoup
import csv
import time

def get_property_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details = {}
    details['MLS'] = soup.find('span', class_='mls-number').text.strip() if soup.find('span', class_='mls-number') else 'N/A'
    details['Address'] = soup.find('h1', class_='property-address').text.strip() if soup.find('h1', class_='property-address') else 'N/A'
    details['Beds'] = soup.find('span', class_='beds').text.strip() if soup.find('span', class_='beds') else 'N/A'
    details['Baths'] = soup.find('span', class_='baths').text.strip() if soup.find('span', class_='baths') else 'N/A'
    details['Square Foot'] = soup.find('span', class_='sqft').text.strip() if soup.find('span', class_='sqft') else 'N/A'
    details['List Price'] = soup.find('span', class_='list-price').text.strip() if soup.find('span', class_='list-price') else 'N/A'
    details['Description'] = soup.find('div', class_='property-description').text.strip() if soup.find('div', class_='property-description') else 'N/A'
    details['Listing Agent'] = soup.find('span', class_='agent-name').text.strip() if soup.find('span', class_='agent-name') else 'N/A'
    details['Year Built'] = soup.find('span', class_='year-built').text.strip() if soup.find('span', class_='year-built') else 'N/A'
    details['County'] = soup.find('span', class_='county').text.strip() if soup.find('span', class_='county') else 'N/A'
    details['Property Type'] = soup.find('span', class_='property-type').text.strip() if soup.find('span', class_='property-type') else 'N/A'
    details['Days on Equator'] = soup.find('span', class_='days-on-equator').text.strip() if soup.find('span', class_='days-on-equator') else 'N/A'
    
    return details

def main():
    base_url = "https://www.equator.com/srp?searchString=New%20York&saleType=Foreclosure&autoType=STATE"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    property_links = soup.find_all('a', class_='property-link', limit=10)
    
    print("Number of links found:", len(property_links))  # Added to print the number of links found
    
    results = []
    for link in property_links:
        property_url = 'https://www.equator.com' + link['href']
        property_details = get_property_details(property_url)
        results.append(property_details)
        time.sleep(1)  # Be polite, don't hammer the server
    
    # Write results to CSV
    with open('property_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['MLS', 'Address', 'Beds', 'Baths', 'Square Foot', 'List Price', 'Description', 
                      'Listing Agent', 'Year Built', 'County', 'Property Type', 'Days on Equator']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    main()