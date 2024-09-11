// Sélectionner tous les éléments de la navbar
const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

// Sélectionner toutes les sections correspondantes
const sections = document.querySelectorAll('.section');

// Ajouter un événement de clic à chaque lien
navLinks.forEach((link, index) => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Empêcher le comportement par défaut du lien

        // Retirer la classe 'active' de tous les liens
        navLinks.forEach(nav => nav.classList.remove('active'));

        // Ajouter la classe 'active' au lien cliqué
        this.classList.add('active');

        // Masquer toutes les sections
        sections.forEach(section => section.style.display = 'none');

        // Afficher la section correspondante au lien cliqué
        sections[index].style.display = 'block';
    });
});

// Initialiser le carrousel
document.addEventListener("DOMContentLoaded", function() {
    const myCarousel = document.querySelector('#carouselExample');
    const carouselInstance = new bootstrap.Carousel(myCarousel, {
        interval: 10000 // Intervalle de 10 secondes
    });

    // Masquer toutes les sections sauf la première au chargement
    sections.forEach((section, index) => {
        section.style.display = index === 0 ? 'block' : 'none';
    });
});
document.querySelectorAll('.form-control').forEach((input) => {
    input.addEventListener('input', () => {
        if (input.value.trim() !== '') {
            input.classList.add('filled');
        } else {
            input.classList.remove('filled');
        }
    });
});