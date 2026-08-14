/**
 * Click-to-zoom for images in the docs content.
 *
 * Opens a full-screen viewer where the image can be zoomed with the wheel,
 * a pinch gesture, the toolbar buttons or a double click, and panned by
 * dragging. Escape, the close button or a click on the backdrop closes it.
 */
(function () {
  "use strict";

  var MIN_SCALE = 1;
  var MAX_SCALE = 8;
  var CONTENT = ".sl-markdown-content";

  var overlay = null;
  var stage = null;
  var image = null;
  var scale = 1;
  var offsetX = 0;
  var offsetY = 0;
  var opener = null;
  var pointers = new Map();
  var pinchStart = 0;
  var pinchScale = 1;
  var dragged = false;

  function isZoomable(img) {
    if (img.closest("a")) return false;
    if (img.classList.contains("no-zoom")) return false;
    if (img.closest(".no-zoom")) return false;
    return true;
  }

  function build() {
    overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Image viewer");
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="lightbox-toolbar">' +
      '<button type="button" class="lightbox-button" data-action="out" aria-label="Zoom out">&minus;</button>' +
      '<button type="button" class="lightbox-button" data-action="reset" aria-label="Reset zoom">100%</button>' +
      '<button type="button" class="lightbox-button" data-action="in" aria-label="Zoom in">+</button>' +
      '<button type="button" class="lightbox-button" data-action="close" aria-label="Close image viewer">&times;</button>' +
      "</div>" +
      '<div class="lightbox-stage"><img class="lightbox-image" alt="" /></div>';

    stage = overlay.querySelector(".lightbox-stage");
    image = overlay.querySelector(".lightbox-image");

    overlay.addEventListener("click", onOverlayClick);
    stage.addEventListener("wheel", onWheel, { passive: false });
    stage.addEventListener("dblclick", onDoubleClick);
    stage.addEventListener("pointerdown", onPointerDown);
    stage.addEventListener("pointermove", onPointerMove);
    stage.addEventListener("pointerup", onPointerUp);
    stage.addEventListener("pointercancel", onPointerUp);

    document.body.appendChild(overlay);
  }

  function apply() {
    image.style.transform =
      "translate(" + offsetX + "px, " + offsetY + "px) scale(" + scale + ")";
    stage.dataset.zoomed = scale > 1 ? "true" : "false";
  }

  function setScale(next, originX, originY) {
    next = Math.min(MAX_SCALE, Math.max(MIN_SCALE, next));
    var rect = stage.getBoundingClientRect();
    var cx = (originX === undefined ? rect.width / 2 : originX - rect.left) - rect.width / 2;
    var cy = (originY === undefined ? rect.height / 2 : originY - rect.top) - rect.height / 2;
    var ratio = next / scale;

    offsetX = cx - (cx - offsetX) * ratio;
    offsetY = cy - (cy - offsetY) * ratio;
    scale = next;
    if (scale === MIN_SCALE) {
      offsetX = 0;
      offsetY = 0;
    }
    apply();
  }

  function open(img) {
    if (!overlay) build();
    opener = img;
    scale = 1;
    offsetX = 0;
    offsetY = 0;
    image.src = img.currentSrc || img.src;
    image.alt = img.alt || "";
    apply();
    overlay.hidden = false;
    document.documentElement.classList.add("lightbox-open");
    document.addEventListener("keydown", onKeyDown, true);
    overlay.querySelector('[data-action="close"]').focus();
  }

  function close() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    image.removeAttribute("src");
    pointers.clear();
    document.documentElement.classList.remove("lightbox-open");
    document.removeEventListener("keydown", onKeyDown, true);
    if (opener) {
      opener.focus({ preventScroll: true });
      opener = null;
    }
  }

  function onOverlayClick(event) {
    var button = event.target.closest("[data-action]");
    if (button) {
      var action = button.dataset.action;
      if (action === "close") close();
      else if (action === "in") setScale(scale * 1.5);
      else if (action === "out") setScale(scale / 1.5);
      else setScale(1);
      return;
    }
    if (dragged) {
      dragged = false;
      return;
    }
    if (event.target === image) return;
    close();
  }

  function onKeyDown(event) {
    if (event.key === "Escape") {
      event.preventDefault();
      close();
    } else if (event.key === "+" || event.key === "=") {
      setScale(scale * 1.5);
    } else if (event.key === "-") {
      setScale(scale / 1.5);
    } else if (event.key === "0") {
      setScale(1);
    } else if (event.key === "Tab") {
      // Keep focus inside the viewer.
      var buttons = overlay.querySelectorAll(".lightbox-button");
      var first = buttons[0];
      var last = buttons[buttons.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }

  function onWheel(event) {
    event.preventDefault();
    var factor = Math.exp(-event.deltaY / 400);
    setScale(scale * factor, event.clientX, event.clientY);
  }

  function onDoubleClick(event) {
    event.preventDefault();
    setScale(scale > 1 ? 1 : 2.5, event.clientX, event.clientY);
  }

  function distance() {
    var points = Array.from(pointers.values());
    return Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y);
  }

  function onPointerDown(event) {
    if (event.target.closest("[data-action]")) return;
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    dragged = false;
    if (pointers.size === 2) {
      pinchStart = distance();
      pinchScale = scale;
    }
    stage.setPointerCapture(event.pointerId);
  }

  function onPointerMove(event) {
    var previous = pointers.get(event.pointerId);
    if (!previous) return;
    var current = { x: event.clientX, y: event.clientY };
    pointers.set(event.pointerId, current);

    if (pointers.size === 2 && pinchStart > 0) {
      var points = Array.from(pointers.values());
      setScale(
        (pinchScale * distance()) / pinchStart,
        (points[0].x + points[1].x) / 2,
        (points[0].y + points[1].y) / 2,
      );
      dragged = true;
      return;
    }

    if (scale <= 1) return;
    event.preventDefault();
    offsetX += current.x - previous.x;
    offsetY += current.y - previous.y;
    if (Math.abs(current.x - previous.x) + Math.abs(current.y - previous.y) > 2) {
      dragged = true;
    }
    apply();
  }

  function onPointerUp(event) {
    pointers.delete(event.pointerId);
    if (pointers.size < 2) pinchStart = 0;
    if (stage.hasPointerCapture(event.pointerId)) {
      stage.releasePointerCapture(event.pointerId);
    }
  }

  function prepare() {
    var images = document.querySelectorAll(CONTENT + " img");
    images.forEach(function (img) {
      if (img.dataset.zoomable || !isZoomable(img)) return;
      img.dataset.zoomable = "true";
      img.tabIndex = 0;
      img.setAttribute("role", "button");
      img.setAttribute("title", "Click to enlarge");
      img.addEventListener("click", function () {
        open(img);
      });
      img.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          open(img);
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", prepare);
  } else {
    prepare();
  }
  // Re-run after client-side navigation, if it is ever enabled.
  document.addEventListener("astro:page-load", prepare);
})();
