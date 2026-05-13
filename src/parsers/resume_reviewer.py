import os
import re
from pathlib import Path

import joblib

from parsers.utils import (
    extract_text_from_pdf,
    get_matching_skills,
    is_passive,
    preprocess_text,
    read_text_file,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PARSED_DATA_PATH = PROJECT_ROOT / "data" / "parsed_data"
MODEL_PATH = PROJECT_ROOT / "data" / "Preprocessing" / "retrained_old_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "data" / "Preprocessing" / "tfidf_vectorizer.pkl"


def _load_tone_model():
    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)
    return None, None


old_model, old_vectorizer = _load_tone_model()


def save_parsed_data(parsed_text, original_file_name):
    PARSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    base_name = os.path.splitext(original_file_name)[0]
    output_file = PARSED_DATA_PATH / f"{base_name}_parsed.txt"
    output_file.write_text(parsed_text, encoding="utf-8")
    return str(output_file)


def process_resume(file_path):
    if not file_path.endswith(".pdf"):
        raise ValueError("Unsupported file type: only PDF files are accepted.")
    extracted_text = extract_text_from_pdf(file_path)
    cleaned_text = preprocess_text(extracted_text)
    return save_parsed_data(cleaned_text, os.path.basename(file_path))


def calculate_skill_score(file_path, job_title):
    resume_text = read_text_file(file_path)
    skills = get_matching_skills(job_title)

    skill_score = _calculate_skill_score_from_keywords(resume_text, skills)
    tone_score = _calculate_tone_score(resume_text)
    grammar_score = _calculate_grammar_score(resume_text)
    clarity_score = _calculate_clarity_score(resume_text)
    project_score = calculate_project_score(resume_text)
    experience_score = calculate_experience_score(resume_text)
    total_score = (
        skill_score
        + tone_score
        + grammar_score
        + clarity_score
        + project_score
        + experience_score
    )

    return {
        "skill_score": skill_score,
        "tone_score": tone_score,
        "grammar_score": grammar_score,
        "clarity_score": clarity_score,
        "project_score": project_score,
        "experience_score": experience_score,
        "total_score": total_score,
    }


def _calculate_skill_score_from_keywords(resume_text, skills):
    if not skills:
        return 0
    normalized = resume_text.lower()
    matches = 0
    for skill in skills:
        skill_text = skill.strip().lower()
        if skill_text and skill_text in normalized:
            matches += 1
    ratio = matches / max(len(skills), 1)
    return min(50, max(0, int(round(ratio * 50))))


def check_tone_of_resume(resume_text):
    cleaned_text = preprocess_text(resume_text)
    if old_model is not None and old_vectorizer is not None:
        vectorized = old_vectorizer.transform([cleaned_text])
        return old_model.predict(vectorized)[0]

    positive_tokens = {
        "achieved",
        "improved",
        "optimized",
        "led",
        "managed",
        "developed",
        "built",
    }
    hits = sum(1 for token in cleaned_text.split() if token in positive_tokens)
    if hits >= 8:
        return "Professional"
    if hits >= 4:
        return "Formal"
    return "Regular"


def _calculate_tone_score(resume_text):
    predicted_tone = check_tone_of_resume(resume_text)
    if predicted_tone == "Regular":
        return 10
    if predicted_tone == "Formal":
        return 12
    if predicted_tone == "Professional":
        return 13
    return 10


def _calculate_grammar_score(resume_text):
    penalty = 0
    if "  " in resume_text:
        penalty += 1
    if len(re.findall(r"[.!?]", resume_text)) < 3:
        penalty += 1
    return max(3, 5 - penalty)


def _calculate_clarity_score(resume_text):
    sentences = [s.strip() for s in re.split(r"[.!?]+", resume_text) if s.strip()]
    if not sentences:
        return 7

    words = resume_text.split()
    avg_words = len(words) / len(sentences)
    passive_count = sum(1 for sentence in sentences if is_passive(sentence))
    passive_percentage = (passive_count / len(sentences)) * 100

    if avg_words <= 14:
        clarity = 15
    elif avg_words <= 20:
        clarity = 12
    else:
        clarity = 9

    if passive_percentage > 20:
        clarity -= 2
    return max(7, clarity)


def calculate_project_score(resume_text):
    project_keywords = ["project", "projects", "portfolio", "github"]
    return 5 if any(k in resume_text.lower() for k in project_keywords) else 1


def calculate_experience_score(resume_text):
    experience_keywords = ["experience", "intern", "engineer", "manager", "worked"]
    return 5 if any(k in resume_text.lower() for k in experience_keywords) else 3
