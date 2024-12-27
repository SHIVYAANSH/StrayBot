import spacy
import streamlit as st
import google.generativeai as genai

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Configure the API key
genai.configure(api_key="AIzaSyA9K-18UsgQIq4pPmkPx6QW8Q5hjYG4Pdw")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

# Streamlit app
st.title('StrayBot')

# Sidebar for additional information
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Enhanced function to detect identity-related questions
def detect_identity_question(user_input):
    doc = nlp(user_input)

    # List of key phrases or words to detect identity-related intent
    identity_keywords = ["who", "what", "where", "how", "creator", "developer", "made", "from", "google", "built", "company", "team",'product']

    # Checking for patterns
    for token in doc:
        # Match keywords for identity-related questions
        if token.lemma_ in identity_keywords:
            # Look for common question structures
            if token.pos_ in ["VERB", "PROPN"] and token.dep_ in ["nsubj", "dobj"]:
                return True

    # Check for named entities (e.g., Google, companies)
    for ent in doc.ents:
        if ent.label_ == "ORG" and ("Google" in ent.text or "Salwan Technnovation" in ent.text):
            return True

    # Additional check for common identity question structures
    if doc[0].text.lower() in ["who", "what", "which"] and doc[1].dep_ in ["nsubj", "dobj"]:
        return True

    return False

# Display previous chat history
for message in st.session_state.chat_history:
    if message.startswith("You:"):
        st.markdown(f"<div style='background-color: #FFC107; color: white; padding: 10px; border-radius: 20px; margin-bottom: 10px; word-wrap: break-word;'>{message}</div>", unsafe_allow_html=True)
    elif message.startswith("AI:"):
        st.markdown(f"<div style='background-color: #FFECB3; color: #333; padding: 10px; border-radius: 20px; margin-bottom: 10px; word-wrap: break-word;'>{message}</div>", unsafe_allow_html=True)

# Input field for user query
user_input = st.text_area("Enter your question:", "", height=100)

# Button to send the query
if st.button('Send'):
    if user_input:
        with st.spinner('Generating response...'):
            try:
                # Add the user input to the chat history
                st.session_state.chat_history.append(f"You: {user_input}")

                # Detect identity-related questions
                if detect_identity_question(user_input):
                    response_text = ("I am StrayBot, a part of the StrayCare app developed by the Salwan Technnovation team. "
                                     "I am here to help with any questions related to our app and the care of stray animals. "
                                     "Feel free to ask about how the app works or any issues you're facing with stray animals! "
                                     "Here's a friendly picture of a stray animal to brighten your day! 🐶")
                    st.session_state.chat_history.append(f"AI: {response_text}")
                else:
                    # Normal AI response
                    response = chat_session.send_message(user_input)
                    st.session_state.chat_history.append(f"AI: {response.text}")

                # Show response in the chat interface
                st.markdown(f"<div style='background-color: #FFECB3; color: #333; padding: 10px; border-radius: 20px; margin-bottom: 10px; word-wrap: break-word;'>{response_text if detect_identity_question(user_input) else response.text}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a question!")

# Custom CSS for design (creative enhancements)
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-image: url(''); 
            background-size: cover;
            background-position: center;
            color: #333;
        }
        .stTextInput textarea {
            font-size: 1.2rem;
            padding: 10px;
            border-radius: 20px;
            border: 1px solid #FFC107;
            background-color: #FFECB3;
        }
        .stButton button {
            background-color: #FF9800;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #FB8C00;
        }
        .stMarkdown {
            word-wrap: break-word;
        }
        .stTextInput {
            position: fixed;
            bottom: 10px;
            width: 100%;
            left: 0;
            padding: 10px;
            background-color: white;
            z-index: 10;
        }
        .stContainer {
            overflow-y: auto;
            max-height: 80vh;
            padding-bottom: 50px;
            margin-top: 50px;
        }
        .stSpinner {
            color: #FF9800;
        }
        .stTitle {
            text-align: center;
            font-size: 2.5rem;
            color: #FF9800;
        }
    </style>
""", unsafe_allow_html=True)
