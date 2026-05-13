import os
import time
import csv
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from Builder.resume_builder import create_pdf, generate_resume_content
from parsers.resume_reviewer import calculate_skill_score, process_resume
from parsers.utils import generate_unique_filename

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
SIMPLIFIED_CSV = DATA_DIR / "Preprocessing" / "Simplified.csv"
UPLOAD_FOLDER = DATA_DIR / "resumes"
GENERATED_FOLDER = DATA_DIR / "generated_resumes"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
GENERATED_FOLDER.mkdir(parents=True, exist_ok=True)

_skills_rows = None


def _load_skills_data():
    global _skills_rows
    if _skills_rows is not None:
        return _skills_rows
    if not SIMPLIFIED_CSV.exists():
        _skills_rows = []
        return _skills_rows
    with SIMPLIFIED_CSV.open("r", encoding="utf-8", newline="") as csv_file:
        _skills_rows = list(csv.DictReader(csv_file))
    return _skills_rows


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    job_title = (request.form.get("job_title") or "").strip()
    if not job_title:
        return jsonify({"error": "Job title not provided"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_FOLDER / filename
    file.save(file_path)

    try:
        parsed_path = process_resume(str(file_path))
        scores = calculate_skill_score(parsed_path, job_title)
        return jsonify(scores)
    except Exception as exc:
        return jsonify({"error": f"Failed to process resume: {exc}"}), 500


@app.route("/get_skills_by_prefix", methods=["GET"])
def get_skills_by_prefix():
    search_term = request.args.get("search_term", "").strip().lower()
    if not search_term:
        return jsonify({"skills": []})

    rows = _load_skills_data()

    all_skills = []
    for row in rows:
        skill_blob = row.get("skill", "")
        all_skills.extend([s.strip() for s in str(skill_blob).split(",") if s.strip()])
    unique_skills = sorted(set(all_skills))
    matching = [skill for skill in unique_skills if skill.lower().startswith(search_term)][:100]
    return jsonify({"skills": matching})


@app.route("/get_job_titles", methods=["GET"])
def get_job_titles():
    rows = _load_skills_data()
    titles = sorted(
        set(
            row.get("job_title", "").strip()
            for row in rows
            if row.get("job_title", "").strip()
        )
    )
    return jsonify({"job_titles": [t for t in titles if t]})


@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json(silent=True) or {}
    job_title = (data.get("jobTitle") or "").strip()
    job_description = (data.get("jobDescription") or "").strip()
    skills = data.get("skills") or []
    projects = (data.get("projects") or "").strip()
    experiences = data.get("experiences") or []

    if not job_title or not job_description or not experiences:
        return jsonify(
            {"success": False, "error": "Job title, description, and experiences are required."}
        ), 400

    try:
        resume_content = generate_resume_content(
            job_title=job_title,
            job_description=job_description,
            skills=skills,
            projects=projects,
            experiences=experiences,
        )
        pdf_filename = f"resume_{int(time.time())}.pdf"
        pdf_path = GENERATED_FOLDER / pdf_filename
        create_pdf(resume_content, str(pdf_path))
        return jsonify({"success": True, "pdf_url": f"/download/{pdf_filename}"})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = GENERATED_FOLDER / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    return jsonify({"success": False, "error": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
