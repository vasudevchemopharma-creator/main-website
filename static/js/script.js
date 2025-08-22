// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile Navigation Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    
    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        
        // Change hamburger icon to X when menu is open
        if (navLinks.classList.contains('active')) {
            menuToggle.innerHTML = '✕';
        } else {
            menuToggle.innerHTML = '☰';
        }
    });
    
    // Close mobile menu when clicking on a link
    const navLinkItems = document.querySelectorAll('.nav-links a');
    navLinkItems.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
            menuToggle.innerHTML = '☰';
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!menuToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            menuToggle.innerHTML = '☰';
        }
    });
    
    // Show More Products Functionality
    const showMoreBtn = document.getElementById('showMoreBtn');
    const hiddenProducts = document.querySelectorAll('.hidden-products');
    let productsVisible = false;
    
    showMoreBtn.addEventListener('click', function() {
        if (!productsVisible) {
            // Show hidden products
            hiddenProducts.forEach(product => {
                product.classList.add('show');
                product.style.display = 'block';
            });
            showMoreBtn.textContent = 'Show Less Products';
            productsVisible = true;
            
            // Add fade-in animation
            setTimeout(() => {
                hiddenProducts.forEach((product, index) => {
                    setTimeout(() => {
                        product.style.opacity = '0';
                        product.style.transform = 'translateY(20px)';
                        product.style.transition = 'all 0.5s ease';
                        
                        requestAnimationFrame(() => {
                            product.style.opacity = '1';
                            product.style.transform = 'translateY(0)';
                        });
                    }, index * 100);
                });
            }, 50);
            
        } else {
            // Hide products
            hiddenProducts.forEach(product => {
                product.classList.remove('show');
                product.style.display = 'none';
            });
            showMoreBtn.textContent = 'Show More Products';
            productsVisible = false;
        }
    });
    
    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Contact Form Handling
    const contactForm = document.getElementById('contactForm');
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const name = formData.get('name');
        const email = formData.get('email');
        const company = formData.get('company');
        const phone = formData.get('phone');
        const product = formData.get('product');
        const message = formData.get('message');
        
        // Basic validation
        if (!name || !email || !message) {
            alert('Please fill in all required fields (Name, Email, and Message).');
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        
        // Show loading state
        const submitBtn = contactForm.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        // Simulate form submission (replace with actual API call)
        setTimeout(() => {
            // Remove loading state
            submitBtn.classList.remove('loading');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            
            // Show success message
            showSuccessMessage('Thank you for your inquiry! We will get back to you within 24 hours.');
            
            // Reset form
            contactForm.reset();
            
            // Log form data (for development - remove in production)
            console.log('Form submitted with data:', {
                name, email, company, phone, product, message
            });
            
        }, 2000);
    });
    
    // Function to show success message
    function showSuccessMessage(message) {
        // Create success message element if it doesn't exist
        let successMessage = document.querySelector('.success-message');
        if (!successMessage) {
            successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            contactForm.parentNode.insertBefore(successMessage, contactForm);
        }
        
        successMessage.textContent = message;
        successMessage.classList.add('show');
        
        // Hide success message after 5 seconds
        setTimeout(() => {
            successMessage.classList.remove('show');
        }, 5000);
    }
    
    // Scroll-triggered animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Add fade-in animation to elements
    const animateElements = document.querySelectorAll('.product-card, .certificate, .partner, .about-text, .contact-info');
    animateElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
    
    // Header background opacity change on scroll
    let lastScrollY = window.scrollY;
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            header.style.background = 'linear-gradient(135deg, rgba(26, 54, 93, 0.95), rgba(45, 80, 22, 0.95))';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'linear-gradient(135deg, #1a365d, #2d5016)';
            header.style.backdropFilter = 'none';
        }
        
        lastScrollY = currentScrollY;
    });
    
    // Product cards hover effect enhancement
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Certificate cards rotation effect
    const certificates = document.querySelectorAll('.certificate');
    certificates.forEach(cert => {
        cert.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) rotateY(5deg)';
        });
        
        cert.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateY(0deg)';
        });
    });
    
    // Partner cards pulse effect
    const partners = document.querySelectorAll('.partner');
    partners.forEach(partner => {
        partner.addEventListener('mouseenter', function() {
            const logo = this.querySelector('.partner-logo');
            logo.style.animation = 'pulse 1s ease-in-out';
        });
        
        partner.addEventListener('mouseleave', function() {
            const logo = this.querySelector('.partner-logo');
            logo.style.animation = 'none';
        });
    });
    
    // Form field focus effects
    const formFields = document.querySelectorAll('.form-group input, .form-group textarea, .form-group select');
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // Add typing effect to hero title
    const heroTitle = document.querySelector('.hero h1');
    const titleText = heroTitle.textContent;
    heroTitle.textContent = '';
    
    let charIndex = 0;
    const typingSpeed = 50;
    
    function typeWriter() {
        if (charIndex < titleText.length) {
            heroTitle.textContent += titleText.charAt(charIndex);
            charIndex++;
            setTimeout(typeWriter, typingSpeed);
        }
    }
    
    // Start typing effect after page load
    setTimeout(typeWriter, 500);
    
    // Add parallax effect to hero section
    const hero = document.querySelector('.hero');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = scrolled * 0.5;
        hero.style.transform = `translateY(${parallax}px)`;
    });
    
    // Add counter animation for certificates
    const certNumbers = document.querySelectorAll('.cert-icon');
    let countersAnimated = false;
    
    const certificatesSection = document.getElementById('certificates');
    const certObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersAnimated) {
                animateCounters();
                countersAnimated = true;
            }
        });
    }, { threshold: 0.5 });
    
    certObserver.observe(certificatesSection);
    
    function animateCounters() {
        certNumbers.forEach((counter, index) => {
            setTimeout(() => {
                counter.style.animation = 'bounceIn 0.6s ease-out';
            }, index * 200);
        });
    }
    
    // Add dynamic year to footer
    const currentYear = new Date().getFullYear();
    const copyrightText = document.querySelector('.footer-section p');
    if (copyrightText && copyrightText.textContent.includes('2025')) {
        copyrightText.textContent = copyrightText.textContent.replace('2025', currentYear);
    }
    
    // --- Partners Section Auto-Scroll Loop ---
    document.addEventListener('DOMContentLoaded', function() {
        // Duplicate partners for seamless horizontal scroll
        const partnersGrid = document.querySelector('.partners-grid');
        if (partnersGrid) {
            partnersGrid.innerHTML += partnersGrid.innerHTML;
        }

        // Auto-scroll function
        function autoScrollPartners() {
            const scrollAmount = 10; // Amount to scroll on each iteration
            const scrollDelay = 80; // Delay between scrolls in milliseconds
            
            function scroll() {
                partnersGrid.scrollLeft += scrollAmount;
                
                // If scrolled to the end, jump back to the start
                if (partnersGrid.scrollLeft >= partnersGrid.scrollWidth / 2) {
                    partnersGrid.scrollLeft = 0;
                }
            }
            
            setInterval(scroll, scrollDelay);
        }
        
        // Start auto-scrolling after a short delay
        setTimeout(autoScrollPartners, 1000);
    });
});

// CSS animations keyframes (to be added via JavaScript)
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);


            