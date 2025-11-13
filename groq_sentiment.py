# groq_sentiment.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqSentimentAnalyzer:
    def __init__(self):
        # Check if API key is loaded
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("ERROR: GROQ_API_KEY environment variable not found!")
            # You might want to raise an error here or handle it
            raise ValueError("GROQ_API_KEY is not set.")
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.1-8b-instant"

    # ... rest of your class ...

    def analyze_sentiment(self, text: str) -> str:
        # ... (initial checks) ...

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a highly accurate sentiment analysis assistant. "
                            "Analyze the sentiment of the following text and return ONLY one of these labels: "
                            "'Positive', 'Negative', 'Neutral', or 'Mixed'. "
                            "Do not include any other text, explanations, or punctuation. "
                            "For example: 'Positive' or 'Negative'."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the sentiment of this text: '{text}'"
                    }
                ],
                model=self.model_name,
                temperature=0.0, # Keep temperature low for consistent sentiment output
                max_tokens=10 # We only expect a short response
            )# ... (messages, model, temperature, max_tokens) ...
            sentiment_label = chat_completion.choices[0].message.content.strip()

            valid_sentiments = ["Positive", "Negative", "Neutral", "Mixed"]
            if sentiment_label in valid_sentiments:
                return sentiment_label
            else:
                print(f"Warning: Groq returned unexpected sentiment '{sentiment_label}'. Defaulting to Neutral for text: '{text}'")
                return "Neutral"

        except Exception as e:
            # IMPORTANT: Print the full exception for debugging
            print(f"Error analyzing sentiment for text '{text}' with Groq: {e}")
            import traceback
            traceback.print_exc() # This will print the full stack trace
            return "Error"

if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")
    print(f"Does .env exist in current directory? {os.path.exists('.env')}")
    print(f"Value of GROQ_API_KEY before init: {os.environ.get('GROQ_API_KEY')}") # Should be None if not loaded yet

    try:
        analyzer = GroqSentimentAnalyzer()
        # This line will only print if the analyzer initializes successfully
        print(f"API Key loaded for client: {analyzer.client.api_key[:5]}...{analyzer.client.api_key[-5:]}") # Print only parts of the key for security
    except ValueError as e:
        print(f"Initialization Error: {e}")
        exit() # Exit if key is not found

    texts_to_analyze = [
        "I absolutely love this product! It's fantastic.",
        "This is the worst customer service I have ever experienced.",
        "The weather is quite mild today.",
        "I like some parts, but other parts are really bad.",
        "The movie was okay, but the ending was terrible."
    ]

    for text in texts_to_analyze:
        print(f"\nAnalyzing: '{text}'") # Added more verbose output
        sentiment = analyzer.analyze_sentiment(text)
        print(f"Result: {sentiment}")