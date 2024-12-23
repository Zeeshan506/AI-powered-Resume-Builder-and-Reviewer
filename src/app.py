from parsers.resume_reviewer import process_resume,calculate_skill_score
from parsers.utils import generate_unique_filename # Ensure this function exists
from Builder.resume_builder import generate_resume_content, create_pdf
from flask import Flask, render_template, request, jsonify,send_from_directory,send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import json
import os
import time



dataset_path = pd.read_csv(r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\data\Preprocessing\final_merged_data.csv')
UPLOAD_FOLDER = r'C:\Users\DELL\Desktop\Projects\DataScience\AI-powered-Resume-Builder-and-Reviewer\src\data\generated_resumes'




app = Flask(__name__, template_folder='templates', static_folder='static')

    
# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = './data/resumes'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        print(f"File saved at {file_path}")

        try:
            # Process the resume and get preprocessed file path
            file_path_1 = process_resume(file_path)
            # Call the skill calculation function, which also returns other scores
            scores = calculate_skill_score(file_path_1, job_title)
            
            # Return the breakdown of scores as a JSON response
            return jsonify({
                'skill_score': scores['skill_score'],
                'tone_score': scores['tone_score'],
                'grammar_score': scores['grammar_score'],
                'clarity_score': scores['clarity_score'],
                'projet_score': scores['project_score'],
                'experience_score': scores['experience_score'],
                'total_score': scores['total_score']
                
            })
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



@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        # Get the data sent from the frontend
        data = request.get_json()
        print("Received data:", data)  # Debugging log

        job_title = data.get('jobTitle')
        job_description = data.get('jobDescription')
        skills = data.get('skills')
        projects = data.get('projects')
        experiences = data.get('experiences')

        # Check if the necessary data is provided
        if not job_title or not job_description or not experiences:
            return jsonify({"success": False, "error": "Job title, description, or experiences missing."})

        # Generate the content for the resume
        resume_content = generate_resume_content(job_title, job_description, skills, projects, experiences)

        # Create the PDF
        pdf_filename = f'resume_{int(time.time())}.pdf'
        pdf_path = os.path.join('data', 'generated_resumes', pdf_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Generate the PDF
        create_pdf(resume_content, pdf_path)

        # Return a success response with the URL for the generated PDF
        return jsonify({"success": True, "pdf_url": f"/download/{pdf_filename}"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('data', 'generated_resumes', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"success": False, "error": "File not found"}), 404


    
if __name__ == '__main__':
    app.run(debug=True)
