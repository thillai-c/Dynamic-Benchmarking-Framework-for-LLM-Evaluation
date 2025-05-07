from flask import Flask, render_template, request, jsonify, send_file
import weatherapi
from weatherapi.rest import ApiException
import json
from flask import Response
import os
import google.generativeai as genai
app = Flask(__name__)
from flask import session
# Configure API key authorization for WeatherAPI
configuration = weatherapi.Configuration()
configuration.api_key['key'] = '0094f51698944c18b46211853240112'
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
questions_json=""


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    hour = int(request.form['hour'])
    date = request.form['date']
    weather_type = request.form['weather_type']
    response_type = request.form['response_type']

    try:
        weather_qna = []  # Initialize this variable outside the if-else blocks
        astro_qna = []    # Initialize as an empty list to avoid reference errors
        day_qna = []      # Initialize as an empty list to avoid reference errors
        hourly_qna = []   # Initialize as an empty list to avoid reference errors

        if weather_type == 'current':
            # Fetch current weather data
            api_response = api_instance.realtime_weather(city)
            weather_data = api_response['current']

            # Frame each field as a separate question-answer pair
            weather_qna = [
                {'question': f"What is the current temperature in {city} (C)?", 'answer': f"{weather_data['temp_c']} C"},
                {'question': f"What is the current temperature in {city} (F)?", 'answer': f"{weather_data['temp_f']} F"},
                {'question': f"What is the current weather condition in {city}?", 'answer': weather_data['condition']['text']},
                {'question': f"What is the current wind speed in {city} (mph)?", 'answer': f"{weather_data['wind_mph']} mph"},
                {'question': f"What is the current wind speed in {city} (kph)?", 'answer': f"{weather_data['wind_kph']} kph"},
                {'question': f"What is the current wind direction in {city} (degrees)?", 'answer': f"{weather_data['wind_degree']}"},
                {'question': f"What is the current wind direction in {city}?", 'answer': weather_data['wind_dir']},
                {'question': f"What is the current air pressure in {city} (mb)?", 'answer': f"{weather_data['pressure_mb']} mb"},
                {'question': f"What is the current air pressure in {city} (in)?", 'answer': f"{weather_data['pressure_in']} in"},
                {'question': f"What is the current precipitation in {city} (mm)?", 'answer': f"{weather_data['precip_mm']} mm"},
                {'question': f"What is the current precipitation in {city} (in)?", 'answer': f"{weather_data['precip_in']} in"},
                {'question': f"What is the current humidity in {city}?", 'answer': f"{weather_data['humidity']}%"},
                {'question': f"What is the current cloud coverage in {city}?", 'answer': f"{weather_data['cloud']}%"},
                {'question': f"What is the current feels-like temperature in {city} (C)?", 'answer': f"{weather_data['feelslike_c']} C"},
                {'question': f"What is the current feels-like temperature in {city} (F)?", 'answer': f"{weather_data['feelslike_f']} F"},
                {'question': f"What is the current windchill temperature in {city} (C)?", 'answer': f"{weather_data['windchill_c']} C"},
                {'question': f"What is the current windchill temperature in {city} (F)?", 'answer': f"{weather_data['windchill_f']} F"},
                {'question': f"What is the current heatindex in {city} (C)?", 'answer': f"{weather_data['heatindex_c']} C"},
                {'question': f"What is the current heatindex in {city} (F)?", 'answer': f"{weather_data['heatindex_f']} F"},
                {'question': f"What is the current dewpoint in {city} (C)?", 'answer': f"{weather_data['dewpoint_c']} C"},
                {'question': f"What is the current dewpoint in {city} (F)?", 'answer': f"{weather_data['dewpoint_f']} F"},
                {'question': f"What is the current visibility in {city} (km)?", 'answer': f"{weather_data['vis_km']} km"},
                {'question': f"What is the current visibility in {city} (miles)?", 'answer': f"{weather_data['vis_miles']} miles"},
                {'question': f"What is the current UV index in {city}?", 'answer': f"{weather_data['uv']}"},
                {'question': f"What is the current gust speed in {city} (mph)?", 'answer': f"{weather_data['gust_mph']} mph"},
                {'question': f"What is the current gust speed in {city} (kph)?", 'answer': f"{weather_data['gust_kph']} kph"}
            ]

        else:
            # Fetch historical weather data
            api_response = api_instance.history_weather(city, date, hour=hour)
            forecast = api_response['forecast']['forecastday'][0]
            astro_data = forecast['astro']
            day_data = forecast['day']
            hourly_data = forecast['hour']

            astro_qna = [
                {'question': f"What time did the sun rise in {city} on {date}?", 'answer': astro_data['sunrise']},
                {'question': f"What time did the sun set in {city} on {date}?", 'answer': astro_data['sunset']},
                {'question': f"What time did the moon rise in {city} on {date}?", 'answer': astro_data['moonrise']},
                {'question': f"What time did the moon set in {city} on {date}?", 'answer': astro_data['moonset']},
                {'question': f"What was the moon phase in {city} on {date}?", 'answer': astro_data['moon_phase']},
                {'question': f"What was the moon illumination percentage in {city} on {date}?", 'answer': astro_data['moon_illumination']},
                {'question': f"What was the average temperature in {city} on {date} (C)?", 'answer': day_data['avgtemp_c']},
                {'question': f"What was the average temperature in {city} on {date} (F)?", 'answer': day_data['avgtemp_f']},
                {'question': f"What was the maximum temperature in {city} on {date} (C)?", 'answer': day_data['maxtemp_c']},
                {'question': f"What was the maximum temperature in {city} on {date} (F)?", 'answer': day_data['maxtemp_f']},
                {'question': f"What was the minimum temperature in {city} on {date} (C)?", 'answer': day_data['mintemp_c']},
                {'question': f"What was the minimum temperature in {city} on {date} (F)?", 'answer': day_data['mintemp_f']},
                {'question': f"What was the average humidity in {city} on {date} (%)?", 'answer': day_data['avghumidity']},
                {'question': f"Did it rain in {city} on {date}?", 'answer': "Yes" if day_data['daily_will_it_rain'] else "No"},
                {'question': f"Did it snow in {city} on {date}?", 'answer': "Yes" if day_data['daily_will_it_snow'] else "No"},
                {'question': f"What was the UV index in {city} on {date}?", 'answer': day_data['uv']},
                {'question': f"What was the condition in {city} on {date}?", 'answer': day_data['condition']['text']},
            ]
            
             # Day Q&A
            day_qna = [
                {'question': f"What was the average temperature in {city} on {date} (C)?", 'answer': day_data['avgtemp_c']},
                {'question': f"What was the average temperature in {city} on {date} (F)?", 'answer': day_data['avgtemp_f']},
                {'question': f"What was the maximum temperature in {city} on {date} (C)?", 'answer': day_data['maxtemp_c']},
                {'question': f"What was the maximum temperature in {city} on {date} (F)?", 'answer': day_data['maxtemp_f']},
                {'question': f"What was the minimum temperature in {city} on {date} (C)?", 'answer': day_data['mintemp_c']},
                {'question': f"What was the minimum temperature in {city} on {date} (F)?", 'answer': day_data['mintemp_f']},
                {'question': f"What was the average humidity in {city} on {date} (%)?", 'answer': day_data['avghumidity']},
                {'question': f"Did it rain in {city} on {date}?", 'answer': "Yes" if day_data['daily_will_it_rain'] else "No"},
                {'question': f"Did it snow in {city} on {date}?", 'answer': "Yes" if day_data['daily_will_it_snow'] else "No"},
                {'question': f"What was the UV index in {city} on {date}?", 'answer': day_data['uv']},
                {'question': f"What was the condition in {city} on {date}?", 'answer': day_data['condition']['text']},
                {'question': f"What was the visibility in {city} on {date} (km)?", 'answer': day_data['avgvis_km']},
                {'question': f"What was the visibility in {city} on {date} (miles)?", 'answer': day_data['avgvis_miles']},
                {'question': f"What was the wind speed in {city} on {date} (kph)?", 'answer': day_data['maxwind_kph']},
                {'question': f"What was the wind speed in {city} on {date} (mph)?", 'answer': day_data['maxwind_mph']},
                {'question': f"What was the total precipitation in {city} on {date} (mm)?", 'answer': day_data['totalprecip_mm']},
                {'question': f"What was the total precipitation in {city} on {date} (in)?", 'answer': day_data['totalprecip_in']},
                {'question': f"What was the total snowfall in {city} on {date} (cm)?", 'answer': day_data['totalsnow_cm']},
            ]


            # Generate Q&A for Hourly data
            hourly_qna = []
            hourly_data = forecast['hour']
            for hour_data in hourly_data:
                hour_time = hour_data['time']
                hourly_qna.extend([
                    {'question': f"What was the temperature in {city} at {hour_time} (C)?", 'answer': hour_data['temp_c']},
                    {'question': f"What was the temperature in {city} at {hour_time} (F)?", 'answer': hour_data['temp_f']},
                    {'question': f"Was it day or night in {city} at {hour_time}?", 'answer': "Day" if hour_data['is_day'] else "Night"},
                    {'question': f"What was the humidity in {city} at {hour_time} (%)?", 'answer': hour_data['humidity']},
                    {'question': f"What was the wind speed in {city} at {hour_time} (kph)?", 'answer': hour_data['wind_kph']},
                    {'question': f"What was the wind speed in {city} at {hour_time} (mph)?", 'answer': hour_data['wind_mph']},
                    {'question': f"What was the wind direction in {city} at {hour_time}?", 'answer': hour_data['wind_dir']},
                    {'question': f"What was the pressure in {city} at {hour_time} (mb)?", 'answer': hour_data['pressure_mb']},
                    {'question': f"What was the pressure in {city} at {hour_time} (in)?", 'answer': hour_data['pressure_in']},
                    {'question': f"What was the chance of rain in {city} at {hour_time} (%)?", 'answer': hour_data['precip_mm']},
                ])

            # Combine all weather-related Q&A
        weather_qna.extend(astro_qna)
        weather_qna.extend(day_qna)
        weather_qna.extend(hourly_qna)
        question_only_1=[{'question': qa['question']} for qa in weather_qna]
        questions_json= json.dumps(question_only_1, indent=4)

        # Convert Q&A to JSON format
        if response_type == 'questions':
            # Extract only the questions
            questions_only = [{'question': qa['question']} for qa in weather_qna]
            json_data = json.dumps(questions_only, indent=4)
            
            download_filename = f"Realtime_questions_{city}_{date.replace('-', '_')}.json"
        elif response_type == 'qna':
            # Keep the full QnA pair
            json_data = json.dumps(weather_qna, indent=4)
            download_filename = f"Realtime_qna_{city}_{date.replace('-', '_')}.json"
        else:
            return jsonify({'error': 'Invalid response type'}), 400

        # Save the JSON data to a file in the 'static/json' folder
        json_folder = os.path.join(app.root_path, 'static', 'json')
        os.makedirs(json_folder, exist_ok=True)  # Ensure the folder exists
        json_file_path = os.path.join(json_folder, download_filename)

        # Save the JSON data to the file
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)

        # Render the JSON data in a webpage with a download link
        return render_template('json_display.html', json_data=json_data, download_filename=download_filename)

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/download/<filename>')
def download_file(filename):
    json_folder = os.path.join(app.root_path, 'static', 'json')
    json_file_path = os.path.join(json_folder, filename)

    if os.path.exists(json_file_path):
        return send_file(json_file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404
    
# Configure Gemini API
genai.configure(api_key="AIzaSyB9LBoBjEQt8yXyPT0Yfvv1rxOlIo_rrn8")
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

# Function to load questions from question.json


@app.route('/evaluate')
def evaluate_on_llm():
    # Load questions from the JSON file
    
    
    # Prepare prompt
    prompt = """
    Give answers to this in json format
 [
    {
        "question": "What time did the sun rise in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What time did the sun set in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What time did the moon rise in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What time did the moon set in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the moon phase in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the moon illumination percentage in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the average temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the average temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the maximum temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the maximum temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the minimum temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the minimum temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the average humidity in Salt Lake City on 2024-10-20 (%)?"
    },
    {
        "question": "Did it rain in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "Did it snow in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the UV index in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the condition in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the average temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the average temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the maximum temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the maximum temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the minimum temperature in Salt Lake City on 2024-10-20 (C)?"
    },
    {
        "question": "What was the minimum temperature in Salt Lake City on 2024-10-20 (F)?"
    },
    {
        "question": "What was the average humidity in Salt Lake City on 2024-10-20 (%)?"
    },
    {
        "question": "Did it rain in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "Did it snow in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the UV index in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the condition in Salt Lake City on 2024-10-20?"
    },
    {
        "question": "What was the visibility in Salt Lake City on 2024-10-20 (km)?"
    },
    {
        "question": "What was the visibility in Salt Lake City on 2024-10-20 (miles)?"
    },
    {
        "question": "What was the wind speed in Salt Lake City on 2024-10-20 (kph)?"
    },
    {
        "question": "What was the wind speed in Salt Lake City on 2024-10-20 (mph)?"
    },
    {
        "question": "What was the total precipitation in Salt Lake City on 2024-10-20 (mm)?"
    },
    {
        "question": "What was the total precipitation in Salt Lake City on 2024-10-20 (in)?"
    },
    {
        "question": "What was the total snowfall in Salt Lake City on 2024-10-20 (cm)?"
    },
    {
        "question": "What was the temperature in Salt Lake City at 2024-10-20 06:00 (C)?"
    },
    {
        "question": "What was the temperature in Salt Lake City at 2024-10-20 06:00 (F)?"
    },
    {
        "question": "Was it day or night in Salt Lake City at 2024-10-20 06:00?"
    },
    {
        "question": "What was the humidity in Salt Lake City at 2024-10-20 06:00 (%)?"
    },
    {
        "question": "What was the wind speed in Salt Lake City at 2024-10-20 06:00 (kph)?"
    },
    {
        "question": "What was the wind speed in Salt Lake City at 2024-10-20 06:00 (mph)?"
    },
    {
        "question": "What was the wind direction in Salt Lake City at 2024-10-20 06:00?"
    },
    {
        "question": "What was the pressure in Salt Lake City at 2024-10-20 06:00 (mb)?"
    },
    {
        "question": "What was the pressure in Salt Lake City at 2024-10-20 06:00 (in)?"
    },
    {
        "question": "What was the chance of rain in Salt Lake City at 2024-10-20 06:00 (%)?"
    }
]   1
    Use this JSON Schema:
    [
    {{
        "question": "What is the current temperature in Salt Lake City (°C)?",
        "answer": "0.0 C"
    }},
    {{
        "question": "What is the current temperature in Salt Lake City (°F)?",
        "answer": "00.0 F"
    }}
    ]
    """
    
    # Call Gemini API
    try:
        response = model.generate_content(prompt)
        llm_result = response.text
    except Exception as e:
        llm_result = f"Error occurred while calling the Gemini API: {e}"
    
    # Render the result on the evaluate page
    return render_template('evaluate.html', llm_result=llm_result)



if __name__ == '__main__':
    app.run(debug=True)
