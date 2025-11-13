// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initLoadingScreen();
    initHeaderScroll();
    initMobileMenu();
    initUCForm();
    initFAQ();
    initContactForm();
    initAnimations();
    initPasswordStrength();
});

// Loading Screen
function initLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    const loadingProgress = document.querySelector('.loading-progress');

    // Simulate loading progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);

            // Hide loading screen after a short delay
            setTimeout(() => {
                loadingScreen.style.opacity = '0';
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                }, 500);
            }, 300);
        }

        loadingProgress.style.width = `${progress}%`;
    }, 200);
}

// Header Scroll Effect
function initHeaderScroll() {
    const header = document.querySelector('.header');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Mobile Menu Toggle
function initMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');

    mobileMenuBtn.addEventListener('click', function() {
        nav.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');

        // Transform hamburger to X
        const spans = mobileMenuBtn.querySelectorAll('span');
        if (nav.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('active');
            mobileMenuBtn.classList.remove('active');

            const spans = mobileMenuBtn.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// UC Form Handling
function initUCForm() {
    const ucForm = document.getElementById('uc-form');
    const ucOptions = document.querySelectorAll('.uc-option');
    const ucAmountInput = document.getElementById('uc-amount');

    // UC Amount Selection
    ucOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            ucOptions.forEach(opt => opt.classList.remove('active'));

            // Add active class to clicked option
            this.classList.add('active');

            // Set the hidden input value
            ucAmountInput.value = this.getAttribute('data-amount');
        });
    });

    // Form Submission
    ucForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate form
        if (!validateUCForm()) {
            return;
        }

        // Show success modal
        showSuccessModal(ucAmountInput.value);

        // Reset form
        ucForm.reset();
        ucOptions.forEach(opt => opt.classList.remove('active'));
    });
}

// UC Form Validation
function validateUCForm() {
    const gameId = document.getElementById('game-id').value;
    const server = document.getElementById('server').value;
    const ucAmount = document.getElementById('uc-amount').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const terms = document.getElementById('terms').checked;

    // Game ID validation
    if (!gameId) {
        showError('O\'yin ID kiritilishi shart');
        return false;
    }

    if (!/^\d+$/.test(gameId)) {
        showError('O\'yin ID faqat raqamlardan iborat bo\'lishi kerak');
        return false;
    }

    // Server validation
    if (!server) {
        showError('Server tanlanishi shart');
        return false;
    }

    // UC Amount validation
    if (!ucAmount) {
        showError('UC miqdori tanlanishi shart');
        return false;
    }

    // Email validation
    if (!email) {
        showError('Email kiritilishi shart');
        return false;
    }

    if (!isValidEmail(email)) {
        showError('To\'g\'ri email manzil kiriting');
        return false;
    }

    // Password validation
    if (!password) {
        showError('Parol kiritilishi shart');
        return false;
    }

    if (password.length < 6) {
        showError('Parol kamida 6 ta belgidan iborat bo\'lishi kerak');
        return false;
    }

    // Terms validation
    if (!terms) {
        showError('Foydalanish shartlariga rozilik bildirishingiz shart');
        return false;
    }

    return true;
}

// Email Validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show Error Message
function showError(message) {
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());

    // Create error element
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.cssText = `
        background: rgba(231, 76, 60, 0.1);
        border: 1px solid var(--error-color);
        color: var(--error-color);
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-weight: 600;
    `;
    errorElement.textContent = message;

    // Insert error before the form
    const form = document.getElementById('uc-form');
    form.insertBefore(errorElement, form.firstChild);

    // Auto remove after 5 seconds
    setTimeout(() => {
        errorElement.remove();
    }, 5000);
}

// Success Modal
function showSuccessModal(amount) {
    const modal = document.getElementById('success-modal');
    const successAmount = document.getElementById('success-amount');
    const closeModal = document.querySelector('.close-modal');
    const modalBtn = document.querySelector('.modal-btn');

    // Set the UC amount
    successAmount.textContent = `${amount} UC`;

    // Show modal
    modal.style.display = 'flex';

    // Close modal events
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    modalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// FAQ Toggle
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');

        question.addEventListener('click', function() {
            // Close all other FAQ items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });

            // Toggle current item
            item.classList.toggle('active');
        });
    });
}

// Contact Form
function initContactForm() {
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate form
        if (!validateContactForm()) {
            return;
        }

        // Show success message
        alert('Xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.');

        // Reset form
        contactForm.reset();
    });
}

// Contact Form Validation
function validateContactForm() {
    const name = document.getElementById('contact-name').value;
    const email = document.getElementById('contact-email').value;
    const message = document.getElementById('contact-message').value;

    if (!name) {
        alert('Ism kiritilishi shart');
        return false;
    }

    if (!email) {
        alert('Email kiritilishi shart');
        return false;
    }

    if (!isValidEmail(email)) {
        alert('To\'g\'ri email manzil kiriting');
        return false;
    }

    if (!message) {
        alert('Xabar kiritilishi shart');
        return false;
    }

    return true;
}

// Password Strength Indicator
function initPasswordStrength() {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.querySelector('.strength-bar');

    passwordInput.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;

        // Check password length
        if (password.length >= 6) {
            strength += 1;
        }

        // Check for lowercase letters
        if (/[a-z]/.test(password)) {
            strength += 1;
        }

        // Check for uppercase letters
        if (/[A-Z]/.test(password)) {
            strength += 1;
        }

        // Check for numbers
        if (/[0-9]/.test(password)) {
            strength += 1;
        }

        // Check for special characters
        if (/[^A-Za-z0-9]/.test(password)) {
            strength += 1;
        }

        // Update strength bar
        strengthBar.className = 'strength-bar';

        if (strength <= 2) {
            strengthBar.classList.add('weak');
        } else if (strength <= 4) {
            strengthBar.classList.add('medium');
        } else {
            strengthBar.classList.add('strong');
        }
    });
}

// Scroll Animations
function initAnimations() {
    // Create Intersection Observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const elementsToAnimate = document.querySelectorAll('.about-card, .uc-form, .form-sidebar, .faq-item, .contact-info, .contact-form');

    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });
}

// Additional Features

// Count Up Animation for Stats
function initCountUp() {
    const stats = document.querySelectorAll('.stat-number');

    stats.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/[^0-9]/g, ''));
        const increment = target / 100;
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }

            stat.textContent = Math.floor(current).toLocaleString() + '+';
        }, 20);
    });
}

// Initialize count up when stats are in view
const statsObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            initCountUp();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Form Input Effects
function initInputEffects() {
    const inputs = document.querySelectorAll('.form-group input, .form-group select, .form-group textarea');

    inputs.forEach(input => {
        // Add focus effect
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        // Remove focus effect
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Check if input has value on page load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
}

// Initialize input effects
initInputEffects();

// Smooth Scrolling for Anchor Links
function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize smooth scrolling
initSmoothScroll();

// Add some interactive effects to buttons
function initButtonEffects() {
    const buttons = document.querySelectorAll('.cta-button, .submit-btn, .modal-btn');

    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });

        button.addEventListener('mouseup', function() {
            this.style.transform = '';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// Initialize button effects
initButtonEffects();

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    // Close modal with Escape key
    if (e.key === 'Escape') {
        const modal = document.getElementById('success-modal');
        if (modal.style.display === 'flex') {
            modal.style.display = 'none';
        }
    }
});

// Add some visual effects for UC options
function initUCOptionEffects() {
    const ucOptions = document.querySelectorAll('.uc-option');

    ucOptions.forEach(option => {
        option.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'scale(1.05)';
            }
        });

        option.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = '';
            }
        });
    });
}

// Initialize UC option effects
initUCOptionEffects();

// Add a simple notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 600;
        z-index: 3000;
        transform: translateX(150%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;

    // Set background color based on type
    if (type === 'success') {
        notification.style.background = 'var(--success-color)';
    } else if (type === 'error') {
        notification.style.background = 'var(--error-color)';
    } else if (type === 'warning') {
        notification.style.background = 'var(--warning-color)';
    } else {
        notification.style.background = 'var(--primary-color)';
    }

    // Add to page
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(150%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Add some sample notifications for demo purposes
setTimeout(() => {
    // Show welcome notification after page loads
    showNotification('PUBG Mobile - Tekin UC ga xush kelibsiz!', 'success');
}, 2000);

// Add a simple theme toggle (optional)
function initThemeToggle() {
    // This is a placeholder for potential theme functionality
    // In a real implementation, you might want to add dark/light mode toggle
}

// Add some particle effects for visual appeal (optional)
function initParticles() {
    // This is a placeholder for potential particle effects
    // In a real implementation, you might use a library like particles.js
}

// Final initialization
window.addEventListener('load', function() {
    // Any final initialization after everything is loaded
    console.log('PUBG Mobile - Tekin UC sayti yuklandi!');
});