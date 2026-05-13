const THEME_KEY = 'arb-theme';

function applyTheme(isDark) {
  const body = document.body;
  const themeToggle = document.getElementById('theme-toggle');
  body.classList.toggle('dark-theme', isDark);
  if (themeToggle) {
    themeToggle.textContent = isDark ? '🌞' : '🌙';
    themeToggle.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
  }
}

function toggleTheme() {
  const isDark = !document.body.classList.contains('dark-theme');
  applyTheme(isDark);
  localStorage.setItem(THEME_KEY, isDark ? 'dark' : 'light');
}

document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(savedTheme ? savedTheme === 'dark' : prefersDark);

  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
});

window.toggleTheme = toggleTheme;
