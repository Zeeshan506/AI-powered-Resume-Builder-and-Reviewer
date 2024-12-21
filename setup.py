from setuptools import setup, find_packages

setup(
    name="ai_resume_reviewer",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
