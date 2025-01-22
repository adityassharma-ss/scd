import requests
from bs4 import BeautifulSoup
import random
import re

def fetch_content(url):
    """Fetch and clean content from a URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    # Clean and return content
    return re.sub(r'\s+', ' ', text).strip()

def generate_questions(content, num_questions, complexity, q_type, order):
    """Generate questions based on the given parameters."""
    sentences = content.split('. ')
    random.shuffle(sentences)
    
    # Filter sentences by complexity (e.g., based on length or keywords)
    if complexity == "easy":
        sentences = [s for s in sentences if len(s.split()) < 15]
    elif complexity == "hard":
        sentences = [s for s in sentences if len(s.split()) > 15]
    
    # Generate questions
    questions = []
    for i in range(min(num_questions, len(sentences))):
        sentence = sentences[i]
        question = f"Q{i + 1}: What is the main idea of this statement?\n - {sentence.strip()}"
        
        # Add options based on type
        if q_type in ["select", "both"]:
            options = [f"Option {chr(65 + j)}: {random.choice(sentences).strip()}" for j in range(3)]
            options.append(f"Option {chr(65 + len(options))}: {sentence.strip()}")
            random.shuffle(options)
            question += "\n" + "\n".join(options)
        
        if q_type == "multi-select":
            options = [f"Option {chr(65 + j)}: {random.choice(sentences).strip()}" for j in range(4)]
            question += "\n" + "\n".join(options)
        
        questions.append(question)
    
    # Sort questions by complexity if needed
    if order == "increasing":
        questions = sorted(questions, key=lambda x: len(x.split()))
    elif order == "decreasing":
        questions = sorted(questions, key=lambda x: len(x.split()), reverse=True)
    
    return questions

def main():
    # Sample input
    url = input("Enter the URL or Topic: ")
    num_questions = int(input("Number of questions: "))
    complexity = input("Complexity level (easy/medium/hard): ").lower()
    q_type = input("Type of questions (select/multi-select/both): ").lower()
    order = input("Order of complexity (none/increasing/decreasing): ").lower()
    
    # Fetch and process content
    content = fetch_content(url)
    questions = generate_questions(content, num_questions, complexity, q_type, order)
    
    # Display questions
    print("\nGenerated Questions:\n")
    for q in questions:
        print(q)
        print()

if __name__ == "__main__":
    main()
