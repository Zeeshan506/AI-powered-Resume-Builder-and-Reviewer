// Function to add experience to the table
function addExperience() {
    const companyName = document.querySelector('.company-name').value;
    const jobTitle = document.querySelector('.job-title').value;
    const duration = document.querySelector('.duration').value;
    const jobDescription = document.querySelector('.job-description').value;
  
    // Validation check
    if (!companyName || !jobTitle || !duration || !jobDescription) {
      alert('Please fill all the fields');
      return;
    }
  
    // Create new row
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
    cell3.innerHTML = duration;
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
    document.querySelector('.duration').value = '';
    document.querySelector('.job-description').value = '';
  }
  
  // Function to remove an experience entry
  function removeExperience(row) {
    row.remove();
  }
  