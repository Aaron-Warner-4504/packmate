import streamlit as st  # Ensure Streamlit is imported first
import requests
import google.generativeai as genai
from groq import Groq
import time
from datetime import datetime
import re
from io import BytesIO
from docx import Document  # Import python-docx for DOCX generation

# Set page configuration (MUST be the first Streamlit command)
st.set_page_config(page_title="Smart Packing Assistant", page_icon="🎒", layout="wide")

# Configure API keys (replace with environment variables for security)
GEMINI_API_KEY = "AIzaSyBDEnO1lXyhUd6NctHbRqESI6BMdk61a8E"
GROQ_API_KEY = "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"
OPENCAGE_API_KEY = "993e21d6cca746a2bbebd2f6e02a8316"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Cache for storing location coordinates to reduce API calls
location_cache = {}
def get_lat_lon_from_opencage(location):
    if location in location_cache:
        return location_cache[location]
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            lat = data["results"][0]["geometry"]["lat"]
            lon = data["results"][0]["geometry"]["lng"]
            location_cache[location] = (lat, lon)
            return lat, lon
    return None, None

def create_docx(weather, packing_list):
    """Generates a DOCX file with bold formatting for asterisk-marked words."""
    buffer = BytesIO()
    doc = Document()
    doc.add_heading("Smart Packing Assistant", level=1)
    
    doc.add_paragraph(f"Weather Forecast: {weather}\n")
    doc.add_heading("Packing List:", level=2)
    
    for item in packing_list:
        para = doc.add_paragraph("- ")  # Bullet point
        # Detect word patterns for bold
        match = re.findall(r"\([^]+)\*", item)  # Match text between asterisks
        if match:
            # Replace word with bold version
            parts = re.split(r"(\[^]+\*)", item)  # Split text by asterisk-marked words
            for part in parts:
                if part.startswith("") and part.endswith(""):  # If it's marked by asterisks
                    run = para.add_run(part[1:-1])  # Remove asterisks
                    run.bold = True  # Make it bold
                else:
                    para.add_run(part)  # Add the rest as normal text
        else:
            para.add_run(item)

    doc.save(buffer)
    buffer.seek(0)
    return buffer


def extract_items_from_suggestions(suggestions):
    return [re.sub(r"[:•\-]+", "", line).strip() for line in suggestions.split("\n") if line.strip()]

def get_packing_suggestions(location, activities, people):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    chat_session = model.start_chat(history=[])
    prompt = f"Suggest a personalized packing list for {people} people traveling to {location} for {activities}. Include age, gender, and medical needs."
    try:
        response = chat_session.send_message(prompt)
        return extract_items_from_suggestions(response.text)
    except:
        return []

def fallback_packing_suggestions(location, activities, people):
    client = Groq(api_key=GROQ_API_KEY)
    query = f"Suggest a personalized packing list for {people} people traveling to {location} for {activities}. Include age, gender, and medical needs."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": query}],
            temperature=1,
            max_completion_tokens=200,
            top_p=1,
            stream=False
        )
        return extract_items_from_suggestions(completion.choices[0].message.get("content", ""))
    except:
        return []

# Streamlit UI
st.title("🎒 Personalized Packing List Generator")
st.markdown("### Plan your trip smarter with weather-based personalized packing lists!")

st.sidebar.header("🌍 Trip Details")
location = st.sidebar.text_input("Enter a location:")
activities = st.sidebar.text_area("Enter your activities (comma-separated):")
date = st.sidebar.date_input("Enter your travel date:", datetime.today()).strftime("%Y-%m-%d")
num_people = st.sidebar.number_input("Number of people:", min_value=1, step=1)

people = []
for i in range(num_people):
    with st.expander(f"👤 Person {i + 1} Details"):
        name = st.text_input(f"Name", key=f"name_{i}")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key=f"gender_{i}")
        age = st.number_input("Age", min_value=0, step=1, key=f"age_{i}")
        medical_issues = st.text_area("Any medical issues", key=f"medical_{i}")
        people.append({"name": name, "gender": gender, "age": age, "medical_issues": medical_issues})

if st.sidebar.button("Generate Packing List 🧳"):
    if not location or not activities or not date or not people:
        st.error("🚨 Please enter all required fields.")
    else:
        lat, lon = get_lat_lon_from_opencage(location)
        if lat and lon:
            weather = "Sunny with 25°C"  # Placeholder, replace with actual weather fetching logic
            packing_list = get_packing_suggestions(location, activities, people)
            if not packing_list:
                packing_list = fallback_packing_suggestions(location, activities, people)

            st.success("✅ Packing list generated successfully!")
            st.subheader("🌤 Weather Forecast")
            st.info(weather)

            st.subheader("📦 Personalized Packing List")
            st.write("\n".join(packing_list) if packing_list else "No suggestions available.")

            # Generate and provide download option for DOCX
            docx_file = create_docx(weather, packing_list)
            st.download_button(
                label="📥 Download Packing List as DOCX",
                data=docx_file,
                file_name="Packing_List.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.error("❌ Unable to retrieve location coordinates.")
