import PyPDF2
import re

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def preprocess_content(content):
    """Preprocess content by cleaning and converting to lowercase."""
    content = re.sub(r'\s+', ' ', content)  # Remove extra spaces
    return content.lower()

def find_answer(question, content):
    """Find the answer to a user's question from the extracted content."""
    question = preprocess_content(question)
    content = preprocess_content(content)
    
    # Attempt keyword matching
    words = question.split()
    for word in words:
        if word in content:
            # Get relevant sentence
            sentences = re.split(r'[.?!]', content)
            for sentence in sentences:
                if word in sentence:
                    return sentence.strip()
    
    return "I don't have this information."

def main():
    pdf_path = input("Enter the path to the PDF document: ")
    content = extract_text_from_pdf(pdf_path)
    
    if not content:
        print("Failed to extract text from the PDF.")
        return
    
    print("\nPDF content successfully loaded. You can now ask questions.")
    
    while True:
        user_question = input("\nEnter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            print("Goodbye!")
            break
        
        answer = find_answer(user_question, content)
        print("\n", answer)

if __name__ == "__main__":
    main()
