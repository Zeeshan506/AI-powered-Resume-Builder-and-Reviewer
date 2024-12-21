from flask import Flask, render_template, request, jsonify
import os
from parsers.resume_reviewer import process_resume,calculate_skill_score
from parsers.utils import generate_unique_filename # Ensure this function exists
import pandas as pd

dataset_path = pd.read_csv(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\Preprocessing\final_merged_data.csv')



app = Flask(__name__, template_folder='templates', static_folder='static')


    
# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = './data/resumes'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clean_skills(skill):
    # Split by comma and trim extra spaces
    return [s.strip() for s in skill.split(',')]

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Renders the index.html file from the templates folder
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    job_title = request.form.get('job_title')  # Get the job title from the form data

    if not job_title:
        return jsonify({'error': 'Job title not provided'}), 400

    if file and allowed_file(file.filename):
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved{file_path}")

        try:
            # Process the resume and get preprocessed file path
            file_path_1 = process_resume(file_path)
            # Call the scoring function with the job title
            score = calculate_skill_score(file_path_1, job_title)
            return jsonify({'score': score})
        except Exception as e:
            print(f"Error processing file: {e}")
            return jsonify({'error': 'Failed to process resume'}), 500

    return jsonify({'error': 'Invalid file type'}), 400






@app.route('/get_skills_by_prefix', methods=['GET'])
def get_skills_by_prefix():
    search_term = request.args.get('search_term', '').strip().lower()
    if not search_term:
        return jsonify({"skills": []})

    try:
        # Load dataset and process skills
        data = pd.read_csv(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\Preprocessing\Simplified.csv')
        all_skills = data['skill'].dropna().str.strip().unique().tolist()
        all_skills = [skill for skill in all_skills if skill]  # Filter out empty skills

        # Create a prefix dictionary
        prefix_dict = {}
        for skill in all_skills:
            for i in range(1, len(skill) + 1):
                prefix = skill[:i].lower()
                if prefix not in prefix_dict:
                    prefix_dict[prefix] = set()  # Use a set to ensure uniqueness
                if len(prefix_dict[prefix]) < 100:
                    prefix_dict[prefix].add(skill)

        # Get matching skills for the current prefix
        matching_skills = sorted(list(prefix_dict.get(search_term, [])))[:100]
        return jsonify({"skills": matching_skills})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def load_job_titles():
    # Assuming you have a CSV file with a 'job_title' column
    df = pd.read_csv(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\Preprocessing\Simplified.csv')
    return df['job_title'].dropna().unique().tolist()  # Ensure no nulls and unique titles

@app.route('/get_job_titles', methods=['GET'])
def get_job_titles():
    try:
        job_titles = load_job_titles()
        return jsonify({"job_titles": job_titles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
    
if __name__ == '__main__':
    app.run(debug=True)
