let jobTitles = [];

async function loadJobTitles() {
  try {
    const response = await fetch('/get_job_titles');
    const data = await response.json();
    jobTitles = data.job_titles || [];
  } catch (error) {
    console.error('Error loading job titles:', error);
  }
}

function renderJobTitles(titles) {
  const optionsList = document.querySelector('.options');
  optionsList.innerHTML = '';

  if (!titles.length) {
    optionsList.innerHTML = '<li>No job titles found</li>';
    return;
  }

  titles.forEach((title) => {
    const li = document.createElement('li');
    li.textContent = title;
    li.addEventListener('click', () => selectJobTitle(title));
    optionsList.appendChild(li);
  });
}

function filterJobTitles() {
  const searchInput = document.querySelector('.search input').value.toLowerCase();
  const filtered = jobTitles.filter((title) => title.toLowerCase().includes(searchInput));
  renderJobTitles(filtered);
}

function selectJobTitle(title) {
  document.querySelector('.search input').value = title;
  document.querySelector('.options').innerHTML = '';
  toggleDropdown();
}

function toggleDropdown() {
  document.querySelector('.wrapper').classList.toggle('active');
}

document.querySelector('.search input').addEventListener('input', filterJobTitles);
document.querySelector('.select-btn').addEventListener('click', toggleDropdown);

document.addEventListener('DOMContentLoaded', async () => {
  await loadJobTitles();
  renderJobTitles(jobTitles);
});
