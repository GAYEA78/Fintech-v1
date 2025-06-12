// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.tabs button');
  const contents = document.querySelectorAll('.tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active from all
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));

      // Activate clicked
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab).classList.add('active');
    });
  });

  // Activate first tab by default
  if (tabs.length > 0) {
    tabs[0].classList.add('active');
    const first = document.getElementById(tabs[0].dataset.tab);
    if (first) first.classList.add('active');
  }

  // Glow mode toggle
  const toggle = document.getElementById('darkToggle');
  toggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('glow');
  });
});
