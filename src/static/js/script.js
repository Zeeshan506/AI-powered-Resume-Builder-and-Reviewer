const form = document.querySelector('.form2'); // The form that wraps your inputs
const submitButton = document.querySelector('.submit-button'); // The submit button
const fileInput = document.querySelector('#resumeInput'); // The file input
const jobTitleInput = document.querySelector('input[name="job_title"]'); // The job title input
const loaderSection = document.getElementById('loaderSection');
const resultSection = document.getElementById('resultSection');
const scoreDisplay = document.getElementById('scoreDisplay');

// Handle form submission
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the default form submission behavior

  const file = fileInput.files[0]; // Get the selected file
  const jobTitle = jobTitleInput.value; // Get the selected job title

  if (file && jobTitle) {
    handleFileUpload(file, jobTitle);
  } else {
    alert('Please select a file and job title.');
  }
});

// Function to handle file upload and job title submission
function handleFileUpload(file, jobTitle) {
  displayFile(file);

  // Show loader
  loaderSection.style.display = 'flex'; // Ensure loader stays aligned
  resultSection.style.display = 'none';

  // Create FormData object
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
      // Ensure loader is visible for a minimum duration
      const loaderDelay = 5000; // Adjust this value as needed
      setTimeout(() => {
        loaderSection.style.display = 'none';

        if (data.score !== undefined) {
          resultSection.style.display = 'flex'; // Replaces loader in the same space
          scoreDisplay.textContent = `${data.score}`;
        } else {
          throw new Error(data.error || 'Unexpected error');
        }
      }, loaderDelay);
    })
    .catch((error) => {
      loaderSection.style.display = 'none';
      alert(`Error: ${error.message}`);
    });
}

function displayFile(file) {
  const uploadText = document.querySelector('.upload-text');
  uploadText.textContent = `File Selected: ${file.name}`;
}
