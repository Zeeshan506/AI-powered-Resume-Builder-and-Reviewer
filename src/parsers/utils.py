import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
import PyPDF2
import docx
import pandas as pd
import string, time


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
        cleaned_text = text.str.lower()
        cleaned_text = cleaned_text.apply(remove_html_tags)
        cleaned_text = cleaned_text.apply(remove_punctuation)
        cleaned_text = cleaned_text.apply(remove_urls)
        cleaned_text = cleaned_text.apply(remove_stopwords)
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