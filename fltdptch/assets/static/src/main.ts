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
document.addEventListener('htmx:afterSwap', (event:any) => {
    const xDataElements = event.detail.target.querySelectorAll('[x-data]');
    xDataElements.forEach((element:any) => {
        // If Alpine was already initialized on this element, destroy the existing instance
        if (element.__x) {
            element.__x.cleanups.forEach((cleanup:any) => cleanup()); // Cleanup existing Alpine instance
            delete element.__x; // Remove Alpine's reference
        }
        // Re-initialize Alpine
        Alpine.initTree(element);
    });
});

