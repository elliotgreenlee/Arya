# Manages weather information
from API_Helpers.openweather_utils import OpenweatherAPI
from API_Helpers.openai_utils import OpenAIAPI
from Utils.utils import load_json
from datetime import datetime


def daily_data_to_prompt(daily_data):
    prompt = "Here's the detailed daily weather data:\n\n"
    for day in daily_data:
        date = datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
        prompt += f"""
Date: {date}
- Morning Temp: {day['temp']['morn']}°F (Feels like: {day['feels_like']['morn']}°F)
- Daytime Temp: {day['temp']['day']}°F (Feels like: {day['feels_like']['day']}°F)
- Evening Temp: {day['temp']['eve']}°F (Feels like: {day['feels_like']['eve']}°F)
- Night Temp: {day['temp']['night']}°F (Feels like: {day['feels_like']['night']}°F)
- Weather: {day['weather'][0]['description']}
- Summary: {day['summary']}
- Humidity: {day['humidity']}%
- Dew Point: {day['dew_point']}°F
- UV Index: {day['uvi']}
- Precipitation Probability: {day['pop']*100}%
- Wind Speed: {day['wind_speed']} m/s (Gusts: {day['wind_gust']} m/s)
- Sunrise: {datetime.utcfromtimestamp(day['sunrise']).strftime('%H:%M:%S')} UTC
- Sunset: {datetime.utcfromtimestamp(day['sunset']).strftime('%H:%M:%S')} UTC

"""
    return prompt


def example():
    credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(credentials_path)

    user_latitude = 45.5152
    user_longitude = -122.6784
    openweather = OpenweatherAPI(api_keys['openweather_api_key'])
    daily_data = openweather.next_eight_days(user_latitude, user_longitude)

    openai = OpenAIAPI(api_keys['openai_api_key'])

    model = "gpt-4o"
    character = "You are Dr. Jo Harding from the movie Twister acting as my meteorologist household assistant."
    task = "Summarize the next 8 days of weather in Portland, taking special note of unseasonable weather and rain."
    weather = daily_data_to_prompt(daily_data)
    prompt = character + " " + task + " " + weather
    completion = openai.ask(model, prompt)

    print(completion.choices[0].message.content)


if __name__ == '__main__':
    example()
