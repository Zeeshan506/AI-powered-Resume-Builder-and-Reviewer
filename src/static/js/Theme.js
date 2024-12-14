function toggleTheme() {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
  
    // Toggle the dark-theme class on body
    body.classList.toggle('dark-theme');
  
    // Change the button text/icon based on the current theme
    if (body.classList.contains('dark-theme')) {
      themeToggle.textContent = '🌞';  // Switch to light theme icon
    } else {
      themeToggle.textContent = '🌙';  // Switch to dark theme icon
    }
  }
  