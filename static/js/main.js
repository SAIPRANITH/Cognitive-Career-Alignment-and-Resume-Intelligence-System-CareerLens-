document.addEventListener('DOMContentLoaded', () => {

    // ══════════════════════════════════════
    //  THEME TOGGLE
    // ══════════════════════════════════════
    const themeToggleBtn = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        htmlElement.setAttribute('data-bs-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let currentTheme = htmlElement.getAttribute('data-theme');
            let targetTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-theme', targetTheme);
            htmlElement.setAttribute('data-bs-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
            updateThemeIcon(targetTheme);
        });
    }
    
    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'light') {
            icon.classList.remove('bi-moon-stars');
            icon.classList.add('bi-sun');
        } else {
            icon.classList.remove('bi-sun');
            icon.classList.add('bi-moon-stars');
        }
    }

    // ══════════════════════════════════════
    //  SIDEBAR TOGGLE
    // ══════════════════════════════════════
    const sidebarToggle = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

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
    //  COUNTER ANIMATION (Animate numbers)
    // ══════════════════════════════════════
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseFloat(el.dataset.target);
                if (isNaN(target)) return;
                const duration = 1500;
                const start = performance.now();
                const isFloat = target % 1 !== 0;
                
                function animate(now) {
                    const elapsed = now - start;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
                    const current = eased * target;
                    el.textContent = isFloat ? current.toFixed(1) : Math.round(current);
                    if (progress < 1) requestAnimationFrame(animate);
                }
                requestAnimationFrame(animate);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.counter[data-target]').forEach(el => {
        counterObserver.observe(el);
    });

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

    // Add ripple keyframes dynamically
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `@keyframes rippleAnim { to { transform: scale(4); opacity: 0; } }`;
        document.head.appendChild(style);
    }

});
