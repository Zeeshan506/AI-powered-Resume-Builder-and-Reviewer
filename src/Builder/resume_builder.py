from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import json
import os


def generate_resume_content(job_title, job_description, skills, projects, experiences):
    resume_content = f"Job Title: {job_title}\n\n"
    resume_content += f"Job Description: {job_description}\n\n"

    # Add skills section
    resume_content += "Skills:\n"
    if skills:
        resume_content += "\n".join(skills) + "\n"
    else:
        resume_content += "No skills listed.\n"

    # Add projects section
    resume_content += "\nProjects:\n"
    if projects:
        resume_content += f"{projects}\n"
    else:
        resume_content += "No projects listed.\n"

    # Add experiences section
    resume_content += "\nWork Experience:\n"
    if experiences:
        for exp in experiences:
            resume_content += f"Company: {exp['companyName']}\n"
            resume_content += f"Job Title: {exp['jobTitle']}\n"
            resume_content += f"Duration: {exp['duration']}\n"
            resume_content += f"Description: {exp['description']}\n\n"
    else:
        resume_content += "No experiences listed.\n"
    
    return resume_content

# Function to create a PDF with the resume content
def create_pdf(content, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    text_object = c.beginText(100, 750)
    text_object.textLines(content)
    c.drawText(text_object)
    c.save()