// // Function to show the loader and simulate the resume generation process
// function generateResume() {
//   // Hide the form and show the loader
//   document.getElementById('resume-form').style.display = 'none';
//   document.getElementById('loader').style.display = 'block';

//   let consoleText = '';
//   const consoleElement = document.getElementById('console');

//   // Simulating step-by-step console log
//   const steps = [
//     "Initializing resume builder...",
//     "C:\\Server\\..\\ Generating PDF...",
//     "C:\\Server\\..\\ Parsing resume data...",
//     "C:\\Server\\..\\ Adding job experience section...",
//     "C:\\Server\\..\\ Adding skills and education...",
//     "C:\\Server\\..\\ Formatting resume layout...",
//     "C:\\Server\\..\\ Finalizing document...",
//     "C:\\Server\\..\\ Resume generation complete!"
//   ];

//   let stepIndex = 0;

//   // Simulate console output
//   function simulateConsoleOutput() {
//     if (stepIndex < steps.length) {
//       consoleText += steps[stepIndex] + '\n';
//       consoleElement.textContent = consoleText; // Update the console display
//       stepIndex++;
//       setTimeout(simulateConsoleOutput, 1000); // Wait for 1 second before next step
//     } else {
//       // After simulation, call the backend to generate the resume
//       fetch('/generate-resume', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           jobTitle: document.getElementById('job-title').value,
//           jobDescription: document.getElementById('job-description').value,
//           skills: document.getElementById('skills').value.split(','),
//           projects: document.getElementById('projects').value,
//           experiences: JSON.parse(document.getElementById('experiences').value) // Assuming JSON format
//         }),
//       })
//         .then(response => response.json())
//         .then(result => {
//           if (result.success) {
//             // Update the download button with the resume URL
//             const downloadButton = document.getElementById('download-btn');
//             downloadButton.href = result.pdf_url; // Add the URL to the button
//             downloadButton.style.display = 'inline-block'; // Show the download button
//           } else {
//             alert('Error generating resume: ' + result.error);
//           }
//           // Hide the loader
//           document.getElementById('loader').style.display = 'none';
//         })
//         .catch(error => {
//           alert('Error contacting the server: ' + error);
//           document.getElementById('loader').style.display = 'none';
//         });
//     }
//   }

//   simulateConsoleOutput(); // Start the simulation
// }

// // Event listener for the "Generate Resume" button
// document.querySelector('#resume-form button[type="submit"]').addEventListener('click', function (event) {
//   event.preventDefault(); // Prevent actual form submission
//   generateResume(); // Start the resume generation process
// });

// // Function to trigger the download of the resume
// function downloadResume() {
//   alert('Download Started!');
// }
