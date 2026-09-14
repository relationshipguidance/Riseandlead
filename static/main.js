/* =========================================================
   RISE&LEAD — interaction layer
   ========================================================= */

(function () {
    "use strict";

    /* ---------- Scroll reveal ---------- */
    const revealTargets = document.querySelectorAll(
        ".hero-grid > *, .trust-strip-inner > *, " +
        ".for-whom-head > *, .profile, " +
        ".methodology-head > *, .step, " +
        ".about-grid > *, .about-signature, " +
        ".assessment-cta-grid > *, .assessment-panel, " +
        ".final-section > .container > *, " +
        ".question-card, .lead-box, .result-card"
    );

    revealTargets.forEach((el, i) => {
        el.classList.add("reveal");
        if (i % 3 === 1) el.classList.add("d1");
        if (i % 3 === 2) el.classList.add("d2");
    });

    const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("in");
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    revealTargets.forEach((el) => io.observe(el));

    /* ---------- Count-up for the hero card counter ---------- */
    const counterNumber = document.querySelector(".card-counter .number");
    if (counterNumber) {
        const raw = counterNumber.textContent.trim();
        const match = raw.match(/^(\d+)(\+?)$/);
        if (match) {
            const target = parseInt(match[1], 10);
            const suffix = match[2] || "";
            counterNumber.textContent = "0" + suffix;

            const countIO = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    const duration = 1600;
                    const start = performance.now();
                    function tick(now) {
                        const t = Math.min((now - start) / duration, 1);
                        const eased = 1 - Math.pow(1 - t, 3);
                        counterNumber.textContent = Math.round(target * eased) + suffix;
                        if (t < 1) requestAnimationFrame(tick);
                    }
                    requestAnimationFrame(tick);
                    countIO.unobserve(counterNumber);
                });
            }, { threshold: 0.4 });
            countIO.observe(counterNumber);
        }
    }

    /* ---------- Nav shadow on scroll ---------- */
    const header = document.querySelector(".site-header");
    if (header) {
        window.addEventListener("scroll", () => {
            const y = window.scrollY;
            header.style.boxShadow = y > 20
                ? "0 1px 0 rgba(17,28,46,.05), 0 14px 32px -22px rgba(17,28,46,.18)"
                : "none";
        }, { passive: true });
    }

    /* ---------- Smooth anchor scroll ---------- */
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
        a.addEventListener("click", (e) => {
            const id = a.getAttribute("href");
            if (id.length < 2) return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            const top = target.getBoundingClientRect().top + window.scrollY - 100;
            window.scrollTo({ top, behavior: "smooth" });
        });
    });

})();
