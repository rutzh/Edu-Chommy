

fetch('navBar.html')
.then(res => res.text())
.then(data => {
  document.getElementById('navbar').innerHTML = data;

  
  const toggleBtn = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  toggleBtn?.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });
});

