// ==================== Search Functionality ====================
const searchInput = document.getElementById('search-input');

// Search index with relative URLs from root
const searchIndex = [
    { title: 'Home', url: 'index.html', keywords: 'home maticlib welcome' },
    { title: 'Getting Started', url: 'pages/getstarted/sample.html', keywords: 'start quick example tutorial' },
    { title: 'Installation', url: 'pages/getstarted/installation.html', keywords: 'install pip setup requirements' },
    { title: 'Google GenAI Client', url: 'pages/docs/llm/clients/google-genai.html', keywords: 'gemini google llm api client' },
    { title: 'Mistral Client', url: 'pages/docs/llm/clients/mistral.html', keywords: 'mistral llm api client' },
    { title: 'MaticGraph', url: 'pages/docs/graph/maticgraph.html', keywords: 'graph workflow state agent parallel' },
    { title: 'Messages', url: 'pages/docs/messages.html', keywords: 'message system human ai conversation' }
];

// Dynamically detect the base URL for the site
function getSiteBaseUrl() {
    const currentUrl = window.location.href;
    const currentPath = window.location.pathname;
    
    // Find the root of the site by looking for index.html or the base directory
    let baseUrl;
    
    if (currentPath.includes('index.html')) {
        // We're on index.html, extract everything before it
        baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('index.html'));
    } else if (currentPath.endsWith('/')) {
        // We're on a directory index
        // Go up directories until we find the root
        const pathSegments = currentPath.split('/').filter(segment => segment);
        const urlBase = window.location.origin;
        
        // Count how many levels deep we are by checking for known directories
        if (currentPath.includes('/pages/')) {
            const beforePages = currentPath.substring(0, currentPath.indexOf('/pages/'));
            baseUrl = urlBase + beforePages + '/';
        } else {
            baseUrl = urlBase + '/';
        }
    } else {
        // We're on a specific HTML file
        // Navigate up to find the root
        const pathParts = currentPath.split('/').filter(p => p);
        
        // Remove the filename
        pathParts.pop();
        
        // Check if we're in pages directory
        if (currentPath.includes('/pages/')) {
            const pagesIndex = pathParts.indexOf('pages');
            if (pagesIndex !== -1) {
                // Go back to before 'pages' directory
                pathParts.splice(pagesIndex);
            }
        }
        
        baseUrl = window.location.origin + '/' + pathParts.join('/') + '/';
        
        // Handle the root case
        if (!currentPath.includes('/pages/')) {
            baseUrl = window.location.origin + currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        }
    }
    
    return baseUrl;
}

// More robust base path calculation
function getBasePath() {
    const currentPath = window.location.pathname;
    
    // Handle different scenarios
    // 1. If we're at the root (index.html or /)
    if (currentPath === '/' || currentPath.endsWith('/index.html') || !currentPath.includes('/')) {
        return '';
    }
    
    // 2. If we're in a subdirectory
    // Count how many levels deep we are from root
    const pathWithoutFile = currentPath.substring(0, currentPath.lastIndexOf('/'));
    const segments = pathWithoutFile.split('/').filter(s => s.length > 0);
    
    // Find if 'pages' is in the path and count from there
    const pagesIndex = segments.indexOf('pages');
    if (pagesIndex !== -1) {
        // We're inside pages directory
        const depthFromPages = segments.length - pagesIndex;
        return '../'.repeat(depthFromPages);
    }
    
    // If no 'pages' found, count total depth
    return '../'.repeat(segments.length);
}

// Universal URL resolver - works in all environments
function getAbsoluteUrl(relativeUrl) {
    // Create a temporary anchor element to resolve the URL
    const baseUrl = getSiteBaseUrl();
    const fullUrl = new URL(relativeUrl, baseUrl);
    return fullUrl.href;
}

// Convert search result URL to work from current page
function getWorkingUrl(url) {
    // Try to use absolute URL first (works best for web servers)
    if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
        return getAbsoluteUrl(url);
    }
    
    // Fallback to relative path for file:// protocol
    const basePath = getBasePath();
    return basePath + url;
}

// Keyboard shortcut (Ctrl+K or Cmd+K)
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput?.focus();
    }
});

// Search functionality
let searchTimeout;
searchInput?.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.toLowerCase().trim();
    
    if (query.length < 2) {
        hideSearchResults();
        return;
    }
    
    searchTimeout = setTimeout(() => {
        performSearch(query);
    }, 300);
});

function performSearch(query) {
    const results = searchIndex.filter(item => 
        item.title.toLowerCase().includes(query) ||
        item.keywords.toLowerCase().includes(query)
    );
    
    displaySearchResults(results);
}

function displaySearchResults(results) {
    // Remove existing results
    let resultsContainer = document.querySelector('.search-results');
    if (!resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-results';
        searchInput.parentElement.appendChild(resultsContainer);
        
        // Style the results container
        resultsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 8px;
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            max-height: 400px;
            overflow-y: auto;
            z-index: 1000;
        `;
    }
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<div style="padding: 16px; color: var(--text-secondary);">No results found</div>';
    } else {
        resultsContainer.innerHTML = results.map(result => {
            const workingUrl = getWorkingUrl(result.url);
            return `
                <a href="${workingUrl}" class="search-result-item" style="
                    display: block;
                    padding: 12px 16px;
                    color: var(--text-primary);
                    text-decoration: none;
                    border-bottom: 1px solid var(--border-color);
                    transition: background-color 0.2s;
                ">
                    <div style="font-weight: 600; margin-bottom: 4px;">${result.title}</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">${result.url}</div>
                </a>
            `;
        }).join('');
        
        // Add hover effect
        document.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                const target = e.target.closest('.search-result-item');
                if (target) target.style.backgroundColor = 'var(--bg-secondary)';
            });
            item.addEventListener('mouseleave', (e) => {
                const target = e.target.closest('.search-result-item');
                if (target) target.style.backgroundColor = 'transparent';
            });
        });
    }
}

function hideSearchResults() {
    const resultsContainer = document.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.remove();
    }
}

// Close search results when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        hideSearchResults();
    }
});

// Clear search on page navigation
searchInput?.addEventListener('blur', () => {
    setTimeout(hideSearchResults, 200);
});

// Close search results on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        hideSearchResults();
        searchInput?.blur();
    }
});

// Debug function (remove in production)
if (window.location.search.includes('debug')) {
    console.log('Current URL:', window.location.href);
    console.log('Current Path:', window.location.pathname);
    console.log('Site Base URL:', getSiteBaseUrl());
    console.log('Base Path:', getBasePath());
    console.log('Sample resolved URL:', getWorkingUrl('pages/docs/messages.html'));
}