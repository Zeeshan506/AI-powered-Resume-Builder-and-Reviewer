/// Get the elements
const dropdownToggle = document.getElementById('dropdown-toggle');
const dropdown = document.getElementById('dropdown');
const searchSkillInput = document.getElementById('search-skill');
const skillOptions = document.getElementById('skill-options');
const selectedSkillsList = document.getElementById('selected-skills-list');

const skills = [
  "JavaScript", "Python", "Java", "C++", "PHP", "HTML", "CSS", "React", 
  "Node.js", "Django", "Flask", "SQL", "MongoDB", "Git", "Docker", 
  "AWS", "Azure", "Kubernetes", "Go", "Ruby", "Swift", "C#", "TypeScript"
];

// Show or hide the dropdown list when clicking the toggle button
dropdownToggle.addEventListener('click', () => {
  dropdown.classList.toggle('active');
});

// Function to filter skills based on the search input
function filterSkills(searchTerm) {
  const filteredSkills = skills.filter(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()));
  displaySkills(filteredSkills);
}

// Function to display skills in the dropdown list
function displaySkills(skillsList) {
  skillOptions.innerHTML = '';
  
  if (skillsList.length > 0) {
    skillsList.forEach(skill => {
      const skillItem = document.createElement('li');
      skillItem.textContent = skill;
      skillItem.addEventListener('click', () => addSkill(skill));
      skillOptions.appendChild(skillItem);
    });
  } else {
    skillOptions.innerHTML = '<p>Skills not found</p>';
  }
}

// Function to add a skill to the selected skills list
function addSkill(skill) {
  // Check if the skill is already selected
  if (!isSkillSelected(skill)) {
    const skillItem = document.createElement('li');
    skillItem.textContent = skill;
    
    // Add a remove button for each selected skill
    const removeButton = document.createElement('span');
    removeButton.textContent = 'x';
    removeButton.classList.add('remove');
    removeButton.addEventListener('click', () => removeSkill(skillItem));
    
    skillItem.appendChild(removeButton);
    selectedSkillsList.appendChild(skillItem);
  }
}

// Function to check if the skill is already in the selected skills list
function isSkillSelected(skill) {
  const selectedSkills = selectedSkillsList.querySelectorAll('li');
  for (let selectedSkill of selectedSkills) {
    if (selectedSkill.textContent.replace('x', '').trim() === skill) {
      return true;
    }
  }
  return false;
}

// Function to remove a skill from the selected skills list
function removeSkill(skillItem) {
  selectedSkillsList.removeChild(skillItem);
}

// Listen for search input changes and filter skills
searchSkillInput.addEventListener('input', () => {
  const searchTerm = searchSkillInput.value;
  filterSkills(searchTerm);
});

// Initial display of all skills
displaySkills(skills);
