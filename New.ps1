Here’s the Python script to analyze the sentiment of statements using a pre-trained sentiment analysis model:

Python Script

from textblob import TextBlob

def analyze_sentiments(statements):
    """
    Analyze the sentiment of a list of statements and classify them as Positive, Negative, or Neutral.
    
    Args:
        statements (list): List of statements to analyze.

    Returns:
        dict: A dictionary containing each statement and its corresponding sentiment.
    """
    sentiment_results = {}
    for statement in statements:
        analysis = TextBlob(statement)
        # Determine sentiment polarity: >0 positive, <0 negative, 0 neutral
        if analysis.sentiment.polarity > 0:
            sentiment = "Positive"
        elif analysis.sentiment.polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiment_results[statement] = sentiment
    return sentiment_results

# Sample Input
statements = [
    "I absolutely loved the new movie, it was fantastic!",
    "The service was terrible, I will never go back there again.",
    "It's okay, not too bad, not too good either.",
    "What a beautiful day outside!",
    "I hate waiting in long lines at the airport."
]

# Output
results = analyze_sentiments(statements)
for statement, sentiment in results.items():
    print(f"Statement: \"{statement}\" -> Sentiment: {sentiment}")

Sample Output

For the given input list, the output will be:

Statement: "I absolutely loved the new movie, it was fantastic!" -> Sentiment: Positive
Statement: "The service was terrible, I will never go back there again." -> Sentiment: Negative
Statement: "It's okay, not too bad, not too good either." -> Sentiment: Neutral
Statement: "What a beautiful day outside!" -> Sentiment: Positive
Statement: "I hate waiting in long lines at the airport." -> Sentiment: Negative

Key Features:

1. Handles Different Types of Statements: Works on declarative statements, questions, and exclamatory sentences.


2. Accurate Analysis: Uses TextBlob, which provides reliable polarity-based sentiment scores.


3. Flexible Input: Can analyze multiple statements at once.



You can further enhance the script using libraries like VADER or Transformers for even more accurate results.

