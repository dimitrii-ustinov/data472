from flask import Flask, jsonify, request
import pandas as pd
import requests

application = Flask(__name__)

# Define the correct API key
API_KEY = "Fish-Sea-Hat-Forest!"

aqi_data = []
for i in range(200):
    data_point = {
        "date": f"2024-05-{i+1}",
        "location": f"Location {i+1}",
        "region": f"Region {(i % 5) + 1}",  # Assign regions based on a modulus operation
        "aqi": 50 + i,
        "pm25": 10 + i,
        "pm10": 20 + i,
        "o3": 30 + i,
        "no2": 40 + i,
        "so2": 50 + i,
        "co": 60 + i,
        "temperature": 20 + i,
        "humidity": 50 + i,
        "wind_speed": 5 + i,
    }
    aqi_data.append(data_point)


@application.route("/")
def get_aqi_data():
    return jsonify(aqi_data)


# Construct the API URL with parameters
url = "https://gis.ccc.govt.nz/server/rest/services/OpenData/Furniture/FeatureServer/19/query?where=1%3D1&outFields=LastEditDate,Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus&outSR=4326&f=json"
params = {
    'where': '1=1',
    'outFields': 'Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus',
    'outSR': '4326',
    'f': 'json'
}

# Make the GET request
def get_df():
   response = requests.get(url, params=params)
   key = request.args.get('key')
   #fields = request.args.get('fields')
   if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    #Check if the request was successful (status code 200)
   elif response.status_code == 200:
       # Parse the JSON response
       data = response.json()
       
       # Extract the features from the response
       features = data.get('features', [])
       #print(features[10])
       
       # Extract attributes from each feature
       records = [feature['attributes'] for feature in features]
       geometry = [feature['geometry'] for feature in features]
       
       # Create DataFrame
       df = pd.DataFrame(records)
       for values in geometry:
           df['lon'] = values['x']
           df['lat'] = values['y']

       #df["Last_Edit_Date"] = pd.to_datetime(df["LastEditDate"], unit='ms').dt.date
       #del(df["LastEditDate"])
       return df
   else:
       print("Error:", response.status_code)
@application.route('/query')
def get_data():
   df = get_df()
   # Return the entire DataFrame as JSON
   return jsonify(df.to_dict(orient='records'))

# @application.route("/query")
# def query_data():
#     # Check if the 'key' and 'fields' query parameters are provided
#     key = request.args.get('key')
#     fields = request.args.get('fields')

#     #Verify if the API key matches
#     if key != API_KEY:
#         return jsonify({"error": "Invalid API key"}), 401  # Unauthorized

#     # Check if 'fields' parameter is provided
#     #if not fields:
#     #    return jsonify({"error": "Missing 'fields' parameter"}), 400  # Bad Request

#     # Only proceed if the correct key is provided
#     # For demonstration purposes, you can directly return a sample response
#     sample_response = {
#         "Type": "Sample Type",
#         "PhotographURL": "https://example.com/sample.jpg",
#         "SiteName": "Sample Site",
#         "AssetLongDescription": "Sample Description",
#         "ContractArea": "Sample Area",
#         "ServiceStatus": "Active"
#     }
#     return jsonify(sample_response)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)