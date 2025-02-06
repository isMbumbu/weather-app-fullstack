from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
import requests
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

API_KEY = os.getenv("WEATHER_API_KEY", "abc123yourapikey")

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "temperature": self.temperature,
            "description": self.description,
        }


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

    # Save the weather data to the database
    weather = Weather.query.filter_by(city=city).first()

    if not weather:
        weather = Weather(
            city=data["name"],
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"]
        )
        db.session.add(weather)
        db.session.commit()

    weather_data = weather.to_dict()

    return jsonify(weather_data)
     


if __name__ == '__main__':
    app.run(port=5555)
