# AI-powered Resume Builder and Reviewer (Basic Runnable Edition)

This project has been cleaned into a **presentable, junior-friendly baseline** focused on:

1. Resume Builder: create a PDF resume from form input.
2. Resume Reviewer: upload a PDF and get a score breakdown.
3. Skills/Job Title suggestions from `data/Preprocessing/Simplified.csv`.

---

## Python version (important)

This codebase is pinned to an older stable runtime for compatibility:

- **Python 3.10**

Use `.python-version` (already included) with pyenv/asdf, or create the venv explicitly with Python 3.10.

---

## Setup guide

### 1. Create virtual environment

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure AI key

```bash
cp .env.example .env
```

Then set values in `.env` and export them in your shell (or via your preferred env loader).

> If API key is missing, app still works using local non-AI resume formatting.

### 4. Run app

```bash
python src/app.py
```

Open: `http://127.0.0.1:5000`

---

## Dataset + file placement (for junior handoff)

After cloning, place files exactly like this:

```text
data/
  Preprocessing/
    Simplified.csv                # REQUIRED (job_title, skill columns)
    retrained_old_model.pkl       # OPTIONAL (tone model)
    tfidf_vectorizer.pkl          # OPTIONAL (tone vectorizer)
  resumes/                        # input resumes uploaded by app
  parsed_data/                    # parsed text output from reviewer
  generated_resumes/              # generated resume PDFs from builder
```

- `Simplified.csv` is the only mandatory dataset file for normal app behavior.
- If tone model files are missing, reviewer still runs with fallback scoring.
- `resumes/`, `parsed_data/`, and `generated_resumes/` are runtime folders and should stay lightweight.

When you share the dataset source link, put it in this README under a new section:

```md
## Dataset source
https://www.kaggle.com/datasets/suriyaganesh/resume-dataset-structured
```

---

## API key and model config explained

The builder can optionally call Gemini for improved resume wording.

Environment variables used by `src/Builder/resume_builder.py`:

- `GEMINI_API_KEY`: turns on AI rewriting.
- `GEMINI_MODEL`: model name (default: `gemini-1.5-flash`).
- `GEMINI_TEMPERATURE`: creativity level (default: `0.6`).
- `GEMINI_TOP_P`: nucleus sampling (default: `0.95`).
- `GEMINI_TOP_K`: token candidate cap (default: `40`).
- `GEMINI_MAX_OUTPUT_TOKENS`: max generation length (default: `2048`).

If any of these are not set, safe defaults are used.

---

## What was cleaned

- Removed hardcoded local Windows paths.
- Removed hardcoded API key usage from runtime path.
- Removed all bundled PDF artifacts from the repository.
- Simplified reviewer flow to a robust baseline scoring system.
- Simplified front-end builder and job-title scripts to avoid duplicate/broken submit flows.
- Replaced oversized dependency list with minimal project requirements.
- Added clean `.gitignore`, `.env.example`, and Python version pinning.

---

## Key files for a junior developer

- `src/app.py` → Flask routes and app wiring.
- `src/Builder/resume_builder.py` → Resume text generation + PDF creation + optional Gemini.
- `src/parsers/resume_reviewer.py` → Reviewer scoring logic.
- `src/parsers/utils.py` → PDF text extraction + skill lookup helpers.
- `src/templates/index.html` and `src/static/js/` → Front-end behavior.
