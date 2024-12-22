import os
from parsers.utils import extract_text_from_pdf, preprocess_text, get_matching_skills, read_text_file,is_passive
import pandas as pd
import joblib
import language_tool_python
import textstat
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')



model_path = r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\src\parsers\retrained_old_model.pkl'
vectorizer_path = r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\src\parsers\tfidf_vectorizer.pkl'


old_model = joblib.load(model_path)
old_vectorizer = joblib.load(vectorizer_path)
    

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
    path = f"{output_file}"
    return path

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
            path = save_parsed_data(cleaned_text, os.path.basename(file_path))
            return path
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



# Function to calculate the skill score and tone score based on the resume
def calculate_skill_score(file_path, job_title):
    """
    Calculates the skill score based on the user's resume and the selected job title.
    Also calculates the tone, grammar, and clarity scores and adds them to the total.

    :param file_path: Path to the user's resume file.
    :param job_title: The selected job title to fetch the relevant skills.
    :return: A dictionary containing individual scores and the total score.
    """
    try:
        # Fetch the list of skills related to the selected job title
        skills = get_matching_skills(job_title)
        
        if not skills:
            return {
                'skill_score': 0,
                'tone_score': 0,
                'grammar_score': 0,
                'clarity_score': 0,
                'total_score': 0
            }

        skill_score = 0
        skill_count = 0

        # Read the resume text
        resume_text = read_text_file(file_path)
        resume_words = set(resume_text.lower().split())

        # Calculate the skill score
        for skill in skills:
            skill = skill.strip().lower()
            if skill in resume_words:
                skill_count += 1
                skill_score += 20 + (skill_count - 1) * 5  # Base score of 20, plus 5 for each additional match

                # Ensure the score doesn't exceed 50
                if skill_score > 50:
                    skill_score = 50
                    break

        # Calculate the tone score
        predicted_tone = check_tone_of_resume(resume_text)

        if predicted_tone == 'Regular':
            tone_score = 10
        elif predicted_tone == 'Formal':
            tone_score = 12
        elif predicted_tone == 'Professional':
            tone_score = 13
        else:
            tone_score = 0  # In case of an unknown tone

        error_count, error_details = check_grammar_of_resume(resume_text)
        grammar_score = max(4, 5 - error_count)  # Deduct points for errors, up to 10
        clarity_score = calculate_clarity_score(resume_text)  # Returns a score out of 15
        project_score = calculate_project_score(resume_text) # Returns a score out of 5
        experience_score= calculate_experience_score(resume_text) # Returns a score out of 5
        total_score = skill_score + tone_score + grammar_score + clarity_score + project_score + experience_score

        print (f"""
            'skill_score': {skill_score},
            'tone_score': {tone_score},
            'grammar_score': {grammar_score},
            'clarity_score': {clarity_score},
            'project_score': {project_score},
            'experience_score': {experience_score},
            'total_score': {total_score}
        """)
        # Return the result as a dictionary
        return {
            'skill_score': skill_score,
            'tone_score': tone_score,
            'grammar_score': grammar_score,
            'clarity_score': clarity_score,
            'project_score': project_score,
            'experience_score': experience_score,
            'total_score': total_score,
        }

    except Exception as e:
        print(f"Error calculating skill score: {e}")
        return {
            'skill_score': 0,
            'tone_score': 0,
            'grammar_score': 0,
            'clarity_score': 0,
            'project_score': 0,
            'experience_score': 0,
            'total_score': 0,
        }



def check_tone_of_resume(resume_text):
    # Preprocess the resume text
    cleaned_text = preprocess_text(resume_text)
    
    # Vectorize the cleaned text
    X_tfidf = old_vectorizer.transform([cleaned_text])
    
    # Predict the tone using the retrained model
    predicted_tone = old_model.predict(X_tfidf)[0]  # Predict the tone for the resume text
    
    return predicted_tone



def check_grammar_of_resume(resume_text):
    # Initialize the language tool (English)
    tool = language_tool_python.LanguageTool('en-US')
    
    # Check the text for grammar mistakes
    matches = tool.check(resume_text)
    
    # If there are grammar issues, return the number of errors and a list of issues
    if matches:
        errors = []
        for match in matches:
            errors.append({
                'message': match.message,
                'context': match.context,
                'replacements': match.replacements,
                'offset': match.offset
            })
        return len(errors), errors  # Return number of errors and details
    else:
        return 0, []  # No errors found


        
        
def calculate_clarity_score(resume_text):
    """
    Calculates clarity score based on readability and the percentage of passive voice.

    :param resume_text: The text of the resume.
    :return: The clarity score.
    """
    # Calculate Flesch Reading Ease Score
    reading_score = textstat.flesch_reading_ease(resume_text)
    
    # Tokenize sentences to analyze passive voice
    sentences = sent_tokenize(resume_text)
    passive_count = sum(1 for sentence in sentences if is_passive(sentence))
    
    # Determine percentage of passive voice
    passive_percentage = (passive_count / len(sentences)) * 100 if sentences else 0

    # Scoring based on readability and passive voice
    clarity_score = 15  # Start with full score
    if reading_score < 50:
        clarity_score = 5
    elif reading_score < 70:
        clarity_score = 10
    
    # Penalize for excessive passive voice
    if passive_percentage > 20:
        clarity_score -= 2  # Deduct points for excessive passive voice usage

    return max(clarity_score, 7)  # Ensure score doesn't go negative


def calculate_project_score(resume_text):
    # Define the keywords related to "projects"
    project_keywords = ['project', 'projects','personal projects']

    # Check if any of the keywords appear in the resume text (case insensitive)
    if any(keyword.lower() in resume_text.lower() for keyword in project_keywords):
        return 5  # Award 5 marks if projects are mentioned
    else:
        return 1  # No marks if no relevant keywords are found


def calculate_experience_score(resume_text):
    # Define the keywords related to "experience" or "jobs"
    experience_keywords = ['experience', 'experiences', 'job', 'jobs']

    # Check if any of the keywords appear in the resume text (case insensitive)
    if any(keyword.lower() in resume_text.lower() for keyword in experience_keywords):
        return 5  # Award 5 marks if experience-related keywords are mentioned
    else:
        return 3  # No marks if no relevant keywords are found
