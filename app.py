import requests
import pandas as pd
import datetime
import numpy as np

# Construct the API URL with parameters
url = "https://gis.ccc.govt.nz/server/rest/services/OpenData/Furniture/FeatureServer/19/query?where=1%3D1&outFields=LastEditDate,Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus&outSR=4326&f=json"
params = {
    'where': '1=1',
    'outFields': 'LastEditDate,Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus',
    'outSR': '4326',
    'f': 'json'
}

# Make the GET request
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the features from the response
    features = data.get('features', [])
    #print(features[10])
    
    # Extract attributes from each feature
    for feature in features:
        records = feature["attributes"]
        #date_int =  feature["attributes"]['LastEditDate']#datetime.datetime.fromtimestamp(feature["attributes"]['LastEditDate']/1000)
        #date_time = datetime.datetime.fromtimestamp(date_int/1000)
    
    records = [feature['attributes'] for feature in features]
    geometry = [feature['geometry'] for feature in features]
    
    # Create DataFrame
    df = pd.DataFrame(records)
    #del(df["LastEditDate"])
    #df["Last_Edit_Date"] = date
    for values in geometry:
        df['lon'] = values['x']
        df['lat'] = values['y']

    df["Last_Edit_Date"] = pd.to_datetime(df["LastEditDate"], unit='ms').dt.date
    del(df["LastEditDate"])
    
    # Print DataFrame
    print(df.head(4))
else:
    print("Error:", response.status_code)
    

app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def get_data():
    # Return the entire DataFrame as JSON
    return "Response"#jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    #df = get_df()
    app.run(debug=True)

