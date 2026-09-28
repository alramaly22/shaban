document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("mobileMenu");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var isOpen = menu.classList.toggle("is-open");
      toggle.classList.toggle("is-open", isOpen);
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.remove("is-open");
        toggle.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Single orchestrated hero reveal on page load
  var hero = document.querySelector(".hero__inner");
  if (hero && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    hero.style.opacity = "0";
    hero.style.transform = "translateY(14px)";
    hero.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        hero.style.opacity = "1";
        hero.style.transform = "translateY(0)";
      });
    });
  }

  // Payment method panel: dim the card fields unless "Card Payment" is selected
  var cardPanel = document.getElementById("cardPanel");
  var methodInputs = document.querySelectorAll('input[name="payment_method"]');
  if (cardPanel && methodInputs.length) {
    var syncCardPanel = function () {
      var selected = document.querySelector('input[name="payment_method"]:checked');
      cardPanel.style.display = selected && selected.value === "CARD" ? "block" : "none";
    };
    methodInputs.forEach(function (input) {
      input.addEventListener("change", syncCardPanel);
    });
    syncCardPanel();
  }

  // Before / after comparison slider on the featured transformation.
  // Vanilla JS, no dependencies. Does nothing if the slider isn't present
  // (e.g. before real transformation photos have been uploaded).
  var slider = document.querySelector("[data-ba-slider]");
  if (slider) {
    var handle = slider.querySelector("[data-ba-handle]");
    var beforeImg = slider.querySelector(".ba-slider__before");
    var dragging = false;

    var setPosition = function (percent) {
      percent = Math.max(0, Math.min(100, percent));
      beforeImg.style.clipPath = "inset(0 " + (100 - percent) + "% 0 0)";
      handle.style.left = percent + "%";
    };

    var positionFromEvent = function (clientX) {
      var rect = slider.getBoundingClientRect();
      var percent = ((clientX - rect.left) / rect.width) * 100;
      setPosition(percent);
    };

    var onMove = function (e) {
      if (!dragging) return;
      var clientX = e.touches ? e.touches[0].clientX : e.clientX;
      positionFromEvent(clientX);
    };

    var startDrag = function (e) {
      dragging = true;
      onMove(e);
    };
    var stopDrag = function () { dragging = false; };

    handle.addEventListener("mousedown", startDrag);
    slider.addEventListener("mousedown", startDrag);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", stopDrag);

    slider.addEventListener("touchstart", startDrag, { passive: true });
    window.addEventListener("touchmove", onMove, { passive: true });
    window.addEventListener("touchend", stopDrag);

    setPosition(50);
  }
});
