from app import app, db, Weather

def seed():
    with app.app_context():  # Ensure the app context is used
        # Add some sample weather data
        city_weather = Weather(city="Nairobi", temperature=25.0, description="Clear sky")
        db.session.add(city_weather)
        db.session.commit()
        print("Database seeded!")

if __name__ == "__main__":
    seed()
