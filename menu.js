document.addEventListener("click", (e) => {
  const menu = document.querySelector(".site-menu");
  const toggle = document.querySelector(".menu-toggle");

  if (!menu || !toggle) return;

  if (toggle.contains(e.target)) {
    menu.classList.toggle("open");
    toggle.setAttribute(
      "aria-expanded",
      menu.classList.contains("open")
    );
  } else if (!menu.contains(e.target)) {
    menu.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }
});
