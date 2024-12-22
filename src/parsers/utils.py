import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
import PyPDF2
import docx
import pandas as pd
import string, time
import os
import time


exclude = string.punctuation
lemmatizer = WordNetLemmatizer()


def lemmatize_text(words):
    """
    Lemmatizes a list of words to their root form.
    """
    return [lemmatizer.lemmatize(word) for word in words]  # Lemmatize each word

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
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    """Extract text from DOCX"""
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    text = text.apply(preprocess_text)
    return text



def preprocess_text(text):
    try:
        # Convert text to lowercase
        cleaned_text = text.lower()

        # Remove HTML tags
        cleaned_text = remove_html_tags(cleaned_text)

        # Remove punctuation
        cleaned_text = remove_punctuation(cleaned_text)

        # Remove URLs
        cleaned_text = remove_urls(cleaned_text)

        # Remove stopwords
        cleaned_text = remove_stopwords(cleaned_text)

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
    new_text = []
    for word in text.split():
        if word in stopwords.words('english'):
            new_text.append('')
        else:
            new_text.append(word)
    x = new_text[:]
    new_text.clear()
    return " ".join(x)



def get_matching_skills(job_title):
    """
    Fetches matching skills based on the given job title from the dataset.

    :param job_title: Job title string to search in the dataset.
    :return: List of skills related to the job title.
    """
    try:
        # Load the preprocessed skills dataset
        df = pd.read_csv(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\Preprocessing\Simplified.csv')
        
        # Filter the dataset for the given job title and extract the skills
        job_data = df[df['job_title'].str.lower() == job_title.lower()]
        
        # If matching rows are found, extract the skills from all rows
        if not job_data.empty:
            skills_list = job_data['skill'].tolist()
            all_skills = []
            for skills in skills_list:
                all_skills.extend(skills.split(','))  # Add all skills from the rows to the list
            
            return list(set(all_skills))  # Return unique skills as a list
        else:
            return []  # Return empty list if no match is found
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
