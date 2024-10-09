# Import necessary modules
from dotenv import load_dotenv
import os
import requests

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
api_key = os.getenv('API_KEY')

# Base URL of the Cat API
url = "https://api.thecatapi.com/v1/images/search"

# Headers including the API key for authentication
headers = {
    "x-api-key": api_key
}

# Make a request to the Cat API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Print the cat image URL from the response
    print("Here is a random cat image URL:", data[0]['url'])
else:
    # Print an error message if the request failed
    print(f"Failed to retrieve data: {response.status_code}")
