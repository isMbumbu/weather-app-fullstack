import { useState } from "react";
import axios from "axios";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState("");

  const fetchWeather = async () => {
    try {
      setError("");
      const response = await axios.get(`http://127.0.0.1:5555/api/weather`, {
        params: { city },
      });
      setWeather(response.data);
    } catch (err) {
      setWeather(null);
      setError(err.response?.data?.error || "Failed to fetch weather");
    }
  };

  return (
    <div className="flex flex-col items-center p-10">
      <h1 className="text-2xl font-bold mb-4">Weather App 🌤</h1>
      <input
        type="text"
        className="border p-2 mb-4"
        placeholder="Enter city name"
        value={city}
        onChange={(e) => setCity(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={fetchWeather}
      >
        Get Weather
      </button>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {weather && (
        <div className="mt-4">
          <h2 className="text-xl">{weather.city}</h2>
          <p>Temperature: {weather.temperature}°C</p>
          <p>Description: {weather.description}</p>
        </div>
      )}
    </div>
  );
}

export default App;
