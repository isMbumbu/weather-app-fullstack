from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "abc123yourapikey"


@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400
    
    # Fetch weather from OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": data.get("message", "Something went wrong")}), response.status_code

    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(port=5555)
