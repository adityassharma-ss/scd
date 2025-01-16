To generate Meeting Minutes (MOM) and Action Items from a meeting transcript, we can use natural language processing (NLP) techniques to extract important information such as discussions, decisions, and action items.

Approach:

1. Extract text from the transcript: We need to read the transcript, which could be in a PDF or text format. We'll use PyPDF2 for PDF files and simple file reading for text files.


2. Identify key discussions: Use NLP tools like spaCy or nltk to identify action items, deliverables, and other important details like tasks, decisions, and owners.


3. Format the output: Generate structured MOM (Minutes of Meeting) and list the action items.



Here is an implementation of the solution:

import re
import PyPDF2
import spacy
from collections import defaultdict

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def extract_mom_and_actions(transcript_text):
    mom = []
    action_items = []

    # Process text using spaCy
    doc = nlp(transcript_text)

    for sent in doc.sents:
        # Example logic for detecting action items (simple keyword-based)
        if 'action item' in sent.text.lower() or 'deliverable' in sent.text.lower() or 'task' in sent.text.lower():
            action_items.append(sent.text.strip())
        else:
            mom.append(sent.text.strip())

    return mom, action_items

def process_transcript(pdf_path):
    transcript_text = extract_text_from_pdf(pdf_path)
    mom, action_items = extract_mom_and_actions(transcript_text)

    print("Minutes of Meeting (MOM):\n")
    for item in mom:
        print(f"- {item}")

    print("\nAction Items:\n")
    for action in action_items:
        print(f"- {action}")

pdf_path = 'path_to_transcript.pdf'  # Replace with actual transcript path
process_transcript(pdf_path)

Explanation:

1. extract_text_from_pdf: Extracts text from the given PDF file using the PyPDF2 library.


2. extract_mom_and_actions: Uses the spaCy NLP model to process the transcript and identify key sentences related to MOM and action items. It checks for keywords like 'action item', 'deliverable', and 'task' to identify action items.


3. process_transcript: The main function that extracts text from the PDF and processes it to generate MOM and action items. The output is printed to the console.



Notes:

Keywords for Action Items: The script uses simple keyword-based detection to identify action items, but you can further refine this by using more sophisticated NLP techniques like dependency parsing, named entity recognition (NER), and task-related verb patterns.

Transcript Format: This solution assumes the transcript is relatively structured. If the transcript is not structured (e.g., contains unstructured chat dialogue), further preprocessing (like speaker identification or sentence segmentation) would be needed.

spaCy: You need to install the spaCy model before using the script:

pip install spacy
python -m spacy download en_core_web_sm


Libraries Needed:

PyPDF2 for PDF text extraction

spaCy for natural language processing


You can also modify this approach for different formats, such as plain text, by simply changing the input handling logic.


