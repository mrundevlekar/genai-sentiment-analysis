import streamlit as st
from groq_sentiment import GroqSentimentAnalyzer

# Initialize the sentiment analyzer
analyzer = GroqSentimentAnalyzer()

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="GenAI Sentiment Chatbot",
    page_icon="💬",
    layout="centered"
)

st.title("💬 GenAI Sentiment Analysis Chatbot")
st.write("Enter text below to get its sentiment analyzed (Positive, Negative, Neutral, Mixed).")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sentiment" in message:
            st.info(f"Sentiment: **{message['sentiment']}**")

# React to user input
if prompt := st.chat_input("Enter text for sentiment analysis..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing sentiment..."):
            # Get sentiment from our Groq analyzer
            sentiment_result = analyzer.analyze_sentiment(prompt)

            # Prepare assistant's response
            assistant_response = f"I've analyzed the sentiment of your text."
            st.markdown(assistant_response)
            st.info(f"Sentiment: **{sentiment_result}**")

            # Add assistant response and sentiment to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "sentiment": sentiment_result
            })

# st.sidebar.header("How it Works")
# st.sidebar.info(
#     "This chatbot uses Groq's high-speed inference engine with the Llama 3 8B model "
#     "to determine the sentiment of any text you provide. It categorizes sentiment "
#     "as Positive, Negative, Neutral, or Mixed."
# )

# st.sidebar.markdown("---")
# st.sidebar.write("Developed with ❤️ using Streamlit, Groq, and Python.")