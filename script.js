// Drag and drop events

const uploadBox = document.querySelector('.upload-box');
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = '.pdf';

uploadBox.addEventListener('dragover', (event) => {
  event.preventDefault();
  uploadBox.style.borderColor = 'var(--color-button)';
});

uploadBox.addEventListener('dragleave', () => {
  uploadBox.style.borderColor = 'var(--color-tertiary)';
});

uploadBox.addEventListener('drop', (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  displayFile(file);
});

uploadBox.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  displayFile(file);
});

function displayFile(file) {
  const fileName = file.name;
  const uploadText = document.querySelector('.upload-text');
  uploadText.textContent = `File Selected: ${fileName}`;
}


// Form Validation
