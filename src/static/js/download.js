// Function to show the loader and simulate a dummy script output
function generateResume() {
    // Hide the form and show the loader
    document.getElementById('resume-form').style.display = 'none';
    document.getElementById('loader').style.display = 'block';
  
    // Simulate the dummy script with a delay to mimic a process (e.g., resume generation)
    let consoleText = '';
    const consoleElement = document.getElementById('console');
  
    // Simulating step-by-step console log
    const steps = [
        "Initializing resume builder...",
        "C:\\Server\\..\\ Generating PDF...",
        "C:\\Server\\..\\ Parsing resume data...",
        "C:\\Server\\..\\ Adding job experience section...",
        "C:\\Server\\..\\ Adding skills and education...",
        "C:\\Server\\..\\ Formatting resume layout...",
        "C:\\Server\\..\\ Finalizing document...",
        "C:\\Server\\..\\ Resume generation complete!"
      ];
  
    let stepIndex = 0;
    
    function simulateConsoleOutput() {
      if (stepIndex < steps.length) {
        consoleText += steps[stepIndex] + '\n';
        consoleElement.textContent = consoleText; // Update the console display
        stepIndex++;
        setTimeout(simulateConsoleOutput, 1000); // Wait for 1 second before next step
      } else {
        // Show the download button when the process is complete
        document.getElementById('download-btn').style.display = 'inline-block';
      }
    }
  
    simulateConsoleOutput();
  }
  
  // Function to trigger the download of the resume (mock behavior for now)
  function downloadResume() {
    alert('Download Started!');
    // Here you can integrate the actual file download logic
    // For now, we show a simple alert
  }
  
  // Event listener for the "Generate Resume" button
  document.querySelector('#resume-form button[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent actual form submission
    generateResume(); // Start the resume generation process
  });
  