from reportlab.lib.pagesizes import letter
import google.generativeai as genai
from reportlab.pdfgen import canvas
from fpdf import FPDF
import pandas as pd
import json
import os
import re


def generate_resume_content(job_title, job_description, skills, projects, experiences):
    resume_content = f"Job Title: {job_title}\n"
    resume_content += f"Job Description: {job_description}\n"
    resume_content += f"Skills: {', '.join(skills)}\n"
    resume_content += f"Projects: {projects}\n"

    resume_content += "Experience:\n"
    for exp in experiences:
        resume_content += f"- Company: {exp['company']}\n"
        resume_content += f"  Job Title: {exp['title']}\n"
        resume_content += f"  Duration: {exp['startDate']} - {exp['endDate']}\n"
        resume_content += f"  Description: {exp['description']}\n"

    # Call the AI API to improve the resume content
    improved_resume = call_ai_api(resume_content)

    return improved_resume

# Function to create a PDF with the resume content
def create_pdf(resume_content, pdf_path):
    # Extract content between <start> and <end> tags
    start_tag = "<start>"
    end_tag = "<end>"
    
    # Find the content between the start and end tags
    match = re.search(f'{re.escape(start_tag)}(.*?){re.escape(end_tag)}', resume_content, re.DOTALL)
    if match:
        content = match.group(1)  # Extracted content between <start> and <end>
        
        # Remove any '*' (used for bullet points) from the content
        content = content.replace('*', '')  # Removes the '*' symbols
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Set title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="Resume", ln=True, align='C')

        # Add resume content to the PDF
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(200, 10, txt=content)

        # Output the PDF to the given path
        pdf.output(pdf_path)
    else:
        print("Error: Content between <start> and <end> tags not found.")
    
    

api_key = "AIzaSyDHcWLsDv5REcL54DBAcdSiiQKqtgWeTIU""
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Function to call the AI API and process the resume data
def call_ai_api(resume_content):
    # Define the refined prompt that follows the format for resume content
    prompt = """
    <start>
    Write the resume content following the structure provided below. Use the tags <start> to begin the resume content and <end> to mark the end of the actual resume content. Ensure clarity, conciseness, and eliminate unnecessary details. Focus on quantifiable achievements and use specific technologies. The content should follow this exact order:

    1. **Summary/Profile:** A brief, impactful statement showcasing key strengths, experience, and motivation.
    2. **Skills:** A categorized list of relevant skills (e.g., programming languages, tools, development methodologies).
    3. **Projects:** A description of key projects, including technologies used and quantifiable outcomes where applicable.
    4. **Experience:** A clear listing of key responsibilities and accomplishments from previous roles, emphasizing impact and specific contributions.

    Avoid redundancy, keep the tone professional, and focus on providing clear, direct language. Do not include unnecessary introductory text or formatting.

    <end>
    """
    
    # Add the resume content provided by the user to the prompt
    user_message = "Please follow the instructions in the prompt and generate the resume content as specified:\n" + prompt + resume_content
    
    # Start a chat session using the model API and send the prompt along with the user message
    chat_session = model.start_chat(
        history=[{
            "role": "user",
            "parts": [user_message]
        }]
    )
    
    # Send the message and get the response
    response = chat_session.send_message(user_message)
    
    return response.text

