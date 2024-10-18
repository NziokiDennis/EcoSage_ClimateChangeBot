import streamlit as st
from transformers import pipeline
import logging
import requests

# Set up logging for user interactions
logging.basicConfig(filename='user_interactions.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Title for the chatbot app
st.title("EcoSage Climate Bot")

# Load the pre-trained question-answering model from Hugging Face
@st.cache_resource
def load_qa_pipeline():
    return pipeline("question-answering")

qa_pipeline = load_qa_pipeline()

# Function to get climate change data from external API
@st.cache_data
def get_climate_data(query):
    # Placeholder for climate data API; implement your desired API here
    return "This functionality is not implemented yet."

# Function to get weather data from OpenWeatherMap API
@st.cache_data
def get_weather_openweather(city_name):
    api_key = "542197954daaa02018e565e8db2e94f0"  # Your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The current weather in {city_name} is {weather} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't fetch the weather data. Please check the city name."

# Function to get weather data from Tomorrow.io API
@st.cache_data
def get_weather_tomorrowio(latitude, longitude):
    api_key = "ViNsx9F66SGCBTepCbONJo6YubFDIpFk"  # Your Tomorrow.io API key
    base_url = f"https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&apikey={api_key}"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        # Extract relevant information from the response
        weather_description = data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
        temperature = data['data']['timelines'][0]['intervals'][0]['values']['temperature']
        return f"The current weather is {weather_description} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't fetch the weather data. Please check the location coordinates."

# Initialize session state for conversation history and context memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# Input field for user to enter their question
prompt = st.chat_input("Ask a question about climate change or weather:")

# Immediately display user's question after input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    logging.info(f'User asked: {prompt}')

    # Determine if the query is a greeting
    if prompt.lower() in ["hello", "hi", "hey"]:
        answer = "Hello! How can I assist you with climate change or weather-related questions today?"

    # Handle weather-related question
    elif "weather" in prompt.lower():
        city_name = prompt.split("in")[-1].strip() if "in" in prompt.lower() else None
        if city_name:
            answer = get_weather_openweather(city_name)  # Use OpenWeather API
        else:
            answer = "Please specify a city."

    # Handle follow-up questions using previous context
    elif "which activities" in prompt.lower() or "what activities" in prompt.lower():
        if st.session_state.last_answer and "human activities" in st.session_state.last_answer:
            answer = "The main human activities that cause climate change include burning fossil fuels, deforestation, and industrial processes."
        else:
            answer = "Can you clarify your question?"

    # Handle climate-related questions using external API
    elif "climate" in prompt.lower() or "global warming" in prompt.lower():
        answer = get_climate_data(prompt)

    # Handle general climate-related questions using Hugging Face pipeline
    else:
        try:
            answer = qa_pipeline(question=prompt, context='Your context here')['answer']  # Add your context here
            if len(answer) < 5:  # If the answer seems too short, assume it's irrelevant
                answer = "I'm sorry, I couldn't find a relevant answer. Could you try rephrasing your question?"
        except Exception:
            answer = "I'm sorry, I don't have enough information to answer that right now. Could you rephrase your question?"

    # Store last answer in session state for context in future questions
    st.session_state.last_answer = answer

    # Append the assistant's response and display immediately
    st.session_state.messages.append({"role": "assistant", "content": answer})
    logging.info(f'Assistant answered: {answer}')
    with st.chat_message("assistant"):
        st.markdown(answer)
