let jobTitles = []; // data will be added from dataset

// Fetch job titles from the backend 
async function loadJobTitles() {
  try {
    const response = await fetch('/get_job_titles');
    const data = await response.json();
    jobTitles = data.job_titles || []; 
  } catch (error) {
    console.error("Error loading job titles:", error);
  }
}

// Function to filter job titles based on search input
function filterJobTitles() {
  const searchInput = document.querySelector('.search input').value.toLowerCase(); // Get search input
  const optionsList = document.querySelector('.options'); // The container where job titles are listed
  optionsList.innerHTML = ''; // Clear previous search results
  
  const filteredTitles = jobTitles.filter(title => title.toLowerCase().includes(searchInput)); // Filter titles based on input
  
  if (filteredTitles.length === 0) {
    optionsList.innerHTML = '<li>No job titles found</li>'; // Display message if no results found
  } else {
    filteredTitles.forEach(title => {
      const li = document.createElement('li');
      li.textContent = title;
      li.addEventListener('click', () => selectJobTitle(title)); // Add click event to each list item
      optionsList.appendChild(li);
    });
  }
}

// Function to handle job title selection
function selectJobTitle(title) {
  document.querySelector('.search input').value = title; // Set the input value to selected title
  document.querySelector('.options').innerHTML = ''; // Clear the options list
  toggleDropdown(); // Close the dropdown after selecting a title
  
  // Now, submit the resume along with the selected job title
  const formData = new FormData();
  const fileInput = document.querySelector('input[type="file"]'); // Assuming there's a file input element
  const jobTitle = document.querySelector('.search input').value; // Get the selected job title
  
  formData.append('resume', fileInput.files[0]);
  formData.append('job_title', jobTitle); // Append the selected job title
  
  // Send the form data to the backend
  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    if (data.score) {
      console.log('Score:', data.score); // Handle the response (score) from the backend
    } else if (data.error) {
      console.error('Error:', data.error);
    }
  })
  .catch(error => {
    console.error('Error during file upload:', error);
  });
}

// Toggle the visibility of the dropdown
function toggleDropdown() {
  const wrapper = document.querySelector('.wrapper');
  wrapper.classList.toggle('active');
}

// Event listener for the search input field
document.querySelector('.search input').addEventListener('input', filterJobTitles);

// Event listener for the dropdown button to toggle the dropdown visibility
document.querySelector('.select-btn').addEventListener('click', toggleDropdown);

// Initialize dropdown with all job titles when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  await loadJobTitles(); // Load job titles on page load
  const optionsList = document.querySelector('.options');
  jobTitles.forEach(title => {
    const li = document.createElement('li');
    li.textContent = title;
    li.addEventListener('click', () => selectJobTitle(title)); // Add click event to each list item
    optionsList.appendChild(li);
  });
});
