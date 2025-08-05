document.addEventListener('DOMContentLoaded', function() {
    // Use data attributes for better isolation
    const burgerToggle = document.querySelector('[data-burger-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    const mobileOverlay = document.querySelector('[data-mobile-overlay]');
    const mobileClose = document.querySelector('[data-mobile-close]');
    const searchModal = document.querySelector('[data-search-modal]');
    const searchTriggers = document.querySelectorAll('[data-search-trigger]');
    const searchClose = document.querySelector('[data-search-close]');
    const searchInput = document.querySelector('[data-search-input]');
    const searchClear = document.querySelector('[data-search-clear]');
    const languageItems = document.querySelectorAll('.dresscode-language-item');
    const mobileLangBtns = document.querySelectorAll('.dresscode-mobile-lang-btn');
    const currentLang = document.querySelector('.dresscode-current-lang');

    // Check if elements exist before adding event listeners
    if (!burgerToggle || !mobileMenu || !searchModal) {
        console.warn('DressCode Header: Required elements not found');
        return;
    }

    // Mobile menu toggle
    function toggleMobileMenu() {
        const isActive = mobileMenu.classList.contains('active');

        if (isActive) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    function openMobileMenu() {
        mobileMenu.classList.add('active');
        if (mobileOverlay) mobileOverlay.classList.add('active');
        burgerToggle.classList.add('active');

        // Store original overflow value
        const originalOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';
        document.body.setAttribute('data-dresscode-original-overflow', originalOverflow);
    }

    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        if (mobileOverlay) mobileOverlay.classList.remove('active');
        burgerToggle.classList.remove('active');

        // Restore original overflow
        const originalOverflow = document.body.getAttribute('data-dresscode-original-overflow') || '';
        document.body.style.overflow = originalOverflow;
        document.body.removeAttribute('data-dresscode-original-overflow');
    }

    // Search modal
    function openSearchModal() {
        searchModal.classList.add('active');

        // Store original overflow value
        const originalOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';
        document.body.setAttribute('data-dresscode-search-overflow', originalOverflow);

        setTimeout(() => {
            if (searchInput) searchInput.focus();
        }, 300);
    }

    function closeSearchModal() {
        searchModal.classList.remove('active');

        // Restore original overflow
        const originalOverflow = document.body.getAttribute('data-dresscode-search-overflow') || '';
        document.body.style.overflow = originalOverflow;
        document.body.removeAttribute('data-dresscode-search-overflow');

        if (searchInput) {
            searchInput.value = '';
            if (searchClear) searchClear.classList.remove('visible');
        }
    }

    // Language selection
    function changeLanguage(langCode) {
        if (currentLang) currentLang.textContent = langCode;

        // Update active states
        languageItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.lang === langCode) {
                item.classList.add('active');
            }
        });

        mobileLangBtns.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.lang === langCode) {
                btn.classList.add('active');
            }
        });

        console.log('DressCode: Language changed to:', langCode);
    }

    // Event listeners with null checks
    if (burgerToggle) {
        burgerToggle.addEventListener('click', toggleMobileMenu);
    }

    if (mobileClose) {
        mobileClose.addEventListener('click', closeMobileMenu);
    }

    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeMobileMenu);
    }

    // Search triggers
    searchTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            openSearchModal();
            closeMobileMenu(); // Close mobile menu if open
        });
    });

    if (searchClose) {
        searchClose.addEventListener('click', closeSearchModal);
    }

    if (searchModal) {
        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) {
                closeSearchModal();
            }
        });
    }

    // Search input
    if (searchInput && searchClear) {
        searchInput.addEventListener('input', (e) => {
            if (e.target.value.length > 0) {
                searchClear.classList.add('visible');
            } else {
                searchClear.classList.remove('visible');
            }
        });

        searchClear.addEventListener('click', () => {
            searchInput.value = '';
            searchClear.classList.remove('visible');
            searchInput.focus();
        });
    }

    // Language selection
    languageItems.forEach(item => {
        item.addEventListener('click', () => {
            changeLanguage(item.dataset.lang);
        });
    });

    mobileLangBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            changeLanguage(btn.dataset.lang);
        });
    });

    // Close mobile menu when clicking on nav links
    const mobileNavLinks = document.querySelectorAll('.dresscode-mobile-nav-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (!link.classList.contains('dresscode-search-trigger')) {
                closeMobileMenu();
            }
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (searchModal && searchModal.classList.contains('active')) {
                closeSearchModal();
            } else if (mobileMenu && mobileMenu.classList.contains('active')) {
                closeMobileMenu();
            }
        }
    });

    // Handle search suggestions
    const suggestionItems = document.querySelectorAll('.dresscode-suggestion-item');
    suggestionItems.forEach(item => {
        item.addEventListener('click', () => {
            if (searchInput && searchClear) {
                searchInput.value = item.textContent.replace('Popular: ', '');
                searchClear.classList.add('visible');
            }
            console.log('DressCode: Search for:', item.textContent);
        });
    });

    // Prevent body scroll when modals are open
    function preventBodyScroll() {
        const scrollY = window.scrollY;
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollY}px`;
        document.body.style.width = '100%';
    }

    function restoreBodyScroll() {
        const scrollY = document.body.style.top;
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, parseInt(scrollY || '0') * -1);
    }

    // Add loading states for buttons
    const authButtons = document.querySelectorAll('.dresscode-btn');
    authButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const link = btn.closest('a');
            if (link && link.getAttribute('href') && link.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                btn.style.opacity = '0.7';
                btn.style.transform = 'scale(0.95)';

                setTimeout(() => {
                    btn.style.opacity = '';
                    btn.style.transform = '';
                    console.log('DressCode: Navigate to:', link.getAttribute('href'));
                }, 200);
            }
        });
    });
});