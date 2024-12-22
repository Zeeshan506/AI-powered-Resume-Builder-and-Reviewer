// Function to add experience to the table
function addExperience() {
  const companyName = document.querySelector('.company-name').value;
  const jobTitle = document.querySelector('.job-title').value;
  const startDate = document.querySelector('.start-date').value.trim();
  const endDate = document.querySelector('.end-date').value.trim();
  const jobDescription = document.querySelector('.job-description').value;

  // Removed validation checks
  // The form will now allow submission even if fields are empty or invalid

  // Create new row in the table
  const table = document.getElementById('experience-table').getElementsByTagName('tbody')[0];
  const newRow = table.insertRow();

  // Insert cells with experience data
  const cell1 = newRow.insertCell(0);
  const cell2 = newRow.insertCell(1);
  const cell3 = newRow.insertCell(2);
  const cell4 = newRow.insertCell(3);
  const cell5 = newRow.insertCell(4);

  cell1.innerHTML = companyName;
  cell2.innerHTML = jobTitle;
  cell3.innerHTML = `${startDate} to ${endDate}`; // Display start and end date
  cell4.innerHTML = jobDescription;

  // Add Remove button in the last column
  const removeButton = document.createElement('button');
  removeButton.textContent = 'Remove';
  removeButton.onclick = function () {
    removeExperience(newRow);
  };
  cell5.appendChild(removeButton);

  // Clear input fields after adding
  document.querySelector('.company-name').value = '';
  document.querySelector('.job-title').value = '';
  document.querySelector('.start-date').value = '';
  document.querySelector('.end-date').value = '';
  document.querySelector('.job-description').value = '';
}

// Function to remove an experience entry
function removeExperience(row) {
  row.remove();
}
