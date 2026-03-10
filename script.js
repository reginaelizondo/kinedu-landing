/* =========================================
   KINEDU — OPAL-INSPIRED INTERACTIONS
   ========================================= */

document.addEventListener('DOMContentLoaded', () => {

    // --- i18n SYSTEM ---
    (function initI18n() {
        const STORAGE_KEY = 'kinedu-lang';
        const DEFAULT_LANG = 'en';
        const SUPPORTED = ['en', 'es', 'pt'];

        function getInitialLang() {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored && SUPPORTED.includes(stored)) return stored;
            return DEFAULT_LANG;
        }

        let currentLang = getInitialLang();

        function applyTranslations(lang) {
            if (!window.TRANSLATIONS) return;
            const t = window.TRANSLATIONS[lang];
            if (!t) return;

            document.documentElement.lang = lang;

            // Page title
            const isScience = window.location.pathname.includes('science');
            const titleKey = isScience ? 'meta.titleScience' : 'meta.title';
            if (t[titleKey]) document.title = t[titleKey];

            // Standard text replacements
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');

                // Special case: problem words
                if (key === 'problem.words') {
                    rebuildProblemText(el, t[key]);
                    return;
                }

                const value = t[key];
                if (value === undefined) return;

                if (el.hasAttribute('data-i18n-html')) {
                    el.innerHTML = value;
                } else {
                    el.textContent = value;
                }
            });

            // Update toggle buttons
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
            });

            // Swap hero images per language
            const imgMap = { en: 'EN', es: 'ES', pt: 'PT' };
            const folder = imgMap[lang] || 'EN';
            const heroImg = document.getElementById('heroImg');
            const heroSource = document.getElementById('heroSourceMobile');
            if (heroImg) heroImg.src = folder + '/' + (folder === 'EN' ? 'desktop.png' : folder.toLowerCase() + '_desktop.png');
            if (heroSource) heroSource.srcset = folder + '/' + (folder === 'EN' ? 'mobile.png' : folder.toLowerCase() + '_mobile.png');

            localStorage.setItem(STORAGE_KEY, lang);
            currentLang = lang;

            // Remove FOUC class
            document.documentElement.classList.remove('no-fouc');
            document.documentElement.classList.add('fouc-ready');
        }

        function rebuildProblemText(container, words) {
            if (!words || !Array.isArray(words)) return;
            const existingWords = container.querySelectorAll('.word');
            const litStates = Array.from(existingWords).map(w => w.classList.contains('lit'));

            container.innerHTML = words.map((w, i) => {
                const classes = ['word'];
                if (w.a) classes.push('accent');
                if (litStates[i]) classes.push('lit');
                return '<span class="' + classes.join(' ') + '">' + w.t + '</span>';
            }).join('\n');
        }

        // Bind toggle buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.getAttribute('data-lang');
                if (lang !== currentLang) {
                    applyTranslations(lang);
                }
            });
        });

        // Initialize
        applyTranslations(currentLang);
    })();

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
        const navPill = document.querySelector('.nav-pill');
        const navLogo = document.querySelector('.nav-logo');

        hamburger.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
            if (navPill) navPill.classList.toggle('menu-open', isOpen);
            if (navLogo) navLogo.classList.toggle('menu-open', isOpen);
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
                if (navPill) navPill.classList.remove('menu-open');
                if (navLogo) navLogo.classList.remove('menu-open');
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
                const offset = navbar.offsetHeight - 10;
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

    // --- TRUST BAR — Staggered reveal + counting animation ---
    const trustItems = document.querySelectorAll('.trust-item');
    const trustSeps = document.querySelectorAll('.trust-sep');

    // Hide separators initially too
    trustSeps.forEach(sep => { sep.style.opacity = '0'; sep.style.transition = 'opacity 0.4s ease'; });

    const trustObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                trustItems.forEach((item, i) => {
                    setTimeout(() => {
                        item.classList.add('visible');
                        // Animate the counting value
                        const val = item.querySelector('.trust-val[data-count]');
                        if (val) {
                            const target = parseInt(val.getAttribute('data-count'));
                            const suffix = val.getAttribute('data-suffix') || '';
                            animateTrustCount(val, target, suffix);
                        }
                    }, i * 150);
                });
                // Fade in separators
                trustSeps.forEach((sep, i) => {
                    setTimeout(() => { sep.style.opacity = '1'; }, i * 150 + 75);
                });
                trustObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const heroTrust = document.querySelector('.hero-trust');
    if (heroTrust) trustObserver.observe(heroTrust);

    function animateTrustCount(el, target, suffix) {
        const duration = 1200;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
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
        '.feature-row, .step-item, .review-card, .trial-wrap, .stat-item, .faq-item'
    );

    revealElements.forEach(el => el.classList.add('reveal'));

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Stagger based on siblings
                const parent = entry.target.parentElement;
                const siblings = Array.from(parent.children).filter(c => c.classList.contains('reveal'));
                const index = siblings.indexOf(entry.target);

                const delay = entry.target.classList.contains('stat-item') ? 180 : 100;
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, index * delay);

                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

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
