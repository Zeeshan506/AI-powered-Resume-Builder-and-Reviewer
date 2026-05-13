document.addEventListener('DOMContentLoaded', () => {
  const submitButton = document.querySelector('#submit-btn');
  const downloadButton = document.querySelector('#download-btn');

  async function submitFormData(event) {
    event.preventDefault();

    const jobTitle = document.querySelector('#job-title').value.trim();
    const jobDescription = document.querySelector('#job-description').value.trim();
    const projects = document.querySelector('#projects').value.trim();

    const selectedSkills = Array.from(
      document.querySelectorAll('#selected-skills-list li')
    ).map((skill) => skill.textContent.replace('x', '').trim());

    const experiences = Array.from(
      document.querySelectorAll('#experience-table tbody tr')
    ).map((row) => ({
      company: row.cells[0]?.textContent || '',
      title: row.cells[1]?.textContent || '',
      startDate: row.cells[2]?.textContent || '',
      endDate: row.cells[3]?.textContent || '',
      description: row.cells[4]?.textContent || '',
    }));

    const payload = {
      jobTitle,
      jobDescription,
      skills: selectedSkills,
      projects,
      experiences,
    };

    try {
      const response = await fetch('/generate-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Resume generation failed.');
      }

      downloadButton.href = data.pdf_url;
      downloadButton.style.display = 'inline-block';
    } catch (error) {
      alert(`Error generating resume: ${error.message}`);
    }
  }

  submitButton.addEventListener('click', submitFormData);
});
