# Data description
The dataset contains information about seats in Christchurch.


# Structure

The API ports are structured the following way:
- '/dus15/query' :        'returns the raw json with 3973 rows at the moment"

- '/dus15/metadata' :     'returns the metadata table of the following format:
                          "field": "column name"
                          "type": "data type"
                          "description": "short string of text"
                        
- '/dus15/readme' :       'returns this file'

- '/':                    'returns the creator of the project'

# Insights

The information is taken from OpenData portal. However, the information about the seats is not intuitively accessible from google maps or CCC website.
It is challenging to navigate and find the data. It is important to provide easy and intuitive access to this data to elderly, disabled and people with young children.
Possible visualizations:
1. Map the seats
2. Distribution of seats for each type and SiteName
