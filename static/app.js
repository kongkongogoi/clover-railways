document.addEventListener("DOMContentLoaded", () => {
  const today = new Date().toISOString().split("T")[0];
  document.querySelectorAll('input[type="date"]').forEach(el => {
    if (!el.min) el.min = today;
  });

  // Add drifting clover and star particles to the first page only.
  const particleHost = document.querySelector(".magic-particles");
  if (particleHost) {
    ["✥", "✦", "♣", "✧", "✥", "✦", "♣", "✧", "✥"].forEach((symbol, index) => {
      const particle = document.createElement("span");
      particle.textContent = symbol;
      particle.style.left = `${5 + ((index * 13) % 91)}%`;
      particle.style.animationDelay = `${-index * 1.7}s`;
      particleHost.appendChild(particle);
    });
  }

  // Play the train transition before navigating between local pages.
  const transition = document.querySelector(".page-transition");
  if (transition && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#") || link.target === "_blank" || link.hasAttribute("download")) return;
      const destination = new URL(link.href, window.location.href);
      if (destination.origin !== window.location.origin || destination.pathname === window.location.pathname && destination.search === window.location.search) return;
      link.addEventListener("click", event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
        event.preventDefault();
        transition.classList.add("active");
        window.setTimeout(() => { window.location.href = destination.href; }, 720);
      });
    });
  }
});
