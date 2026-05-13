import os
import re

from fpdf import FPDF

try:
    import google.generativeai as genai
except Exception:
    genai = None


def _build_resume_text(job_title, job_description, skills, projects, experiences):
    lines = [
        "Summary/Profile",
        f"Target Role: {job_title}",
        f"Profile: {job_description}",
        "",
        "Skills",
        ", ".join(skills or []) if skills else "No skills provided",
        "",
        "Projects",
        projects if projects else "No projects provided",
        "",
        "Experience",
    ]

    for exp in experiences or []:
        lines.extend(
            [
                f"Company: {exp.get('company', '')}",
                f"Role: {exp.get('title', '')}",
                f"Duration: {exp.get('startDate', '')} - {exp.get('endDate', '')}",
                f"Details: {exp.get('description', '')}",
                "",
            ]
        )

    return "\n".join(lines).strip()


def generate_resume_content(job_title, job_description, skills, projects, experiences):
    base_resume = _build_resume_text(
        job_title=job_title,
        job_description=job_description,
        skills=skills,
        projects=projects,
        experiences=experiences,
    )
    return call_ai_api(base_resume)


def create_pdf(resume_content, pdf_path):
    start_tag = "<start>"
    end_tag = "<end>"
    match = re.search(
        f"{re.escape(start_tag)}(.*?){re.escape(end_tag)}",
        resume_content,
        re.DOTALL,
    )
    content = match.group(1).strip() if match else resume_content.strip()
    content = content.replace("*", "")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Resume", ln=True, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, txt=content)
    pdf.output(pdf_path)


def call_ai_api(resume_content):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or genai is None:
        return f"<start>\n{resume_content}\n<end>"

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.6"))
    top_p = float(os.getenv("GEMINI_TOP_P", "0.95"))
    top_k = int(os.getenv("GEMINI_TOP_K", "40"))
    max_output_tokens = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "2048"))

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "text/plain",
        },
    )

    prompt = (
        "Rewrite this resume draft with concise professional language. "
        "Return only resume text wrapped in <start> and <end> tags.\n\n"
        f"{resume_content}"
    )
    response = model.generate_content(prompt)
    text = response.text if response and getattr(response, "text", None) else ""
    return text.strip() if text.strip() else f"<start>\n{resume_content}\n<end>"
