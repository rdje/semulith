// Prefer an explicit current chapter to mdBook's root-index alias fallback.
// Run before DOMContentLoaded, when the generated script inserts heading links.
(() => {
    "use strict";
    const sidebar = document.querySelector("#mdbook-sidebar");
    if (!sidebar) return;

    function pageAddress(value) {
        const url = new URL(value, document.baseURI);
        url.hash = "";
        url.search = "";
        if (url.pathname.endsWith("/")) url.pathname += "index.html";
        return url.href.replace(/\.html$/, "");
    }

    const links = [...sidebar.querySelectorAll(".chapter-link-wrapper > a[href]")];
    const current = pageAddress(document.location.href);
    const matches = links.filter(link => pageAddress(link.href) === current);
    // No explicit match means an index alias (or an auxiliary page). Keep it.
    if (matches.length !== 1) return;
    links.forEach(link => {
        link.classList.toggle("active", link === matches[0]);
    });
})();
