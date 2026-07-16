(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  var path = window.location.pathname.replace(/\/index\.html$/, "").replace(/\/$/, "");
  document.querySelectorAll(".main-nav a[data-nav]").forEach(function (a) {
    var target = a.getAttribute("data-nav");
    if (path.endsWith(target) || (target === "home" && /document-center\/?$/.test(path))) {
      a.classList.add("active");
    }
  });
})();
