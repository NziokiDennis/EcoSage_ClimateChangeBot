import streamlit as st
from transformers import pipeline

# Title for the chatbot app
st.title("Welcome to EcoSage, your Climate Change Literacy Bot")

# Instructions
st.write("Ask me anything about climate change, sustainability, or environmental issues!")

# Load pre-trained question-answering model
qa_pipeline = pipeline("question-answering")

# Define a knowledge base for the chatbot to pull answers from
climate_context = """
Climate change refers to long-term shifts in temperatures and weather patterns, primarily due to human activities.
Burning fossil fuels like coal, oil, and gas has been the main driver of climate change since the 1800s. 
The effects include rising global temperatures, extreme weather events, and sea level rise.
Sustainable solutions like renewable energy, reducing carbon emissions, and reforestation are essential.
"""

# Get user input (the question they ask)
user_question = st.text_input("Ask a question about climate change:")

# If the user enters a question, process it
if user_question:
    # Get the answer from the pre-trained model based on the context
    answer = qa_pipeline(question=user_question, context=climate_context)
    # Display the answer
    st.write(f"Answer: {answer['answer']}")
