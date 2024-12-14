
const form = document.querySelector('#builder-form');
const jobTitle = document.querySelector('#job-title');
const jobDesc = document.querySelector('#job-desc');
const submitButton = document.querySelector('#submit-btn');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  validateForm();
});

function validateForm() {
  if (!jobTitle.value.trim() || !jobDesc.value.trim()) {
    alert("Job Title and Description are required.");
    return;
  }
  submitForm();
}

function submitForm() {
  // Process the form data
}


// Skill Suggestions
