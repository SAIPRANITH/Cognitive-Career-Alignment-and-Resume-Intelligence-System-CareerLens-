document.addEventListener('DOMContentLoaded', () => {

    // ══════════════════════════════════════
    //  FILE UPLOAD DRAG & DROP
    // ══════════════════════════════════════
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const clearFileBtn = document.getElementById('clearFile');
    const submitBtn = document.getElementById('submitBtn');
    const uploadForm = document.getElementById('uploadForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (fileInput && dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        });

        fileInput.addEventListener('change', function() {
            handleFiles(this.files);
        });

        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                const validExts = ['pdf', 'docx'];
                const ext = file.name.split('.').pop().toLowerCase();
                
                if (!validExts.includes(ext)) {
                    alert('Only PDF and DOCX files are supported.');
                    clearFile();
                    return;
                }
                
                if (file.size > 16 * 1024 * 1024) {
                    alert('File must be smaller than 16MB.');
                    clearFile();
                    return;
                }

                if (fileInput.files.length === 0 || fileInput.files[0] !== file) {
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    fileInput.files = dt.files;
                }

                fileName.textContent = file.name;
                fileSize.textContent = formatBytes(file.size);
                
                dropZone.classList.add('d-none');
                fileInfo.classList.remove('d-none');
                submitBtn.disabled = false;
                
                // Animate the file info appearance
                fileInfo.style.animation = 'fadeInUp 0.5s ease-out';
            }
        }

        function clearFile() {
            fileInput.value = '';
            dropZone.classList.remove('d-none');
            fileInfo.classList.add('d-none');
            submitBtn.disabled = true;
        }

        if (clearFileBtn) {
            clearFileBtn.addEventListener('click', clearFile);
        }

        if (uploadForm) {
            uploadForm.addEventListener('submit', () => {
                if (loadingOverlay) loadingOverlay.classList.remove('d-none');
                submitBtn.disabled = true;
            });
        }
    }

    // ══════════════════════════════════════
    //  ANIMATED COUNTERS
    // ══════════════════════════════════════
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        if (isNaN(target)) return;
        
        const duration = 1500;
        const startTime = performance.now();
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(eased * target);
            
            counter.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        }
        
        // Use IntersectionObserver to trigger when visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    requestAnimationFrame(updateCounter);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });

    // ══════════════════════════════════════
    //  SCROLL REVEAL ANIMATION
    // ══════════════════════════════════════
    const revealElements = document.querySelectorAll('.reveal, .glass-card, .card');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add staggered delay based on position
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 80);
                revealObserver.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => {
        // Only apply if not already animated
        if (!el.classList.contains('fade-in-up') && !el.style.animation) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            revealObserver.observe(el);
        }
    });

    // ══════════════════════════════════════
    //  PROGRESS BAR ANIMATION
    // ══════════════════════════════════════
    const progressBars = document.querySelectorAll('.progress-bar');
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const targetWidth = bar.style.width;
                bar.style.width = '0%';
                bar.style.transition = 'width 1.2s cubic-bezier(0.16, 1, 0.3, 1)';
                setTimeout(() => {
                    bar.style.width = targetWidth;
                }, 100);
                progressObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.3 });

    progressBars.forEach(bar => progressObserver.observe(bar));

    // ══════════════════════════════════════
    //  BADGE SKILL HOVER EFFECTS
    // ══════════════════════════════════════
    document.querySelectorAll('.badge').forEach(badge => {
        badge.classList.add('badge-hover');
    });

    // ══════════════════════════════════════
    //  NAVBAR SCROLL EFFECT
    // ══════════════════════════════════════
    const navbar = document.querySelector('.glass-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.backdropFilter = 'blur(30px)';
                navbar.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.8)';
            } else {
                navbar.style.backdropFilter = 'blur(24px)';
                navbar.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.5)';
            }
        });
    }

    // ══════════════════════════════════════
    //  SMOOTH SCROLL FOR ANCHOR LINKS
    // ══════════════════════════════════════
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ══════════════════════════════════════
    //  TYPEWRITER ANIMATION
    // ══════════════════════════════════════
    document.querySelectorAll('.typewriter-text').forEach(el => {
        const text = el.textContent;
        const chars = text.length;
        el.style.animationDuration = `${Math.max(1, chars * 0.06)}s, 0.75s`;
    });

    // ══════════════════════════════════════
    //  REDUCED MOTION CHECK
    // ══════════════════════════════════════
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('.float-element, .scan-line, .cyber-grid').forEach(el => {
            el.style.animation = 'none';
        });
    }

    // ══════════════════════════════════════
    //  UTILITY
    // ══════════════════════════════════════
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }



    // ══════════════════════════════════════
    //  SCROLL-TRIGGERED FADE-IN ANIMATIONS
    // ══════════════════════════════════════
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.fade-in-up').forEach(el => {
        // Set initial state via JS to avoid flash
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        fadeObserver.observe(el);
    });

    // Add CSS for the visible state dynamically
    if (!document.getElementById('fade-in-style')) {
        const style = document.createElement('style');
        style.id = 'fade-in-style';
        style.textContent = `.fade-in-up.visible { opacity: 1 !important; transform: translateY(0) !important; transition: opacity 0.7s cubic-bezier(0.4,0,0.2,1), transform 0.7s cubic-bezier(0.4,0,0.2,1); }`;
        document.head.appendChild(style);
    }

    // ══════════════════════════════════════
    //  SCROLL PROGRESS INDICATOR
    // ══════════════════════════════════════
    let scrollBar = document.querySelector('.scroll-indicator');
    if (!scrollBar) {
        scrollBar = document.createElement('div');
        scrollBar.className = 'scroll-indicator';
        scrollBar.style.width = '0%';
        document.body.prepend(scrollBar);
    }
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight > 0) {
            scrollBar.style.width = (scrollTop / docHeight * 100) + '%';
        }
    }, { passive: true });

    // ══════════════════════════════════════
    //  BUTTON RIPPLE EFFECT
    // ══════════════════════════════════════
    document.querySelectorAll('.btn-ripple').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255,255,255,0.3)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'rippleAnim 0.6s ease-out forwards';
            ripple.style.pointerEvents = 'none';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // ══════════════════════════════════════
    //  (Removed Magnetic Cursor & Glitch)
    // ══════════════════════════════════════

    // ══════════════════════════════════════
    //  WORD-BY-WORD REVEAL ON HERO SUBTITLE
    // ══════════════════════════════════════
    document.querySelectorAll('.hero-subtitle').forEach(el => {
        const words = el.textContent.trim().split(/\s+/);
        el.innerHTML = '';
        el.classList.add('word-reveal');
        words.forEach((word, i) => {
            const span = document.createElement('span');
            span.textContent = word + '\u00A0';
            span.style.animationDelay = `${0.8 + i * 0.04}s`;
            el.appendChild(span);
        });
    });

    // ══════════════════════════════════════
    //  INJECT AURORA BLOBS INTO HERO
    // ══════════════════════════════════════
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.style.position = 'relative';
        ['a1', 'a2', 'a3'].forEach(cls => {
            const blob = document.createElement('div');
            blob.className = `aurora-glow ${cls}`;
            heroSection.appendChild(blob);
        });
        // Also inject morph blob
        const morphBlob = document.createElement('div');
        morphBlob.className = 'morph-blob';
        morphBlob.style.top = '20%';
        morphBlob.style.left = '50%';
        morphBlob.style.transform = 'translateX(-50%)';
        heroSection.appendChild(morphBlob);
    }

    // ══════════════════════════════════════
    //  3D TILT ON TECH FACT BOXES
    // ══════════════════════════════════════
    document.querySelectorAll('.tech-fact-box, .feature-card').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `perspective(800px) rotateY(${x * 12}deg) rotateX(${-y * 12}deg) scale(1.02)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.transition = 'transform 0.5s ease';
        });
        card.addEventListener('mouseenter', () => {
            card.style.transition = 'none';
        });
    });

    // ══════════════════════════════════════
    //  SCROLL SPARK PARTICLES
    // ══════════════════════════════════════
    let lastScrollY = window.scrollY;
    let scrollThrottle = false;
    window.addEventListener('scroll', () => {
        if (scrollThrottle) return;
        scrollThrottle = true;
        setTimeout(() => { scrollThrottle = false; }, 60);

        const delta = Math.abs(window.scrollY - lastScrollY);
        lastScrollY = window.scrollY;
        if (delta > 15) {
            for (let i = 0; i < 3; i++) {
                const p = document.createElement('div');
                p.className = 'scroll-particle';
                p.style.left = (Math.random() * window.innerWidth) + 'px';
                p.style.top = (Math.random() * window.innerHeight) + 'px';
                document.body.appendChild(p);
                setTimeout(() => p.remove(), 800);
            }
        }
    }, { passive: true });

    // ══════════════════════════════════════
    //  NUMBER COUNTING WITH SUFFIX
    // ══════════════════════════════════════
    document.querySelectorAll('[data-count-to]').forEach(el => {
        const target = parseFloat(el.getAttribute('data-count-to'));
        const suffix = el.getAttribute('data-suffix') || '';
        const decimals = target % 1 !== 0 ? 1 : 0;
        const duration = 2000;
        const startTime = performance.now();

        function tick(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = (eased * target).toFixed(decimals) + suffix;
            if (progress < 1) requestAnimationFrame(tick);
        }

        const obs = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {
                requestAnimationFrame(tick);
                obs.unobserve(el);
            }
        }, { threshold: 0.5 });
        obs.observe(el);
    });

    // ══════════════════════════════════════
    //  LENIS SMOOTH SCROLLING
    // ══════════════════════════════════════
    if (typeof Lenis !== 'undefined') {
        const lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), 
            smooth: true,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
    }

    // ══════════════════════════════════════
    //  LETTER-BY-LETTER REVEAL (HEADINGS)
    // ══════════════════════════════════════
    document.querySelectorAll('.letter-reveal').forEach(el => {
        const text = el.textContent.trim();
        el.innerHTML = '';
        [...text].forEach((letter, i) => {
            const span = document.createElement('span');
            span.textContent = letter === ' ' ? '\u00A0' : letter;
            span.style.animationDelay = `${i * 0.03}s`;
            el.appendChild(span);
        });
    });

    // ══════════════════════════════════════
    //  IMAGE OBSERVER (FADE-IN & CLIP REVEAL)
    // ══════════════════════════════════════
    const imgObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-revealed');
                imgObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.img-fade-in, .img-clip-reveal').forEach(img => {
        imgObserver.observe(img);
    });

    // ══════════════════════════════════════
    //  NEW ANIMATIONS & EFFECTS
    // ══════════════════════════════════════

    // 1. Text Scramble
    class TextScramble {
        constructor(el) {
            this.el = el;
            this.chars = '!<>-_\\\\/[]{}—=+*^?#________';
            this.update = this.update.bind(this);
        }
        setText(newText) {
            const oldText = this.el.innerText;
            const length = Math.max(oldText.length, newText.length);
            const promise = new Promise((resolve) => this.resolve = resolve);
            this.queue = [];
            for (let i = 0; i < length; i++) {
                const from = oldText[i] || '';
                const to = newText[i] || '';
                const start = Math.floor(Math.random() * 40);
                const end = start + Math.floor(Math.random() * 40);
                this.queue.push({ from, to, start, end });
            }
            cancelAnimationFrame(this.frameRequest);
            this.frame = 0;
            this.update();
            return promise;
        }
        update() {
            let output = '';
            let complete = 0;
            for (let i = 0, n = this.queue.length; i < n; i++) {
                let { from, to, start, end, char } = this.queue[i];
                if (this.frame >= end) {
                    complete++;
                    output += to;
                } else if (this.frame >= start) {
                    if (!char || Math.random() < 0.28) {
                        char = this.randomChar();
                        this.queue[i].char = char;
                    }
                    output += `<span style="color:#00e5ff">${char}</span>`;
                } else {
                    output += from;
                }
            }
            this.el.innerHTML = output;
            if (complete === this.queue.length) {
                this.resolve();
            } else {
                this.frameRequest = requestAnimationFrame(this.update);
                this.frame++;
            }
        }
        randomChar() {
            return this.chars[Math.floor(Math.random() * this.chars.length)];
        }
    }

    document.querySelectorAll('[data-scramble]').forEach(el => {
        const fx = new TextScramble(el);
        const text = el.getAttribute('data-scramble');
        const obs = new IntersectionObserver(e => {
            if (e[0].isIntersecting) { fx.setText(text); obs.unobserve(el); }
        });
        obs.observe(el);
    });

    // 2. Parallax Orbs
    const orbs = [];
    for(let i=0; i<3; i++) {
        let orb = document.createElement('div');
        orb.className = 'aurora-glow';
        orb.style.position = 'fixed';
        orb.style.top = Math.random() * 100 + 'vh';
        orb.style.left = Math.random() * 100 + 'vw';
        orb.style.zIndex = -5;
        orb.style.opacity = 0.3;
        document.body.appendChild(orb);
        orbs.push({el: orb, speed: Math.random() * 0.5 + 0.1});
    }
    
    // 3. Scroll Update (Progress & Skew & Orbs)
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    document.body.appendChild(progressBar);

    let scrollWrap = document.querySelector('main') || document.body;
    let isScrolling;
    window.addEventListener('scroll', () => {
        let scrollY = window.scrollY;
        
        // Progress bar
        let dh = document.documentElement.scrollHeight - window.innerHeight;
        if(dh > 0) progressBar.style.transform = `scaleX(${scrollY / dh})`;

        // Removed Scroll Skew due to NaN jitter

        // Orbs parallax
        orbs.forEach(orb => {
            orb.el.style.transform = `translateY(${-scrollY * orb.speed}px)`;
        });
    });

    // 4. Staggered Reveal Observer
    const staggerObs = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-revealed');
                staggerObs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal-stagger').forEach((el, i) => {
        el.style.transitionDelay = `${(i%5)*0.1}s`;
        staggerObs.observe(el);
    });

    // 5. Ripple Click
    document.addEventListener('mousedown', function (e) {
        if (!e.target.closest('.card, .btn')) return;
        const target = e.target.closest('.card, .btn');
        if (getComputedStyle(target).position === 'static') target.style.position = 'relative';
        target.style.overflow = 'hidden';
        const ripple = document.createElement('span');
        const rect = target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = e.clientX - rect.left - size/2 + 'px';
        ripple.style.top = e.clientY - rect.top - size/2 + 'px';
        ripple.style.position = 'absolute';
        ripple.style.background = 'rgba(0, 229, 255, 0.4)';
        ripple.style.borderRadius = '50%';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'rippleAnim 0.6s linear';
        ripple.style.pointerEvents = 'none';
        target.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });

});


// ══════════════════════════════════════
//  CINEMATIC PAGE LOADER (runs outside DOMContentLoaded)
// ══════════════════════════════════════
(function() {
    // Don't show on analysis results page (avoid annoying repeat loads)
    if (document.querySelector('.cinematic-loader')) return;

    const loader = document.createElement('div');
    loader.className = 'cinematic-loader';
    loader.innerHTML = `
        <div class="loader-ring"></div>
        <div class="loader-text">Initializing Career Lens</div>
        <div class="loader-bar"><div class="loader-bar-inner"></div></div>
    `;
    document.body.prepend(loader);

    window.addEventListener('load', () => {
        setTimeout(() => {
            loader.classList.add('fade-out');
            setTimeout(() => loader.remove(), 600);
        }, 1600);
    });
})();
