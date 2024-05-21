
from flask import Flask, jsonify, request, Response
import pandas as pd
import requests
import os
import logging
import time
import datetime

application = Flask(__name__)

# Define the correct API key
API_KEY = "Fish-Sea-Hat-Forest!"

# Metadata for the fields in the response
metadata = [
    {"field": "PhotographURL", "type": "string", "description": "URL to the photograph of the asset"},
    {"field": "SiteName", "type": "string", "description": "Name of the site where the asset is located"},
    {"field": "Type", "type": "string", "description": "Type of the asset"},
    {"field": "lat", "type": "float", "description": "Latitude of the asset location"},
    {"field": "lon", "type": "float", "description": "Longitude of the asset location"}
]

# Ensure the "logs" directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging configuration
logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

logger = logging.getLogger(__name__)

@application.route("/")
def get_aqi_data():
    logger.info("Accessed / route")
    return jsonify({"Individual Project": "Dimitrii Ustinov"})

# Construct the API URL with parameters
url = "https://gis.ccc.govt.nz/server/rest/services/OpenData/Furniture/FeatureServer/19/query"
params = {
    'where': '1=1',
    'outFields': 'Type,SiteName,PhotographURL',
    'resultType': 'standard',  # Retrieve all records at once
    'outSR': '4326',
    'f': 'json'
}

# Make the GET request
def get_df():

    logger.debug("Making GET request to API")
    start_time = time.time()  # Start time of the request
    response = requests.get(url, params=params)
    end_time = time.time()  # End time of the request
    if response.status_code == 200:
        duration = end_time - start_time  # Duration of the request in seconds
        data_size = len(response.content)  # Size of the received data in bytes 
        logger.info(f"Data successfully retrieved in {duration:.2f} seconds. Data size: {data_size/1024} kbytes.")       
        data = response.json()
        features = data.get('features', [])
        records = [feature['attributes'] for feature in features]
        geometry = [feature['geometry'] for feature in features]
        df = pd.DataFrame(records)
        for values in geometry:
            df['lon'] = values['x']
            df['lat'] = values['y']
        df['SiteName'] = df['SiteName'].str.split(' - ').str.get(1)
        # year = datetime.datetime.now().year
        # month = datetime.datetime.now().month
        # day = datetime.datetime.now().day
        # df['DateSaved'] = datetime.date(year,month,day)
        logger.info("Data successfully retrieved and DataFrame created")
        return df
    else:
        logger.error(f"Error: {response.status_code}")
        #print("Error:", response.status_code)
        return None
    

@application.route('/dus15/query')
def get_data():
    key = request.args.get('key')
    if key != API_KEY:
        logger.warning("Invalid API key attempt")
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    df = get_df()
    if df is not None:
        logger.info("Data returned successfully")
        return jsonify(df.to_dict(orient='records'))
    else:
        logger.error("Data retrieval failed")
        return jsonify({"error": "Data retrieval failed"}), 500  # Internal Server Error
    

@application.route('/dus15/metadata')
def get_metadata():
    key = request.args.get('key')
    if key != API_KEY:
        logger.warning("Invalid API key attempt")
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    logger.info("Metadata returned successfully")
    return jsonify(metadata)



@application.route('/dus15/readme')
def get_readme():
    key = request.args.get('key')
    if key != API_KEY:
        logger.warning("Invalid API key attempt")
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized
    readme_path = os.path.join(os.path.dirname(__file__), 'app', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            content = file.read()
            logger.info("README.md returned successfully")
        return Response(content, mimetype='text/plain')
    else:
        logger.error("README.md file not found")
        return 'README.md file not found.', 404

if __name__ == "__main__":
    logger.info("Starting Flask application")
    application.run(host="0.0.0.0", port=8000)
