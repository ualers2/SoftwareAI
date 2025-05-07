
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
      mobileMenuBtn.addEventListener('click', function() {
        navLinks.classList.toggle('show');
        document.querySelectorAll('.mobile-menu-btn span').forEach(span => {
          span.classList.toggle('active');
        });
      });
    }

// FAQ accordion
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
    question.addEventListener('click', () => {
    const isActive = item.classList.contains('active');
    
    // Close all items
    faqItems.forEach(faqItem => {
        faqItem.classList.remove('active');
    });
    
    // If clicked item wasn't active, make it active
    if (!isActive) {
        item.classList.add('active');
    }
    });
});

// Testimonial slider
const testimonialCards = document.querySelectorAll('.testimonial-card');
const dots = document.querySelectorAll('.dot');
let currentSlide = 0;

function showSlide(index) {
    testimonialCards.forEach(card => {
    card.classList.remove('active');
    });
    dots.forEach(dot => {
    dot.classList.remove('active');
    });
    
    testimonialCards[index].classList.add('active');
    dots[index].classList.add('active');
    currentSlide = index;
}

// Click event for dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
    showSlide(index);
    });
});

// Auto-rotate testimonials
function autoRotate() {
    let nextSlide = (currentSlide + 1) % testimonialCards.length;
    showSlide(nextSlide);
}

// Start with first slide
showSlide(0);

// Auto-rotate every 5 seconds
setInterval(autoRotate, 5000);

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
        window.scrollTo({
        top: targetElement.offsetTop - 80,
        behavior: 'smooth'
        });
        
        // Close mobile menu if open
        if (navLinks.classList.contains('show')) {
        navLinks.classList.remove('show');
        }
    }
    });
});

// Animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.feature-card, .pricing-card, .section-header');
    
    elements.forEach(element => {
    const elementPosition = element.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    
    if (elementPosition.top < windowHeight * 0.8) {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }
    });
};

// Set initial styles for animation
document.querySelectorAll('.feature-card, .pricing-card, .section-header').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
});

// Run once on load
animateOnScroll();

// Run on scroll
window.addEventListener('scroll', animateOnScroll);
});
