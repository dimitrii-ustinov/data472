from flask import Flask, jsonify, request
import pandas as pd
import requests

application = Flask(__name__)

# Define the correct API key
API_KEY = "Fish-Sea-Hat-Forest!"

# Metadata for the fields in the response
metadata = [
    {"field": "AssetLongDescription", "type": "string", "description": "Long description of the asset"},
    {"field": "ContractArea", "type": "string", "description": "Contract area where the asset is located"},
    {"field": "LastEditDate", "type": "float", "description": "Timestamp of the last edit date"},
    {"field": "PhotographURL", "type": "string", "description": "URL to the photograph of the asset"},
    {"field": "ServiceStatus", "type": "string", "description": "Current service status of the asset"},
    {"field": "SiteName", "type": "string", "description": "Name of the site where the asset is located"},
    {"field": "Type", "type": "string", "description": "Type of the asset"},
    {"field": "lat", "type": "float", "description": "Latitude of the asset location"},
    {"field": "lon", "type": "float", "description": "Longitude of the asset location"}
]

@application.route("/")
def get_aqi_data():
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
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        records = [feature['attributes'] for feature in features]
        geometry = [feature['geometry'] for feature in features]
        df = pd.DataFrame(records)
        for values in geometry:
            df['lon'] = values['x']
            df['lat'] = values['y']
        return df
    else:
        print("Error:", response.status_code)
        return None

@application.route('/query')
def get_data():
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    df = get_df()
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({"error": "Data retrieval failed"}), 500  # Internal Server Error
    

@application.route('/metadata')
def get_metadata():
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    return jsonify(metadata)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
