import requests
import re
import string
import random
import time

# Function to extract the file code from the provided URL
def extract_file_code(url):
    match = re.search(r'.*/(.*)', url.rstrip('/'))
    return match.group(1) if match else None

# Function to generate a random string of letters and digits
def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Main function to process the Doodstream URL
def process_doodstream_url(url):
    print("Starting the process to fetch the Doodstream CDN link...")
    
    # Create a session object to maintain settings across requests
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://d000d.com/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    })
    print("Session headers set successfully.")

    # Extract the file code from the URL
    file_code = extract_file_code(url)
    if not file_code:
        print("Error: Can't find the file code in the URL.")
        print(f"Are you sure {url} is correct?")
        return

    # Construct the Doodstream URL using the file code
    doodstream_url = f"https://d000d.com/e/{file_code}"
    print(f"Filecode extracted: {file_code}")
    print(f"Constructed Doodstream URL: {doodstream_url}")

    # Send a GET request to the Doodstream URL
    response = session.get(doodstream_url)
    if response.status_code == 200:
        print("Successfully fetched the Doodstream page.")
        
        # Search for a specific URL pattern inside the response text
        match = re.search(r"\$.get\('([^']+)',\s*function\(data\)", response.text)
        if match:
            url_inside_get = match.group(1)
            print(f"URL found inside the response: {url_inside_get}")
            
            last_value = re.search(r"/([^/]+)$", url_inside_get).group(1)
            url = f"https://d000d.com{url_inside_get}"
            print(f"Constructed URL for second request: {url}")

            # Send a GET request to the URL found inside the initial response
            response = session.get(url)
            if response.ok:
                print("Successfully fetched the secondary URL contents.")
                
                part_1 = response.text
                random_string = generate_random_string()
                token = last_value
                expiry = int(time.time() * 1000)
                part_2 = f"{random_string}?token={token}&expiry={expiry}"
                final_url = f"{part_1}{part_2}"
                
                print(f"Generated random string: {random_string}")
                print(f"Token: {token}")
                print(f"Expiry timestamp: {expiry}")
                print(f"Doodstream CDN link generated: {final_url}")
            else:
                print("Error: Unable to fetch the contents of the secondary URL.")
        else:
            print("Error: Unable to find the required URL inside the initial response.")
    else:
        print("Error: Unable to fetch the Doodstream page. HTTP status code:", response.status_code)

# Get the Doodstream URL from the user
url = input('Doodstream Url: ')
process_doodstream_url(url)
