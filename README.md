# Weather App

A web application that displays weather information for a given city using the OpenWeatherMap API.

## Features

- Search for weather by city name
- Display current temperature, weather conditions, and other details
- 5-day weather forecast
- Geolocation support to get weather for your current location
- Search history with quick access to previous searches
- Dark mode toggle with persistent settings
- Weather icons for better visualization
- Responsive design that works on desktop and mobile devices

## Setup and Installation

1. Clone this repository:

   ```
   git clone <repository-url>
   cd weather-app
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Get an API Key:

   - Sign up at [OpenWeatherMap](https://openweathermap.org/) to get your free API key
   - Create a `.env` file in the root directory
   - Add your API key to the `.env` file:
     ```
     WEATHER_API_KEY=your_api_key_here
     SECRET_KEY=your_secret_key_for_sessions
     ```
   - Or directly update the API_KEY value in app.py with your actual API key

4. Run the application:

   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Technologies Used

- Python
- Flask (Web Framework)
- OpenWeatherMap API
- HTML/CSS
- JavaScript (Geolocation API, Theme Toggle, AJAX)

## Screenshots

(Add screenshots of your application here)

## Future Improvements

- Unit conversion (Celsius/Fahrenheit)
- Weather maps integration
- Weather alerts and notifications
- More detailed hourly forecasts
- Air quality index information
