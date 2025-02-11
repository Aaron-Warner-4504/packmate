# Packmate : Smart Packing Assistant

## Overview
Smart Packing Assistant is a Streamlit web application that generates a personalized packing list based on user inputs such as location, trip type, duration, activities, and personal details. The app fetches weather forecasts for the travel date to provide tailored recommendations. It utilizes AI models (Gemini and LLaMA via Groq API) to generate the packing lists dynamically.

## Features
- 🌍 Location-based packing recommendations
- ⛅ Weather-aware suggestions
- 🎒 Minimalist or detailed packing list options
- 👥 Personalized recommendations based on traveler details
- 🧠 AI-powered packing list generation using Gemini and LLaMA
- 📄 Downloadable DOCX packing list

## Technologies Used
- **Streamlit**: UI framework
- **Google Gemini API**: Primary AI model for generating packing lists
- **Groq LLaMA API**: Fallback AI model
- **OpenCage API**: Geolocation service to fetch latitude & longitude
- **OpenWeather API**: Fetches weather forecasts
- **Python Libraries**: `requests`, `google.generativeai`, `groq`, `docx`, `re`, `datetime`, `io`

## Installation & Setup
### Prerequisites
- Python 3.8+
- Install dependencies using:
  ```bash
  pip install streamlit requests google-generativeai groq python-docx
  ```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/smart-packing-assistant.git
   cd smart-packing-assistant
   ```
2. Set up API keys in the script:
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
   - `OPENCAGE_API_KEY`
   - `WEATHER_API_KEY`
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Enter your travel details in the sidebar (location, trip type, activities, etc.).
2. Select the type of packing list (Minimalist or Detailed).
3. Click "Generate Packing List 🧳" to receive a personalized recommendation.
4. View the weather forecast and suggested items.
5. Download the packing list as a DOCX file.

## API Key Configuration
Replace the placeholder API keys in the script with your actual keys:
```python
GEMINI_API_KEY = "your-gemini-api-key"
GROQ_API_KEY = "your-groq-api-key"
OPENCAGE_API_KEY = "your-opencage-api-key"
WEATHER_API_KEY = "your-weather-api-key"
```

## License
This project is licensed under the MIT License.

## Author
Pranav Kodlinge - pranavkodlinge@gmail.com
