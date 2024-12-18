import os
from utils import extract_text_from_pdf, preprocess_text

# Define paths
parsed_data_path = r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\parsed_data'

# Function to parse and preprocess the extracted text from a resume
def parse_resume(extracted_text):
    """Parse and preprocess extracted text from a resume."""
    print("Extracted text:\n", extracted_text)
    cleaned_text = preprocess_text(extracted_text)
    print("Cleaned text:\n", cleaned_text)
    return cleaned_text

# Function to save parsed data to a text file in the 'parsed_data' folder
def save_parsed_data(parsed_text, original_file_name):
    """Save parsed text into the parsed_data folder"""
    # Ensure the parsed_data directory exists
    if not os.path.exists(parsed_data_path):
        os.makedirs(parsed_data_path)
    
    # Create a new file name based on the original file name (without extension)
    base_name = os.path.splitext(original_file_name)[0]
    output_file = os.path.join(parsed_data_path, f"{base_name}_parsed.txt")
    
    # Write the parsed text to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(parsed_text)
    
    print(f"Parsed data saved to: {output_file}")

# Function to handle parsing and saving
def process_resume(file_path):
    """Main function to handle parsing and saving"""
    try:
        # Extract text only for .pdf files, assuming .pdf will always be sent
        if file_path.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
            # Preprocess the extracted text
            cleaned_text = preprocess_text(extracted_text)
            # Save the parsed text
            save_parsed_data(cleaned_text, os.path.basename(file_path))
            # print(f"Parsed and saved {file_path}")
            # print(cleaned_text)
        else:
            raise ValueError("Unsupported file type: Only PDF files should be processed at the backend.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all resumes in the 'resumes' folder
def process_resumes_in_folder(folder_path):
    """Process all resumes in the folder"""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.pdf'):  # Only process PDF files, no other type checks
            process_resume(file_path)

# Example usage: Process all resumes in the 'resumes' folder
process_resumes_in_folder(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\resumes')
