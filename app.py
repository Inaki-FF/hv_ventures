import streamlit as st
import pandas as pd
from agent import ConversationalAgent
import os
os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"]
# Initialize the Excel agent
agent = ConversationalAgent()

# Streamlit UI
st.title("Chatbot UI")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# Chat input
user_input = st.text_input("Hazme una pregunta: ", "")

if st.button("Send"):
    if user_input:

        
        # Simulate bot response
        bot_response = agent.talk(user_input)
        
        # Store chat history in session state
        st.write(f"Response: {bot_response}")
        



