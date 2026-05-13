const form = document.querySelector('#resume-form');
const jobTitle = document.querySelector('#job-title');
const jobDesc = document.querySelector('#job-description');

if (form && jobTitle && jobDesc) {
  form.addEventListener('submit', () => {
    if (!jobTitle.value.trim() || !jobDesc.value.trim()) {
      alert('Job Title and Description are required.');
    }
  });
}
