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

    // Science pages have hard-coded translated content per file — always
    // render them in the page's own language (buttons navigate instead).
    (function () {
        const p = window.location.pathname;
        const m = p.match(/^\/(es|pt)\/(?:science(-what-we-know|-what-you-can-do)?|book(?:\/introduction)?)(\.html)?$/);
        if (m) { currentLang = m[1]; }
        else if (/^\/(?:science(-what-we-know|-what-you-can-do)?|book(?:\/introduction)?)(\.html)?$/.test(p)) { currentLang = 'en'; }
        else { return; }
        // La ruta fija el idioma: se guarda para que las páginas a las que se
        // navegue desde aquí (live classes, etc.) sigan en el mismo idioma.
        try { localStorage.setItem(STORAGE_KEY, currentLang); } catch (e) {}
    })();

        // Las páginas del blog cargan solo su idioma (translations-<lang>.js). Si hace
        // falta otro (visitante con preferencia guardada distinta a la carpeta, o cambio
        // de idioma en la página), se carga bajo demanda y se vuelve a aplicar.
        const loadingLang = {};
        function loadLang(lang, cb) {
            if (loadingLang[lang]) return;
            loadingLang[lang] = true;
            const s = document.createElement('script');
            s.src = '/translations-' + lang + '.js?v=1007a';
            s.onload = cb;
            document.head.appendChild(s);
        }

        function applyTranslations(lang) {
            if (!window.TRANSLATIONS) return;
            const t = window.TRANSLATIONS[lang];
            if (!t) { if (SUPPORTED.includes(lang)) loadLang(lang, function () { applyTranslations(lang); }); return; }

            document.documentElement.lang = lang;

            // Page title — only override on pages that have a dedicated translated title
            // (home + science). Other pages (blog articles, live-classes, founder, etc.)
            // keep their own static <title>; clobbering it with meta.title showed the
            // home title everywhere and hurt SEO.
            const _p = window.location.pathname;
            const isScience = /^\/(es\/|pt\/)?science(\.html)?\/?$/.test(_p); // only part 1 has a translated title key
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
            // Only touch src when it actually changes — re-assigning forces a
            // reload/repaint of the hero image (visible flicker at page load).
            const heroDesk = 'TAP/NEW/desktop ' + folder + '.webp?v=4';
            const heroMob = 'TAP/NEW/mobile ' + folder + '.webp?v=4';
            if (heroImg && !heroImg.src.endsWith(encodeURI(heroDesk))) heroImg.src = heroDesk;
            if (heroSource && heroSource.srcset !== heroMob) heroSource.srcset = heroMob;

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
                if (el) el.src = '/Features/' + folder + '/' + name + ' ' + folder + '.webp?v=3';
            }

            // Swap App Store link per language
            const appStoreUrls = {
                en: 'https://apps.apple.com/us/app/kinedu-baby-development/id741277284',
                es: 'https://apps.apple.com/es/app/kinedu-desarrollo-del-beb%C3%A9/id741277284',
                pt: 'https://apps.apple.com/br/app/kinedu-desenvolvimento-do-beb%C3%AA/id741277284',
            };
            const appStoreBadge = document.getElementById('appStoreBadge');
            if (appStoreBadge) appStoreBadge.href = appStoreUrls[lang] || appStoreUrls.en;

            // La preferencia SOLO se guarda cuando la persona elige en el switcher
            // (abajo). Antes se guardaba en cada carga, lo que pisaba la señal de
            // "no ha elegido" y rompía la auto-detección por idioma del dispositivo.
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

                // Feedback #3: el idioma debe CAMBIAR LA URL cuando la página
                // tiene versión propia. La fuente de verdad son los hreflang
                // del <head> (los mismos que lee Google): si existe alternate
                // para ese idioma y es otra ruta, navegamos ahí. Se navega
                // relativo (pathname) para que funcione igual en local y prod.
                const alt = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
                if (alt) {
                    try {
                        const u = new URL(alt.getAttribute('href'), window.location.href);
                        if (u.pathname !== window.location.pathname) {
                            localStorage.setItem(STORAGE_KEY, lang);
                            window.location.href = u.pathname + u.search + window.location.hash;
                            return;
                        }
                    } catch (e) { /* href raro: seguimos con el swap normal */ }
                }

                // For blog articles & blog index, the content is hardcoded HTML — we
                // can't translate client-side. Navigate to the equivalent page in the
                // chosen language instead.
                const path = window.location.pathname;
                const isBlogArticle = path.startsWith('/blog/') ||
                                      path.startsWith('/es/blog/') ||
                                      path.startsWith('/pt/blog/');
                const isBlogIndex = /^\/(?:es\/|pt\/)?(?:blog|articles)(?:\.html)?\/?$/.test(path);

                const sciM = path.match(/^\/(?:es\/|pt\/)?science(-what-we-know|-what-you-can-do)?(?:\.html)?$/);
                if (sciM) {
                    localStorage.setItem(STORAGE_KEY, lang);
                    const suf = sciM[1] || '';
                    window.location.href = (lang === 'es' ? '/es' : lang === 'pt' ? '/pt' : '') + '/science' + suf;
                    return;
                }
                const bkM = path.match(/^\/(?:es\/|pt\/)?book(\/introduction)?(?:\.html)?$/);
                if (bkM) {
                    localStorage.setItem(STORAGE_KEY, lang);
                    window.location.href = (lang === 'es' ? '/es' : lang === 'pt' ? '/pt' : '') + '/book' + (bkM[1] || '');
                    return;
                }
                if (/^\/(?:es\/|pt\/)?gift(?:\.html)?$/.test(path)) {
                    localStorage.setItem(STORAGE_KEY, lang);
                    window.location.href = (lang === 'es' ? '/es' : lang === 'pt' ? '/pt' : '') + '/gift';
                    return;
                }
                if (isBlogArticle || isBlogIndex) {
                    localStorage.setItem(STORAGE_KEY, lang);
                    if (lang === 'es') {
                        window.location.href = '/es/blog';
                    } else if (lang === 'pt') {
                        window.location.href = '/pt/blog';
                    } else {
                        window.location.href = '/blog';
                    }
                    return;
                }

                localStorage.setItem(STORAGE_KEY, lang);
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

        // Bubble móvil (clon del nav de Masterclasses): los desplegables se
        // aplanan. Un desplegable cuyo primer item apunta a una página propia
        // (Science → /science) se vuelve UN link plano con la etiqueta del
        // botón; el desplegable original se esconde en móvil (CSS
        // .nav-dd--collapse). Team no tiene página: su botón se esconde y
        // Founder / Experts quedan como links sueltos (solo CSS).
        navLinks.querySelectorAll('.nav-dropdown').forEach(dd => {
            if (dd.id === 'teamDropdown' || dd.id === 'classesDropdown') return; // ambos se aplanan en sus items (solo CSS)
            const label = dd.querySelector('.nav-dropdown-toggle span');
            const first = dd.querySelector('.nd-item');
            const href = first && first.getAttribute('href');
            if (!label || !href) return;
            const flat = document.createElement('a');
            flat.href = href.split('#')[0] || href;
            flat.className = 'nav-flat mobile-only';
            flat.appendChild(label.cloneNode(true)); // conserva data-i18n → se traduce igual
            dd.insertAdjacentElement('beforebegin', flat);
            dd.classList.add('nav-dd--collapse');
        });

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
            // Cierra cualquier otro dropdown abierto para que nunca se solapen dos
            // (antes, al pasar de Science a Team, ambos quedaban abiertos 300ms).
            document.querySelectorAll('.nav-dropdown.open').forEach(function (other) {
                if (other === dropdown) return;
                other.classList.remove('open');
                var t = other.querySelector('.nav-dropdown-toggle');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
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
            const target = document.querySelector(href);
            // Sin target (p.ej. #app/#assessment de science, que activan un panel
            // vía 'hashchange'): dejamos el comportamiento por defecto para que el
            // hash sí cambie. Antes hacíamos preventDefault siempre y esos enlaces
            // quedaban muertos.
            if (!target) return;
            e.preventDefault();
            const offset = navbar.offsetHeight - 10;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
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


    // --- TRUST BAR — estática: números fijos del HTML, sin reveal ni conteo ---
    // (Se eliminó el IntersectionObserver + animateTrustCount a pedido: la
    //  barra debe verse quieta desde el primer pintado.)

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

    // Feedback #17: el reveal iba ~2s detrás del scroll (disparo tardío +
    // stagger largo + transición de 0.8s = secciones en blanco). Ahora:
    // dispara 30% de viewport ANTES de que el elemento entre (rootMargin
    // positivo), el stagger se acota a 210ms, y si el elemento ya está bien
    // adentro (llegada directa por ancla o scroll rápido) aparece al instante.
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const parent = entry.target.parentElement;
                const siblings = Array.from(parent.children).filter(c => c.classList.contains('reveal'));
                const index = siblings.indexOf(entry.target);

                const yaVisible = entry.boundingClientRect.top < window.innerHeight * 0.75;
                const delay = yaVisible ? 0 : Math.min(index * 70, 210);
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, delay);

                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0, rootMargin: '0px 0px 30% 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // --- FAQ ACCORDION ---
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (!question) return; // páginas con su propio FAQ (p. ej. /gift) no usan este markup
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

/* ===== Contact us: formulario en la página en vez de mailto (oct-2026) =====
   Antes el link abría la app de correo con un mensaje vacío y muchos lo cerraban
   sin escribir. Ahora abre un formulario corto aquí mismo; el mensaje sale por
   /masterclasses/api/contact (mismo dominio) hacia hello@kinedu.com, el mismo
   help desk de siempre. Si el envío falla, se abre el mailto con el texto ya
   escrito: nunca se pierde un mensaje. Se mide: abierto, enviado, fallback. */
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('a[href^="mailto:hello@kinedu.com"]'));
  if (!links.length) return;
  var P = location.pathname;
  var L = P.indexOf('/es/') === 0 || P === '/es' ? 'es' : P.indexOf('/pt/') === 0 || P === '/pt' ? 'pt' : 'en';
  var T = {
    en: { title: 'Write to us', sub: 'A real person at Kinedu answers every message, usually within a day.', name: 'Your name', email: 'Your email', msg: 'How can we help?', send: 'Send message', sending: 'Sending…', ok: 'Sent. We will write back to', fail: 'We could not send it from here. Your email app will open with your message ready.', close: 'Close', or: 'Or write directly to hello@kinedu.com' },
    es: { title: 'Escríbenos', sub: 'Una persona real de Kinedu contesta cada mensaje, normalmente en un día.', name: 'Tu nombre', email: 'Tu correo', msg: '¿En qué te ayudamos?', send: 'Enviar mensaje', sending: 'Enviando…', ok: 'Enviado. Te respondemos a', fail: 'No pudimos enviarlo desde aquí. Se abrirá tu app de correo con el mensaje listo.', close: 'Cerrar', or: 'O escribe directo a hello@kinedu.com' },
    pt: { title: 'Fale conosco', sub: 'Uma pessoa real da Kinedu responde cada mensagem, normalmente em um dia.', name: 'Seu nome', email: 'Seu e-mail', msg: 'Como podemos ajudar?', send: 'Enviar mensagem', sending: 'Enviando…', ok: 'Enviado. Vamos responder para', fail: 'Não conseguimos enviar daqui. Seu app de e-mail vai abrir com a mensagem pronta.', close: 'Fechar', or: 'Ou escreva direto para hello@kinedu.com' }
  }[L];
  function track(label) { try { navigator.sendBeacon('/api/track', JSON.stringify({ page: P, lang: L, event: 'conversion', cta: label })); } catch (e) {} }
  var css = '.kc-ov{position:fixed;inset:0;background:rgba(8,27,70,.45);z-index:10000;display:flex;align-items:flex-end;justify-content:center;padding:0}' +
    '@media(min-width:641px){.kc-ov{align-items:center;padding:24px}}' +
    '.kc-box{background:#fff;width:100%;max-width:440px;border-radius:22px 22px 0 0;padding:22px 20px calc(22px + env(safe-area-inset-bottom));box-shadow:0 20px 60px rgba(8,27,70,.25);font-family:"Proxima Nova","Plus Jakarta Sans","Segoe UI",Helvetica,Arial,sans-serif;color:#1A1D2E;position:relative}' +
    '@media(min-width:641px){.kc-box{border-radius:22px;padding:26px 26px}}' +
    '.kc-x{position:absolute;top:12px;right:12px;width:34px;height:34px;border:0;border-radius:50%;background:#F1F3F7;font-size:20px;line-height:1;color:#5B6170;cursor:pointer}' +
    '.kc-box h3{margin:0 32px 6px 0;font-size:21px;font-weight:800;letter-spacing:-.3px;color:#0A2540}.kc-box p{margin:0 0 14px;font-size:14px;color:#5B6170;line-height:1.5}' +
    '.kc-box input,.kc-box textarea{display:block;width:100%;box-sizing:border-box;border:1.5px solid #E3E6EE;border-radius:12px;padding:12px 14px;font:inherit;font-size:16px;margin:0 0 10px;background:#FBFAF8;color:#1A1D2E}' +
    '.kc-box input:focus,.kc-box textarea:focus{outline:none;border-color:#087BF3;background:#fff}.kc-box textarea{min-height:110px;resize:vertical}' +
    '.kc-hp{position:absolute;left:-9999px;top:-9999px;height:0;width:0;opacity:0}' +
    '.kc-btn{display:block;width:100%;border:0;border-radius:999px;background:#087BF3;color:#fff;font:inherit;font-size:16px;font-weight:700;padding:14px 18px;cursor:pointer}.kc-btn[disabled]{opacity:.6;cursor:default}' +
    '.kc-alt{display:block;text-align:center;font-size:12.5px;color:#9AA0AD;margin:12px 0 0}.kc-alt a{color:#087BF3;text-decoration:none}' +
    '.kc-ok{text-align:center;padding:18px 0 6px}.kc-ok .kc-ico{width:56px;height:56px;border-radius:50%;background:#E4F6E7;color:#23803A;font-size:28px;line-height:56px;margin:0 auto 12px}' +
    '.kc-err{background:#FDEBD8;color:#B4531F;border-radius:10px;padding:10px 12px;font-size:13.5px;margin:0 0 10px}';
  var style = document.createElement('style'); style.textContent = css; document.head.appendChild(style);
  function mailtoFallback(name, email, msg) {
    var subject = encodeURIComponent('Contact us (kinedu.com)');
    var body = encodeURIComponent((name ? name + '\n' : '') + (email ? email + '\n\n' : '') + msg);
    location.href = 'mailto:hello@kinedu.com?subject=' + subject + '&body=' + body;
  }
  function open() {
    track('Contact us — opened');
    var ov = document.createElement('div'); ov.className = 'kc-ov';
    ov.innerHTML = '<div class="kc-box" role="dialog" aria-modal="true" aria-label="' + T.title + '"><button type="button" class="kc-x" aria-label="' + T.close + '">&times;</button>' +
      '<h3>' + T.title + '</h3><p>' + T.sub + '</p>' +
      '<form novalidate><input type="text" name="name" placeholder="' + T.name + '" autocomplete="name">' +
      '<input type="email" name="email" placeholder="' + T.email + '" autocomplete="email" required>' +
      '<textarea name="message" placeholder="' + T.msg + '" required></textarea>' +
      '<input type="text" name="website" class="kc-hp" tabindex="-1" autocomplete="off">' +
      '<div class="kc-err" style="display:none"></div>' +
      '<button type="submit" class="kc-btn">' + T.send + '</button>' +
      '<span class="kc-alt"><a href="mailto:hello@kinedu.com" data-kc-direct="1">' + T.or + '</a></span></form></div>';
    document.body.appendChild(ov);
    var box = ov.querySelector('.kc-box'), form = ov.querySelector('form'), err = ov.querySelector('.kc-err'), btn = ov.querySelector('.kc-btn');
    function close() { ov.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    document.addEventListener('keydown', onKey);
    ov.querySelector('.kc-x').addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    ov.querySelector('[data-kc-direct]').addEventListener('click', function () { track('Contact us — direct mailto'); close(); });
    setTimeout(function () { var f = form.querySelector('input[name=name]'); if (f) f.focus(); }, 50);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.name.value.trim(), email = form.email.value.trim(), msg = form.message.value.trim();
      err.style.display = 'none';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || msg.length < 5) {
        err.textContent = T.email + ' · ' + T.msg; err.style.display = 'block'; return;
      }
      btn.disabled = true; btn.textContent = T.sending;
      var payload = JSON.stringify({ name: name, email: email, message: msg, website: form.website.value, page: location.href, lang: L });
      var done = false;
      var timer = setTimeout(function () { if (!done) { done = true; fail(); } }, 12000);
      function fail() {
        track('Contact us — fallback mailto');
        box.innerHTML = '<button type="button" class="kc-x" aria-label="' + T.close + '">&times;</button><div class="kc-ok"><p>' + T.fail + '</p></div>';
        box.querySelector('.kc-x').addEventListener('click', close);
        setTimeout(function () { mailtoFallback(name, email, msg); }, 900);
      }
      fetch('/masterclasses/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: payload })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (d) {
          if (done) return; done = true; clearTimeout(timer);
          if (!d || !d.ok) return fail();
          track('Contact us — sent');
          box.innerHTML = '<button type="button" class="kc-x" aria-label="' + T.close + '">&times;</button><div class="kc-ok"><div class="kc-ico">&#10003;</div><h3>' + T.ok + '<br>' + email.replace(/</g, '&lt;') + '</h3></div>';
          box.querySelector('.kc-x').addEventListener('click', close);
        })
        .catch(function () { if (done) return; done = true; clearTimeout(timer); fail(); });
    });
  }
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (a.getAttribute('data-kc-direct')) return;
      e.preventDefault(); open();
    });
  });
})();
