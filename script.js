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
            // Check URL path first: /es or /pt
            const path = window.location.pathname;
            if (path === '/es' || path.startsWith('/es/')) return 'es';
            if (path === '/pt' || path.startsWith('/pt/')) return 'pt';
            // Then check stored preference
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

            // Page title — only override on pages that have a dedicated translated title
            // (home + science). Other pages (blog articles, live-classes, founder, etc.)
            // keep their own static <title>; clobbering it with meta.title showed the
            // home title everywhere and hurt SEO.
            const _p = window.location.pathname;
            const isScience = /^\/(es\/|pt\/)?science(\.html)?\/?$/.test(_p);
            const isHome = _p === '/' || _p === '/index.html' || _p === '/es' || _p === '/es/' || _p === '/pt' || _p === '/pt/';
            const titleKey = isScience ? 'meta.titleScience' : (isHome ? 'meta.title' : null);
            if (titleKey && t[titleKey]) document.title = t[titleKey];

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

            // Update href values for language-specific links
            document.querySelectorAll('[data-i18n-href]').forEach(el => {
                const key = el.getAttribute('data-i18n-href');
                const value = t[key];
                if (value) el.setAttribute('href', value);
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
            if (heroImg) heroImg.src = 'TAP/NEW/desktop ' + folder + '.webp';
            if (heroSource) heroSource.srcset = 'TAP/NEW/mobile ' + folder + '.webp';

            // Swap feature images per language
            const featureImages = {
                featureImg1: 'TAP',
                featureImg2: 'Calendar',
                featureImg3: 'Milestones',
                featureImg4: 'Report',
                featureImg5: 'Tracker',
                lcHeroCalendar: 'Liveclasses',
            };
            for (const [id, name] of Object.entries(featureImages)) {
                const el = document.getElementById(id);
                if (el) el.src = 'Features/' + folder + '/' + name + ' ' + folder + '.webp';
            }

            // Swap App Store link per language
            const appStoreUrls = {
                en: 'https://apps.apple.com/us/app/kinedu-baby-development/id741277284',
                es: 'https://apps.apple.com/es/app/kinedu-desarrollo-del-beb%C3%A9/id741277284',
                pt: 'https://apps.apple.com/br/app/kinedu-desenvolvimento-do-beb%C3%AA/id741277284',
            };
            const appStoreBadge = document.getElementById('appStoreBadge');
            if (appStoreBadge) appStoreBadge.href = appStoreUrls[lang] || appStoreUrls.en;

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
                if (lang === currentLang) return;

                // For blog articles & blog index, the content is hardcoded HTML — we
                // can't translate client-side. Navigate to the equivalent page in the
                // chosen language instead.
                const path = window.location.pathname;
                const isBlogArticle = path.startsWith('/blog/') ||
                                      path.startsWith('/es/blog/') ||
                                      path.startsWith('/pt/blog/');
                const isBlogIndex = path === '/articles.html' || path === '/articles' ||
                                    path === '/es/articles.html' || path === '/es/articles' ||
                                    path === '/pt/articles.html' || path === '/pt/articles';

                if (isBlogArticle || isBlogIndex) {
                    localStorage.setItem(STORAGE_KEY, lang);
                    if (lang === 'es') {
                        window.location.href = '/es/articles';
                    } else if (lang === 'pt') {
                        window.location.href = '/pt/articles';
                    } else {
                        window.location.href = '/articles.html';
                    }
                    return;
                }

                applyTranslations(lang);
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

        // Create backdrop element
        const backdrop = document.createElement('div');
        backdrop.className = 'nav-menu-backdrop';
        document.body.appendChild(backdrop);

        function openMenu() {
            navLinks.classList.add('active');
            hamburger.classList.add('active');
            if (navPill) navPill.classList.add('menu-open');
            backdrop.classList.add('visible');
        }

        function closeMenu() {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
            if (navPill) navPill.classList.remove('menu-open');
            backdrop.classList.remove('visible');
        }

        hamburger.addEventListener('click', () => {
            navLinks.classList.contains('active') ? closeMenu() : openMenu();
        });

        backdrop.addEventListener('click', closeMenu);

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href') || '';
                if (href.startsWith('#')) {
                    // Hash link — close immediately, smooth scroll will handle it
                    closeMenu();
                } else {
                    // Page/external link — delay so Safari doesn't cancel navigation
                    e.preventDefault();
                    const target = this.getAttribute('target');
                    const url = href;
                    closeMenu();
                    setTimeout(() => {
                        if (target === '_blank') {
                            window.open(url, '_blank');
                        } else {
                            window.location.href = url;
                        }
                    }, 50);
                }
            });
        });
    }


    // --- NAV DROPDOWNS (Learn, Team, ...) ---
    document.querySelectorAll('.nav-dropdown').forEach(function (dropdown) {
        var toggle = dropdown.querySelector('.nav-dropdown-toggle');
        if (!toggle) return;

        function openDropdown() {
            dropdown.classList.add('open');
            toggle.setAttribute('aria-expanded', 'true');
        }
        function closeDropdown() {
            dropdown.classList.remove('open');
            toggle.setAttribute('aria-expanded', 'false');
        }

        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdown.classList.contains('open') ? closeDropdown() : openDropdown();
        });

        dropdown.querySelectorAll('.nd-item').forEach(function (item) {
            item.addEventListener('click', function () {
                closeDropdown();
                var navLinks = document.getElementById('navLinks');
                var hbg = document.getElementById('hamburger');
                var pill = document.querySelector('.nav-pill');
                var bd = document.querySelector('.nav-menu-backdrop');
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    if (hbg) hbg.classList.remove('active');
                    if (pill) pill.classList.remove('menu-open');
                    if (bd) bd.classList.remove('visible');
                }
            });
        });

        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target)) closeDropdown();
        });

        // Desktop: abrir al pasar el cursor (patrón Wonder Weeks del doc)
        if (window.matchMedia('(hover: hover)').matches) {
            var closeTimer = null;
            dropdown.addEventListener('mouseenter', function () {
                if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
                openDropdown();
            });
            dropdown.addEventListener('mouseleave', function () {
                closeTimer = setTimeout(closeDropdown, 300);
            });
        }
    });

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

    // --- HASH ON LOAD (cross-page nav like science.html → /#faq) ---
    // The browser's native anchor jump doesn't account for the sticky navbar,
    // so re-scroll with proper offset once the page has rendered.
    if (window.location.hash) {
        const adjust = () => {
            const target = document.querySelector(window.location.hash);
            if (!target) return;
            const offset = navbar.offsetHeight - 10;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        };
        // Wait for layout (images may shift content) then nudge into place.
        setTimeout(adjust, 50);
        window.addEventListener('load', () => setTimeout(adjust, 50));
    }

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
        '.feature-row, .review-card, .stat-item, .faq-item'
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
        question.setAttribute('aria-expanded', 'false');
        question.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');

            // Close all
            faqItems.forEach(other => {
                other.classList.remove('open');
                const q = other.querySelector('.faq-question');
                if (q) q.setAttribute('aria-expanded', 'false');
            });

            // Toggle clicked
            if (!isOpen) {
                item.classList.add('open');
                question.setAttribute('aria-expanded', 'true');
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
