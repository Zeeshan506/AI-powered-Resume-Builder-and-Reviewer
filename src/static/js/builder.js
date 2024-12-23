document.addEventListener('DOMContentLoaded', function () {
  // Attach the event listener after the DOM has been fully loaded
  document.querySelector('#submit-btn').addEventListener('click', submitFormData);

  function submitFormData(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    // Collect form data
    const jobTitle = document.querySelector('#job-title').value;
    const jobDescription = document.querySelector('#job-description').value;

    const selectedSkills = [];
    const selectedSkillsList = document.querySelectorAll('#selected-skills-list li');
    selectedSkillsList.forEach(skill => selectedSkills.push(skill.textContent.trim()));

    const projects = document.querySelector('#projects').value;

    const experiences = [];
    const rows = document.querySelectorAll('#experience-table tbody tr');
    rows.forEach(row => {
      const experience = {
        company: row.cells[0].textContent,
        title: row.cells[1].textContent,
        startDate: row.cells[2].textContent,
        endDate: row.cells[3].textContent,
        description: row.cells[4].textContent,
      };
      console.log("Experience:", experience); // Log the experience object for debugging
      experiences.push(experience);
    });

    const formData = {
      jobTitle: jobTitle,
      jobDescription: jobDescription,
      skills: selectedSkills,
      projects: projects,
      experiences: experiences,
    };

    console.log("Form data being sent:", formData); // Debugging log

    fetch('/generate-resume', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then(response => response.json())
      .then(data => {
        console.log("Backend response:", data); // Debugging log
        if (data.success) {
          // Update and show the download button with the generated PDF URL
          const downloadButton = document.querySelector('#download-btn');
          console.log("Generated resume URL:", data.pdf_url); // Check the URL
          downloadButton.href = data.pdf_url; // Set the URL for the download
          downloadButton.style.display = 'inline-block'; // Make the button visible
        } else {
          alert('Error generating resume: ' + data.error); // Handle errors
        }
      })
      .catch(error => {
        alert('Error: ' + error); // Handle fetch errors
      });
  }

  // Function to show the loader and simulate the resume generation process
  function generateResume() {
    // Hide the form and show the loader
    document.getElementById('resume-form').style.display = 'none';
    document.getElementById('loader').style.display = 'block';

    let consoleText = '';
    const consoleElement = document.getElementById('console');

    // Simulating step-by-step console log
    const steps = [
      "Initializing resume builder...",
      "C:\\Server\\..\\ Generating PDF...",
      "C:\\Server\\..\\ Parsing resume data...",
      "C:\\Server\\..\\ Adding job experience section...",
      "C:\\Server\\..\\ Adding skills and education...",
      "C:\\Server\\..\\ Formatting resume layout...",
      "C:\\Server\\..\\ Finalizing document...",
      "C:\\Server\\..\\ Resume generation complete!"
    ];

    let stepIndex = 0;

    // Simulate console output
    function simulateConsoleOutput() {
      if (stepIndex < steps.length) {
        consoleText += steps[stepIndex] + '\n';
        consoleElement.textContent = consoleText; // Update the console display
        stepIndex++;
        setTimeout(simulateConsoleOutput, 1000); // Wait for 1 second before next step
      } else {
        // After simulation, call the backend to generate the resume
        fetch('/generate-resume', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            jobTitle: document.getElementById('job-title').value,
            jobDescription: document.getElementById('job-description').value,
            skills: document.getElementById('skills').value.split(','),
            projects: document.getElementById('projects').value,
            experiences: JSON.parse(document.getElementById('experiences').value) // Assuming JSON format
          }),
        })
          .then(response => response.json())
          .then(result => {
            if (result.success) {
              // Update the download button with the resume URL
              const downloadButton = document.getElementById('download-btn');
              downloadButton.href = result.pdf_url; // Add the URL to the button
              downloadButton.style.display = 'inline-block'; // Show the download button
            } else {
              alert('Error generating resume: ' + result.error);
            }
            // Hide the loader
            document.getElementById('loader').style.display = 'none';
          })
          .catch(error => {
            alert('Error contacting the server: ' + error);
            document.getElementById('loader').style.display = 'none';
          });
      }
    }

    simulateConsoleOutput(); // Start the simulation
  }

  // Event listener for the "Generate Resume" button
  document.querySelector('#resume-form button[type="submit"]').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent actual form submission
    generateResume(); // Start the resume generation process
  });

  // Function to trigger the download of the resume
  function downloadResume() {
    alert('Download Started!');
    const downloadButton = document.querySelector('#download-btn');
    const pdfUrl = downloadButton.href;

    // If the PDF URL is valid, force download by opening in a new tab
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');  // This will open the PDF in a new tab for download
    } else {
      alert("Resume URL is not available.");
    }
  }

  // Make sure the download button calls the downloadResume function
  document.querySelector('#download-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default behavior
    downloadResume(); // Call the download function
  });

});
