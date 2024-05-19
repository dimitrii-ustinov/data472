from flask import Flask, jsonify

# Create a Flask application instance
app = Flask(__name__)

# # Define a route for the GET request
# @app.route('/greet', methods=['GET'])
# def greet():
#     # You can customize the response here
#     return jsonify({'message': 'Hello, welcome to my Flask app!'})

# # Run the application if this file is executed directly
# if __name__ == '__main__':
#     app.run(debug=True)



# Construct the API URL with parameters
url = "https://gis.ccc.govt.nz/server/rest/services/OpenData/Furniture/FeatureServer/19/query?where=1%3D1&outFields=Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus&outSR=4326&f=json"
params = {
    'where': '1=1',
    'outFields': 'Type,PhotographURL,SiteName,AssetLongDescription,ContractArea,ServiceStatus',
    'outSR': '4326',
    'f': 'json'
}

# Make the GET request
def get_df():
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
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
        return df

    # df['geometry'] = geometry
        
        # Print DataFrame
        # print(df.head(4))
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
