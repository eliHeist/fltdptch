import './style.css'
import Alpine from "alpinejs";
import mask from "@alpinejs/mask"
import collapse from "@alpinejs/collapse"
import 'htmx.org';
import "htmx-ext-response-targets";


Alpine.plugin(mask)
Alpine.plugin(collapse)

Alpine.start()

// handle HTMX requests that swap content with Alpine.js
document.addEventListener('htmx:afterSwap', (event: any) => {
    const xDataElements = event.detail.target.querySelectorAll('[x-data]');
    xDataElements.forEach((element: any) => {
        // If Alpine was already initialized on this element, destroy the existing instance
        if (element.__x) {
            element.__x.cleanups.forEach((cleanup: any) => cleanup()); // Cleanup existing Alpine instance
            delete element.__x; // Remove Alpine's reference
        }
        // Re-initialize Alpine
        Alpine.initTree(element);
    });
    // re-run nav-highlighting after HTMX swaps in case nav links changed
    try {
        highlightNavLinks();
    } catch (err) {
        // ignore if highlight function not available
    }
});

// Highlight current nav link by matching data-navlink to current pathname
function normalizePath(p: string) {
    if (!p) return '/';
    try {
        // If passed a full URL, extract pathname
        const u = new URL(p, window.location.origin);
        p = u.pathname;
    } catch (e) {
        // ignore
    }
    if (p.length > 1 && p.endsWith('/')) return p.slice(0, -1);
    return p;
}

export function highlightNavLinks() {
    const current = normalizePath(window.location.pathname + window.location.search);
    const links = document.querySelectorAll<HTMLElement>('.navlink');
    links.forEach((el) => {
        const attr = el.getAttribute('href') || '';
        const linkPath = normalizePath(attr);
        if (linkPath === current || (linkPath !== '/' && current.startsWith(linkPath))) {
            el.classList.add('bg-muted');
            el.setAttribute('aria-current', 'page');
        } else {
            el.classList.remove('bg-muted');
            el.removeAttribute('aria-current');
        }
    });
}

// Run on initial load
document.addEventListener('DOMContentLoaded', () => {
    try { highlightNavLinks(); } catch (e) { }
});

