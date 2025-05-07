# Dynamic Benchmarking Framework for LLM Evaluation

A Flask-based framework for evaluating Large Language Models (LLMs) using real-time weather data. This framework generates structured questions and answers from weather data and allows for LLM evaluation against these ground truth answers.

## Features

- Real-time weather data fetching using WeatherAPI
- Historical weather data retrieval
- Structured Q&A generation from weather data
- LLM evaluation using Google's Gemini model
- JSON export of questions and answers
- Interactive web interface for data visualization

## Prerequisites

- Python 3.7+
- Flask
- WeatherAPI account
- Google Gemini API access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```bash
pip install flask weatherapi google-generativeai
```

3. Set up API keys:
   - WeatherAPI key is already configured in the code
   - Google Gemini API key is already configured in the code

## Project Structure

```
.
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── index.html     # Main page
│   ├── json_display.html  # JSON data display
│   └── evaluate.html  # LLM evaluation page
└── static/
    └── json/          # Generated JSON files
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Access the web interface at `http://127.0.0.1:5000/`

3. Use the interface to:
   - Fetch current weather data
   - Retrieve historical weather data
   - Generate Q&A pairs
   - Evaluate LLM responses
   - Download generated JSON files

## API Endpoints

- `/` - Home page
- `/get_weather` - Weather data retrieval endpoint
- `/download/<filename>` - Download generated JSON files
- `/evaluate` - LLM evaluation endpoint

## Data Generation

The framework generates three types of Q&A pairs:
1. Current weather data
2. Historical weather data
3. Hourly weather data

Each Q&A pair includes:
- Question in natural language
- Answer with appropriate units
- Timestamp and location information

### Data Format

The framework supports two output formats designed for effective LLM evaluation:

1. **Question-Only Format**
This format allows the model to focus solely on response generation without pre-answered data:

```json
[
  {
    "question": "What time did the sun rise in Salt Lake City on 2024-11-21?"
  },
  {
    "question": "What time did the moon rise in Salt Lake City on 2024-11-21?"
  },
  {
    "question": "What is the current weather condition in Salt Lake City?"
  }
]
```

2. **Question-Answer Pairs Format**
This format includes the correct answers for evaluation:

```json
[
  {
    "question": "What time did the sun rise in Salt Lake City on 2024-11-21?",
    "answer": "7:21 AM"
  },
  {
    "question": "What time did the moon rise in Salt Lake City on 2024-11-21?",
    "answer": "11:14 AM"
  },
  {
    "question": "What is the current weather condition in Salt Lake City?",
    "answer": "Partly cloudy"
  }
]
```

This structured format facilitates:
- Direct evaluation of model response accuracy
- Clear benchmarking against ground truth data
- Consistent evaluation across different weather parameters
- Dynamic data-based response assessment

## LLM Evaluation

The framework uses Google's Gemini model to:
- Process generated questions
- Generate responses
- Compare responses with ground truth answers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Acknowledgments

- WeatherAPI for weather data
- Google Gemini for LLM capabilities
- Flask framework for web application 
