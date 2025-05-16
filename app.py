from flask import Flask, render_template, request, session, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Add timestamp filter
@app.template_filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')

# API key for OpenWeatherMap
API_KEY = os.environ.get("WEATHER_API_KEY", "ed3cc874d48e72597b479ba377d9e4cc")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None
    
    # Initialize search history in session if it doesn't exist
    if 'search_history' not in session:
        session['search_history'] = []
    
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            error = "Please enter a city name"
        else:
            try:
                # Current weather data
                params = {
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric'  # Use Celsius
                }
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                
                weather_data = response.json()
                
                # Get 5-day forecast
                forecast_params = {
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric'
                }
                forecast_response = requests.get(FORECAST_URL, params=forecast_params)
                forecast_response.raise_for_status()
                
                # Process forecast data to get one entry per day
                all_forecasts = forecast_response.json()['list']
                forecast_data = process_forecast_data(all_forecasts)
                
                # Add to search history if not already present
                if city not in session['search_history']:
                    session['search_history'].insert(0, city)
                    # Keep only the last 5 searches
                    if len(session['search_history']) > 5:
                        session['search_history'] = session['search_history'][:5]
                    session.modified = True
                
            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    error = f"City '{city}' not found"
                elif response.status_code == 401:
                    error = "API key error. Please check your API key and try again."
                else:
                    error = f"Error fetching weather data: {e}"
            except Exception as e:
                error = f"An error occurred: {e}"
    
    return render_template('index.html', 
                          weather_data=weather_data, 
                          forecast_data=forecast_data,
                          error=error,
                          search_history=session.get('search_history', []))

@app.route('/weather/coordinates', methods=['POST'])
def weather_by_coordinates():
    """Get weather data by coordinates (for geolocation)."""
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        
        if not lat or not lon:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # Current weather data
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        # Get 5-day forecast
        forecast_params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        forecast_response = requests.get(FORECAST_URL, params=forecast_params)
        forecast_response.raise_for_status()
        
        # Process forecast data to get one entry per day
        all_forecasts = forecast_response.json()['list']
        forecast_data = process_forecast_data(all_forecasts)
        
        # Add city to search history if not already present
        city_name = weather_data['name']
        if city_name and city_name not in session.get('search_history', []):
            if 'search_history' not in session:
                session['search_history'] = []
            session['search_history'].insert(0, city_name)
            # Keep only the last 5 searches
            if len(session['search_history']) > 5:
                session['search_history'] = session['search_history'][:5]
            session.modified = True
        
        return jsonify({
            'weather_data': weather_data,
            'forecast_data': forecast_data
        })
        
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f"Error fetching weather data: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

def process_forecast_data(forecast_list):
    """Process the forecast data to get one entry per day."""
    daily_forecasts = {}
    
    for forecast in forecast_list:
        # Convert timestamp to date
        date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
        
        # We'll take the noon forecast as representative for the day
        time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
        
        # If we don't have an entry for this day yet, or if this entry is closer to noon
        if date not in daily_forecasts or abs(int(time.split(':')[0]) - 12) < abs(int(daily_forecasts[date]['time'].split(':')[0]) - 12):
            daily_forecasts[date] = {
                'date': date,
                'time': time,
                'temp': forecast['main']['temp'],
                'feels_like': forecast['main']['feels_like'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed']
            }
    
    # Convert to list and sort by date
    result = list(daily_forecasts.values())
    result.sort(key=lambda x: x['date'])
    
    return result

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear the search history."""
    session['search_history'] = []
    return jsonify({'status': 'success'})

# For local development
if __name__ == '__main__':
    app.run(debug=True)
    
# For Vercel
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None'
) 