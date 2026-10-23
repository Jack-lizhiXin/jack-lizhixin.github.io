/* Progressive enhancement: the complete content remains readable without JS. */
(() => {
  "use strict";

  const page = document.documentElement;
  const language = document.body.dataset.lang === "en" ? "en" : "zh";
  const publications = [...document.querySelectorAll(".publication[data-year]")];
  const filters = [...document.querySelectorAll(".year-filter[data-year]")];
  const count = document.getElementById("publication-count");

  const updateCount = (visible) => {
    if (!count) return;
    const template = language === "en"
      ? count.dataset.enTemplate || "{n} selected publications"
      : count.dataset.zhTemplate || "显示 {n} 篇代表论文";
    count.textContent = template.replace("{n}", String(visible));
  };

  const applyYear = (year) => {
    let visible = 0;
    publications.forEach((publication) => {
      const publicationYear = Number(publication.dataset.year);
      const matches = year === "all"
        || (year === "earlier" && publicationYear <= 2024)
        || String(publicationYear) === year;
      publication.hidden = !matches;
      if (matches) visible += 1;
    });
    filters.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.year === year));
    });
    updateCount(visible);
  };

  if (publications.length && filters.length) {
    filters.forEach((button) => {
      button.addEventListener("click", () => applyYear(button.dataset.year || "all"));
    });
    applyYear("all");
    page.classList.add("js");
  }

  const links = [...document.querySelectorAll('.site-nav a[href^="#"]')];
  const linkedSections = links.map((link) => {
    const id = decodeURIComponent(link.hash.slice(1));
    return { link, section: document.getElementById(id) };
  }).filter((entry) => entry.section);

  if (!linkedSections.length) return;
  const setCurrent = (id) => {
    linkedSections.forEach(({ link, section }) => {
      if (section.id === id) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };

  let scheduled = false;
  const updateCurrent = () => {
    scheduled = false;
    const header = document.querySelector(".site-header");
    const threshold = (header ? header.getBoundingClientRect().height : 80) + 56;
    let current = linkedSections[0].section.id;
    linkedSections.forEach(({ section }) => {
      if (section.getBoundingClientRect().top <= threshold) current = section.id;
    });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8) {
      current = linkedSections[linkedSections.length - 1].section.id;
    }
    setCurrent(current);
  };
  const scheduleUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateCurrent);
  };

  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate, { passive: true });
  window.addEventListener("hashchange", scheduleUpdate);
  filters.forEach((button) => button.addEventListener("click", scheduleUpdate));
  updateCurrent();
})();
