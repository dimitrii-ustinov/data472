# Data Contract for DATA472 Individual project based on Flask API

Base URL
http://54.252.8.81/:8000

Key value: please request the key from Central Collection Team.

## API Endpoints
### 1. Get AQI Data
*Endpoint: /*

Method: GET

Description: Returns a basic response to indicate the API is running.

Response:
```
{
    "Individual Project":"Dimitrii Ustinov"
}
```
### 2. Get Data
*Endpoint: /dus15/query*

Method: GET

Description: Retrieves asset data from the external API and returns it in JSON format.

Request Parameters:

key (required, string): The API key to authenticate the request. 
Response:

- Success (200 OK): Returns a JSON array of asset records.
```
[
    {
        "Type": "Bench",
        "SiteName": "Central Park",
        "PhotographURL": "http://example.com/photo.jpg",
        "lat": -43.5320,
        "lon": 172.6362
    },
    ...
]
```
- Error (401 Unauthorized):
```
{
    "error": "Invalid API key"
}
```
- Error (500 Internal Server Error):
```
{
    "error": "Data retrieval failed"
}
```
### 3. Get Metadata
*Endpoint: /dus15/metadata*

Method: GET

Description: Returns metadata about the fields included in the /dus15/query response.

Request Parameters:

key (required, string): The API key to authenticate the request. 
Response:

- Success (200 OK):
```
[
    {
        "field": "PhotographURL",
        "type": "string",
        "description": "URL to the photograph of the asset"
    },
    {
        "field": "SiteName",
        "type": "string",
        "description": "Name of the site where the asset is located"
    },
    {
        "field": "Type",
        "type": "string",
        "description": "Type of the asset"
    },
    {
        "field": "lat",
        "type": "float",
        "description": "Latitude of the asset location"
    },
    {
        "field": "lon",
        "type": "float",
        "description": "Longitude of the asset location"
    }
]
```
- Error (401 Unauthorized):
```
{
    "error": "Invalid API key"
}
```
### 4. Get README
*Endpoint: /dus15/readme*

Method: GET

Description: Returns the content of the README.md file.

Request Parameters:

key (required, string): The API key to authenticate the request.
Response:

- Success (200 OK): Returns the content of the README.md file as plain text.
- Error (401 Unauthorized):
```
{
    "error": "Invalid API key"
}
```
- Error (404 Not Found):
```
"error": "README.md file not found."
```

### 5. Get Logs
*Endpoint: /dus15/logs*

Method: GET

Description: Returns the content of the log file.

Request Parameters:

key (required, string): The API key to authenticate the request.
Response:

- Success (200 OK): Returns the content of the log file as plain text.
- Error (401 Unauthorized):
```
{
    "error": "Invalid API key"
}
```
- Error (404 Not Found):
```
"error": "Log file not found."
```
### Logging
The application logs are stored in the logs/app.log file. The logs include information about access attempts, errors, and other significant events within the application.

Example Requests
- Example: Front page
```bash
curl http://54.252.8.81:8000/
```
- Example: Get Data
```bash
curl "http://54.252.8.81:8000/dus15/query?key=INSERT-YOUR-KEY"
```
- Example: Get Metadata
```bash
curl "http://54.252.8.81:8000/dus15/metadata?key=INSERT-YOUR-KEY"
```
- Example: Get README
```bash
curl "http://54.252.8.81:8000/dus15/readme?key=INSERT-YOUR-KEY"
```
- Example: Get Logs
```bash
curl "http://54.252.8.81:8000/dus15/logs?key=INSERT-YOUR-KEY"
```

