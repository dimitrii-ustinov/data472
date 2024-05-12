from flask import Flask, jsonify

application = Flask(__name__)

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


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)