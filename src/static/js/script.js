const form = document.querySelector('.form2'); // The form wrapping the inputs
const submitButton = document.querySelector('.submit-button'); // The submit button
const fileInput = document.querySelector('#resumeInput'); // The file input
const jobTitleInput = document.querySelector('input[name="job_title"]'); // The job title input
const loaderSection = document.getElementById('loaderSection'); // Loader element
const resultSection = document.getElementById('resultSection'); // Result section
const scoreDisplay = document.getElementById('scoreDisplay'); // Display for the scores

// Handle form submission
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  const file = fileInput.files[0]; // Get selected file
  const jobTitle = jobTitleInput.value.trim(); // Get job title and trim whitespace

  if (file && jobTitle) {
    handleFileUpload(file, jobTitle);
  } else {
    alert('Please select a file and enter a job title.');
  }
});

// Function to handle file upload and job title submission
function handleFileUpload(file, jobTitle) {
  displayFile(file);

  // Show loader and hide result section
  loaderSection.style.display = 'flex';
  resultSection.style.display = 'none';

  // Create FormData object for the POST request
  const formData = new FormData();
  formData.append('resume', file);
  formData.append('job_title', jobTitle);

  // Make POST request to Flask app
  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to upload file.');
      }
      return response.json();
    })
    .then((data) => {
      // Ensure loader visibility for a consistent user experience
      const minimumLoaderTime = 2000; // Minimum loader display duration in milliseconds
      const startTime = performance.now();

      const processResponse = () => {
        const elapsedTime = performance.now() - startTime;
        const remainingTime = Math.max(minimumLoaderTime - elapsedTime, 0);

        setTimeout(() => {
          loaderSection.style.display = 'none';

          if (data.total_score !== undefined) {
            // Ensure loader visibility for a consistent user experience
            loaderSection.style.display = 'none';  // Hide loader
            resultSection.style.display = 'flex';  // Show result section
            displayScores(data);  // Pass data to displayScores for detailed display
          } else {
            throw new Error(data.error || 'Unexpected error occurred.');
          }
        }, remainingTime);
      };

      processResponse();
    })
    .catch((error) => {
      loaderSection.style.display = 'none';
      alert(`Error: ${error.message}`);
    });
}

// Display selected file name
function displayFile(file) {
  const uploadText = document.querySelector('.upload-text');
  uploadText.textContent = `File Selected: ${file.name}`;
}

// Function to display scores
function displayScores(data) {
  scoreDisplay.innerHTML = `
    <h3>Resume Evaluation Breakdown</h3>
    <div class="score-item"><strong>Skill Score:</strong> ${data.skill_score}</div>
    <div class="score-item"><strong>Tone Score:</strong> ${data.tone_score}</div>
    <div class="score-item"><strong>Grammar Score:</strong> ${data.grammar_score}</div>
    <div class="score-item"><strong>Clarity Score:</strong> ${data.clarity_score}</div>
    <div class="score-item"><strong>Projects Score:</strong> ${data.project_score}</div>
    <div class="score-item"><strong>Experience Score:</strong> ${data.experience_score}</div>
    <div class="score-item"><strong>Total Score:</strong> ${data.total_score}</div>
  `;
}

