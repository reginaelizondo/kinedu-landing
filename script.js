/* =========================================
   KINEDU — OPAL-INSPIRED INTERACTIONS
   ========================================= */

document.addEventListener('DOMContentLoaded', () => {

    // --- NAVBAR SCROLL EFFECT ---
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- HAMBURGER MENU ---
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }

    // --- SMOOTH SCROLL ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offset = navbar.offsetHeight + 20;
                const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // --- ACTIVE NAV LINK ON SCROLL ---
    const navLinkItems = document.querySelectorAll('.nav-links a[href^="#"]');
    const sections = [];

    navLinkItems.forEach(link => {
        const href = link.getAttribute('href');
        const section = document.querySelector(href);
        if (section) sections.push({ link, section });
    });

    function updateActiveNav() {
        const scrollY = window.pageYOffset + 150;
        let current = null;

        sections.forEach(({ link, section }) => {
            const top = section.offsetTop;
            const bottom = top + section.offsetHeight;
            if (scrollY >= top && scrollY < bottom) {
                current = link;
            }
        });

        navLinkItems.forEach(l => l.classList.remove('active'));
        if (current) current.classList.add('active');
    }

    window.addEventListener('scroll', updateActiveNav, { passive: true });
    updateActiveNav();

    // --- PROGRESS BAR FILL ANIMATION ---
    const barFills = document.querySelectorAll('.bar-fill');
    const deviceObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                barFills.forEach((fill, i) => {
                    setTimeout(() => {
                        fill.style.width = fill.getAttribute('data-width');
                    }, i * 200 + 300);
                });
                deviceObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const heroDevice = document.querySelector('.hero-device');
    if (heroDevice) deviceObserver.observe(heroDevice);

    // --- PROBLEM TEXT — Illuminate words on scroll ---
    const problemSection = document.getElementById('problem');
    const words = document.querySelectorAll('.problem-text .word');

    if (problemSection && words.length > 0) {
        const illuminateWords = () => {
            const rect = problemSection.getBoundingClientRect();
            const windowH = window.innerHeight;

            // Calculate progress: 0 when section enters, 1 when section leaves
            const sectionTop = rect.top;
            const sectionHeight = rect.height;
            const triggerStart = windowH * 0.8;
            const triggerEnd = windowH * 0.2;

            const progress = Math.min(1, Math.max(0,
                (triggerStart - sectionTop) / (triggerStart - triggerEnd + sectionHeight * 0.3)
            ));

            const wordsToLight = Math.floor(progress * words.length);

            words.forEach((word, i) => {
                if (i < wordsToLight) {
                    word.classList.add('lit');
                } else {
                    word.classList.remove('lit');
                }
            });
        };

        window.addEventListener('scroll', illuminateWords, { passive: true });
        illuminateWords(); // run once on load
    }

    // --- ANIMATED COUNTERS ---
    const statNums = document.querySelectorAll('.stat-num');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-target'));
                const suffix = el.getAttribute('data-suffix') || '';
                animateCounter(el, target, suffix);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    statNums.forEach(num => counterObserver.observe(num));

    function animateCounter(el, target, suffix) {
        const duration = 2000;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out quart
            const eased = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(target * eased);

            el.textContent = current.toLocaleString() + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.textContent = target.toLocaleString() + suffix;
            }
        }

        requestAnimationFrame(update);
    }

    // --- GRAPH BARS ANIMATION ---
    const graphBars = document.querySelectorAll('.graph-bar');

    const graphObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bars = entry.target.querySelectorAll('.graph-bar');
                bars.forEach((bar, i) => {
                    setTimeout(() => {
                        bar.style.height = bar.getAttribute('data-height');
                    }, i * 300 + 200);
                });
                graphObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const graphWrap = document.querySelector('.graph-bars-wrap');
    if (graphWrap) graphObserver.observe(graphWrap);

    // --- SCROLL REVEAL ---
    const revealElements = document.querySelectorAll(
        '.feature-carousel, .step-item, .testi-card, .trial-wrap, .stat-item, .faq-item'
    );

    revealElements.forEach(el => el.classList.add('reveal'));

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Stagger based on siblings
                const parent = entry.target.parentElement;
                const siblings = Array.from(parent.children).filter(c => c.classList.contains('reveal'));
                const index = siblings.indexOf(entry.target);

                setTimeout(() => {
                    entry.target.classList.add('active');
                }, index * 100);

                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // --- FEATURE CAROUSEL — Immersive Color-Shifting ---
    const fcCarousel = document.querySelector('.feature-carousel');
    if (fcCarousel) {
        const slideImgs = fcCarousel.querySelectorAll('.fc-slide-img');
        const slideTexts = fcCarousel.querySelectorAll('.fc-slide');
        const dots = fcCarousel.querySelectorAll('.fc-dot');
        const prevBtn = fcCarousel.querySelector('.fc-arrow--prev');
        const nextBtn = fcCarousel.querySelector('.fc-arrow--next');
        const totalSlides = slideTexts.length;
        let currentSlide = 0;
        let autoplayTimer = null;
        const AUTO_INTERVAL = 5000;

        function goToSlide(index) {
            if (index < 0) index = totalSlides - 1;
            if (index >= totalSlides) index = 0;

            // Update images (crossfade with blur/scale)
            slideImgs.forEach(img => img.classList.remove('active'));
            slideImgs[index].classList.add('active');

            // Update text slides
            slideTexts.forEach(s => s.classList.remove('active'));
            slideTexts[index].classList.add('active');

            // Update dots
            dots.forEach(d => {
                d.classList.remove('active');
                d.style.animation = 'none';
            });

            dots[index].classList.add('active');

            // Restart progress bar animation
            void dots[index].offsetWidth;
            dots[index].style.animation = '';

            currentSlide = index;
        }

        function nextSlide() { goToSlide(currentSlide + 1); }
        function prevSlide() { goToSlide(currentSlide - 1); }

        function startAutoplay() {
            stopAutoplay();
            autoplayTimer = setInterval(nextSlide, AUTO_INTERVAL);
        }

        function stopAutoplay() {
            if (autoplayTimer) {
                clearInterval(autoplayTimer);
                autoplayTimer = null;
            }
        }

        // Arrow clicks
        nextBtn.addEventListener('click', () => { nextSlide(); startAutoplay(); });
        prevBtn.addEventListener('click', () => { prevSlide(); startAutoplay(); });

        // Dot clicks
        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                goToSlide(parseInt(dot.dataset.index));
                startAutoplay();
            });
        });

        // Pause on hover
        fcCarousel.addEventListener('mouseenter', stopAutoplay);
        fcCarousel.addEventListener('mouseleave', startAutoplay);

        // Touch swipe
        let touchStartX = 0;
        fcCarousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            stopAutoplay();
        }, { passive: true });

        fcCarousel.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) nextSlide(); else prevSlide();
            }
            startAutoplay();
        }, { passive: true });

        // Keyboard accessibility
        fcCarousel.setAttribute('tabindex', '0');
        fcCarousel.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                e.preventDefault(); nextSlide(); startAutoplay();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                e.preventDefault(); prevSlide(); startAutoplay();
            }
        });

        startAutoplay();
    }

    // --- FAQ ACCORDION ---
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');

            // Close all
            faqItems.forEach(other => other.classList.remove('open'));

            // Toggle clicked
            if (!isOpen) {
                item.classList.add('open');
            }
        });
    });

    // --- TILT EFFECT on testimonial cards ---
    const testiCards = document.querySelectorAll('.testi-card');

    testiCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 25;
            const rotateY = (centerX - x) / 25;

            card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) translateY(0)';
        });
    });


    // --- MOUSE GLOW on hero (optional subtle effect) ---
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth) * 100;
            const y = (e.clientY / window.innerHeight) * 100;
            hero.style.setProperty('--mouse-x', x + '%');
            hero.style.setProperty('--mouse-y', y + '%');
        });
    }


});
