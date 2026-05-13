import re
import csv
from pathlib import Path
import PyPDF2
import docx
import string
import os
import time


exclude = string.punctuation
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SIMPLIFIED_DATASET_PATH = PROJECT_ROOT / "data" / "Preprocessing" / "Simplified.csv"


def lemmatize_text(words):
    return words

def extract_email(text):
    """
    Extracts email addresses from the given text.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)  # Find all email addresses

def extract_phone_number(text):
    """
    Extracts phone numbers from the given text.
    """
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(phone_pattern, text)  # Find all phone numbers

def remove_non_alphanumeric(text):
    """
    Removes non-alphanumeric characters from the text.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    """Extract text from DOCX"""
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return preprocess_text(text)



def preprocess_text(text):
    try:
        # Convert text to lowercase
        cleaned_text = (text or "").lower()

        # Remove HTML tags
        cleaned_text = remove_html_tags(cleaned_text)

        # Remove punctuation
        cleaned_text = remove_punctuation(cleaned_text)

        # Remove URLs
        cleaned_text = remove_urls(cleaned_text)

        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    except Exception as e:
        print(f"Error occurred while preprocessing text: {e}")
        return text
    
    return cleaned_text




def remove_html_tags(text):
    pattern = re.compile('<.*?>')
    return pattern.sub(r'',text)

def remove_urls(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'',text)

def remove_punctuation(text):
    return text.translate(str.maketrans('','',exclude))

def remove_stopwords(text):
    return text



def get_matching_skills(job_title):
    """
    Fetches matching skills based on the given job title from the dataset.

    :param job_title: Job title string to search in the dataset.
    :return: List of skills related to the job title.
    """
    try:
        if not SIMPLIFIED_DATASET_PATH.exists():
            return []
        with SIMPLIFIED_DATASET_PATH.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            all_skills = []
            for row in reader:
                row_title = (row.get("job_title") or "").strip().lower()
                if row_title != job_title.lower():
                    continue
                skills_blob = row.get("skill", "")
                all_skills.extend([s.strip() for s in skills_blob.split(",") if s.strip()])
        return list(set(all_skills))
    except Exception as e:
        print(f"Error fetching matching skills: {e}")
        return []
    

def read_text_file(file_path):
    """
    Reads and returns the content of a text file.

    :param file_path: Path to the text file to read.
    :return: The content of the text file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""




def generate_unique_filename(original_filename):
    # Extract the file extension
    _, file_extension = os.path.splitext(original_filename)
    
    # Create a unique identifier based on the current timestamp
    timestamp = int(time.time())
    
    # Construct the new filename
    new_filename = f"resume_{timestamp}{file_extension}"
    
    return new_filename

def is_passive(sentence):
    """
    Basic function to detect passive voice in a sentence.

    :param sentence: A sentence to check for passive voice.
    :return: True if the sentence contains passive voice, otherwise False.
    """
    passive_markers = ["is", "was", "were", "be", "been", "being"]
    words = sentence.lower().split()
    return any(marker in words for marker in passive_markers) and "by" in words
