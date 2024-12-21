// Sample dataset of job titles (replace with your actual dataset)
const jobTitles = [
  "Software Engineer",
  "Data Scientist",
  "Product Manager",
  "UX Designer",
  "Web Developer",
  "Marketing Specialist",
  "System Administrator",
  "Business Analyst",
  "Quality Assurance Tester",
  "DevOps Engineer",
  "HR Manager",
  "Project Manager"
];

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
document.addEventListener('DOMContentLoaded', () => {
  const optionsList = document.querySelector('.options');
  jobTitles.forEach(title => {
    const li = document.createElement('li');
    li.textContent = title;
    li.addEventListener('click', () => selectJobTitle(title)); // Add click event to each list item
    optionsList.appendChild(li);
  });
});
