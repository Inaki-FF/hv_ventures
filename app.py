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
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Append user message to chat history
        agent.insert_chat(user_input, "")
        
        # Simulate bot response
        bot_response = agent.talk(user_input)
        
        # Append bot response to chat history
        agent.insert_chat("", bot_response)
        
        # Store chat history in session state
        st.session_state['responses'].append({"user": user_input, "bot": bot_response})
        
        # Clear user input
        user_input = ""

# Display chat history
if st.session_state['responses']:
    for response in st.session_state['responses']:
        st.write(f"You: {response['user']}")
        st.write(f"Bot: {response['bot']}")


