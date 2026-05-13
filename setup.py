from setuptools import setup, find_packages

setup(
    name="ai_resume_reviewer",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.10,<3.12",
    install_requires=[
        "Flask>=2.3,<3.0",
        "PyPDF2>=3.0,<4.0",
        "python-docx>=0.8,<1.2",
        "fpdf2>=2.7,<3.0",
        "joblib>=1.3,<2.0",
        "scikit-learn>=1.3,<1.6",
        "google-generativeai>=0.4,<1.0",
    ],
)
