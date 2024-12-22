// Function to gather form data and send it to the backend
function submitFormData(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way
  
    // Collect job title and description
    const jobTitle = document.querySelector('#job-title').value;
    const jobDescription = document.querySelector('#job-description').value;
  
    // Collect skills (selected skills)
    const selectedSkills = [];
    const selectedSkillsList = document.querySelectorAll('#selected-skills-list li');
    selectedSkillsList.forEach(skill => selectedSkills.push(skill.textContent.trim()));
  
    // Collect projects (if any)
    const projects = document.querySelector('#projects').value;
  
    // Collect experiences from the table
    const experiences = [];
    const rows = document.querySelectorAll('#experience-table tbody tr');
    rows.forEach(row => {
      const experience = {
        companyName: row.cells[0].textContent,
        jobTitle: row.cells[1].textContent,
        duration: row.cells[2].textContent,
        description: row.cells[3].textContent,
      };
      experiences.push(experience);
    });
  
    // Prepare the data object to be sent to the backend
    const formData = {
      jobTitle: jobTitle,
      jobDescription: jobDescription,
      skills: selectedSkills,
      projects: projects,
      experiences: experiences,
    };
  
    // Send data to the backend via POST request
    fetch('/generate-resume', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Resume generated successfully!');
        // Optionally, provide a download link for the generated PDF
        window.location.href = data.pdf_url; // Redirect to the generated PDF
      } else {
        alert('Error generating resume: ' + data.error);
      }
    })
    .catch(error => {
      alert('Error: ' + error);
    });
  }
  
  // Add event listener to the submit button
  document.querySelector('button[type="submit"]').addEventListener('click', submitFormData);
  