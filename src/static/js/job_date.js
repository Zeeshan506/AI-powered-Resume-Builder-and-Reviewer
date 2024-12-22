// Function to validate the date format (mm/yy) - Optional, but you can disable it.
function validateDateFormat(date) {
  const datePattern = /^(0[1-9]|1[0-2])\/\d{2}$/;  // Regex for mm/yy format
  return datePattern.test(date);
}

// Function to validate that the start date is before the end date - Optional, you can skip this check.
function validateExperienceDates(startDate, endDate) {
  const startParts = startDate.split('/');
  const endParts = endDate.split('/');

  const startMonth = parseInt(startParts[0], 10);
  const startYear = parseInt(startParts[1], 10);
  const endMonth = parseInt(endParts[0], 10);
  const endYear = parseInt(endParts[1], 10);

  // Compare years first, then months - this check can be skipped if you don't need it
  return (startYear < endYear || (startYear === endYear && startMonth < endMonth));
}

// Attach event listener to the form submission
document.getElementById('resume-form').addEventListener('submit', function(event) {
  // Skip general validation for the job title and job description (optional).
  // Just remove this part if you don't want any checks on these fields.
  const jobTitle = document.querySelector('#job-title').value.trim();
  const jobDescription = document.querySelector('#job-description').value.trim();
  if (!jobTitle || !jobDescription) {
    alert('Please fill in all the required fields.'); // Optional check, you can skip this part too
    event.preventDefault();
    return;
  }

  // Skip the validation for experience entries
  const experienceEntries = document.querySelectorAll('.experience-entry');
  let isValidExperience = true;

  experienceEntries.forEach(entry => {
    const startDate = entry.querySelector('.start-date').value.trim();
    const endDate = entry.querySelector('.end-date').value.trim();

    // Skip the date format validation
    // Skip the validation that start date should be before end date
    // Just remove the validation if you don't want any checks
  });

  // Skip checking the experience fields in the table if you want the form to submit no matter what
  const experienceTableRows = document.querySelectorAll('#experience-table tbody tr');
  experienceTableRows.forEach(row => {
    const companyName = row.cells[0].textContent.trim();
    const jobTitle = row.cells[1].textContent.trim();
    const duration = row.cells[2].textContent.trim();
    const description = row.cells[3].textContent.trim();

    // If you want to allow submission without checking experience, skip this part
    // Just make sure to comment out or remove the check here
  });

  // Skip form validation and allow submission no matter what
  return true;  // Allow form submission
});
