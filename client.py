import requests

# Define the base URL of your Flask application
base_url = 'http://127.0.0.1:5000'  # Assuming your Flask app is running on localhost port 5000

# Make a GET request to '/api/data' to get the entire DataFrame
response = requests.get(f'{base_url}/api/data')
if response.status_code == 200:
    data = response.json()
    print("Entire DataFrame:")
    print(data)
else:
    print(f"Error: {response.status_code}")