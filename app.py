import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API key
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Streamlit function
def chat_with_groq(message, history):
    # Conversation history
    messages = [{
        "role": "system",
        "content": ("You are my cringey boyfriend who likes to give me advice about text messages"
                    "(and only text messages/situations). You are not possessive, as in you will help me respond how I want to any type of message "
                    "(even ones asking me out). You are also curious about the context of my texts and will help me respond accordingly. "
                    "Your name is pixel prince and I am a queen or princess to you but make sure to stay gender neutral (you could still call me princess and queen though)."
                    " You don’t judge me negatively based on my responses but you could judge others.")}]

    # Add the latest user message to the conversation history
    for entry in history:
        if isinstance(entry, dict) and "role" in entry and "content" in entry:
            messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": message})

    # Call LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=512,
    )

    # Get the AI response
    ai_message = response.choices[0].message.content
    return ai_message

# Initial message from AI
initial_msg = {
    "role": "assistant",
    "content": "Hello, I’m your Pixel Prince, here at your service.\n"
    "Allow me to assist you with your difficult texting conversation, you know I’m always here for you."
}

# Set up Streamlit interface
if 'history' not in st.session_state:
    st.session_state.history = [initial_msg]  # Initialize chat history

# Display the chat history with alignment
for message in st.session_state.history:
    if message["role"] == "assistant":
        # Left-aligned AI message
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("jaan.jpg", width=50)  # add pfp
        with col2:
            # Display AI name above the message
            st.markdown(f"<div style='text-align: left; font-weight: bold;'>Pixel Prince</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: left;'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        # Right-aligned user message
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"<div style='text-align: right; font-weight: bold;'>You</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: right;'>{message['content']}</div>", unsafe_allow_html=True)
        with col2:
            # Leave the second column empty
            pass

# User input
message = st.text_input("Your message:")

# Handle button click to send message
if st.button("Send"):
    if message:
        # Add user message to history
        st.session_state.history.append({"role": "user", "content": message})

        # Get AI response
        ai_message = chat_with_groq(message, st.session_state.history)

        # Add AI response to history
        st.session_state.history.append({"role": "assistant", "content": ai_message})

        # Refresh the page to show new message
        st.rerun()