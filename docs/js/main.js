// ==================== Theme Toggle ====================
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

// Load saved theme or default to light
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);

themeToggle?.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// ==================== Table of Contents ====================
function initTableOfContents() {
    const tocList = document.querySelector('.toc-list');
    if (!tocList) return;
    
    const headings = document.querySelectorAll('.doc-content h2, .doc-content h3');
    
    headings.forEach(heading => {
        const id = heading.textContent.toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-');
        heading.id = id;
        
        const li = document.createElement('li');
        li.className = 'toc-item';
        
        const link = document.createElement('a');
        link.href = `#${id}`;
        link.className = 'toc-link';
        link.textContent = heading.textContent;
        
        if (heading.tagName === 'H3') {
            link.style.paddingLeft = '24px';
            link.style.fontSize = '13px';
        }
        
        li.appendChild(link);
        tocList.appendChild(li);
    });
    
    // Highlight active section
    highlightActiveSection();
    window.addEventListener('scroll', highlightActiveSection);
}

function highlightActiveSection() {
    const tocLinks = document.querySelectorAll('.toc-link');
    const headings = document.querySelectorAll('.doc-content h2, .doc-content h3');
    
    let activeId = '';
    
    headings.forEach(heading => {
        const rect = heading.getBoundingClientRect();
        if (rect.top <= 100 && rect.top >= -rect.height) {
            activeId = heading.id;
        }
    });
    
    tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${activeId}`) {
            link.classList.add('active');
        }
    });
}

// ==================== Smooth Scrolling ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==================== Initialize ====================
document.addEventListener('DOMContentLoaded', () => {
    initTableOfContents();
});