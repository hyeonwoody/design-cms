/* Design CMS front end.
 * - Tab switching with lazy data loading.
 * - Palettes tab mirrors the K-Design POC: a palette switcher that applies the six
 *   color tokens as CSS variables instantly, with a live component preview.
 * - Inline token editing (F7): editable only when the user has the permission.
 * - Polling: palettes refetch on an interval so a palette added/published by one
 *   admin shows up for every other user without a manual reload.
 */
(function () {
  "use strict";

  var cfg = window.DESIGN_CMS || {};
  var loaded = {};
  var palettesState = { data: null, activeSlug: null, signature: "" };
  var POLL_MS = 10000;

  var TOKEN_LABELS = {
    "color.background": "Background",
    "color.foreground": "Foreground",
    "color.muted": "Muted",
    "color.card": "Card",
    "color.border": "Border",
    "color.accent": "Accent"
  };

  function patch(url, body) {
    return fetch(url, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", "X-CSRFToken": cfg.csrfToken },
      credentials: "same-origin",
      body: JSON.stringify(body)
    });
  }

  function tokenMap(palette) {
    var map = {};
    (palette.tokens || []).forEach(function (t) { map[t.key] = t.value; });
    return map;
  }

  function applyTheme(preview, palette) {
    var map = tokenMap(palette);
    Object.keys(TOKEN_LABELS).forEach(function (key) {
      var cssVar = "--" + key.replace(".", "-");
      if (map[key]) { preview.style.setProperty(cssVar, map[key]); }
    });
  }

  function renderPalettes(body) {
    var data = palettesState.data || [];
    if (!data.length) { body.innerHTML = "<p>No palettes yet.</p>"; return; }
    if (!palettesState.activeSlug ||
        !data.some(function (p) { return p.slug === palettesState.activeSlug; })) {
      palettesState.activeSlug = data[0].slug;
    }

    body.innerHTML = "";

    var switcher = document.createElement("div");
    switcher.className = "palette-switcher";
    data.forEach(function (palette) {
      var btn = document.createElement("button");
      btn.className = "palette-chip" +
        (palette.slug === palettesState.activeSlug ? " active" : "");
      btn.textContent = palette.name + (palette.is_published ? "" : " (draft)");
      btn.addEventListener("click", function () {
        palettesState.activeSlug = palette.slug;
        renderPalettes(body);
      });
      switcher.appendChild(btn);
    });
    body.appendChild(switcher);

    var active = data.filter(function (p) {
      return p.slug === palettesState.activeSlug;
    })[0];

    var preview = document.createElement("div");
    preview.className = "palette-preview";
    applyTheme(preview, active);
    preview.innerHTML =
      '<div class="pp-card"><span class="pp-title">' + active.name + '</span>' +
      '<p class="pp-muted">Live token preview</p>' +
      '<button class="pp-accent">Accent</button></div>';
    body.appendChild(preview);

    var table = document.createElement("table");
    table.className = "token-table";
    var map = tokenMap(active);
    Object.keys(TOKEN_LABELS).forEach(function (key) {
      var token = (active.tokens || []).filter(function (t) { return t.key === key; })[0];
      var tr = document.createElement("tr");
      var swatch = '<span class="swatch" style="background:' + (map[key] || "#000") + '"></span>';
      tr.innerHTML = "<td>" + swatch + TOKEN_LABELS[key] + "</td>";
      var valCell = document.createElement("td");
      if (cfg.canEditTokens && token) {
        var input = document.createElement("input");
        input.value = token.value;
        input.dataset.tokenId = token.id;
        input.addEventListener("change", function () {
          patch("/api/tokens/" + token.id + "/", { value: input.value }).then(function (r) {
            input.classList.toggle("saved", r.ok);
            if (r.ok) { token.value = input.value; applyTheme(preview, active); }
          });
        });
        valCell.appendChild(input);
      } else {
        valCell.textContent = map[key] || "-";
      }
      tr.appendChild(valCell);
      table.appendChild(tr);
    });
    body.appendChild(table);
  }

  function panelHasFocus(body) {
    return body.contains(document.activeElement) &&
      document.activeElement.tagName === "INPUT";
  }

  function loadPalettes(body, isPoll) {
    return fetch("/api/palettes/", { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var results = data.results || data;
        var signature = JSON.stringify(results);
        if (isPoll && (signature === palettesState.signature || panelHasFocus(body))) {
          return; // nothing changed, or user is mid-edit: do not clobber
        }
        palettesState.data = results;
        palettesState.signature = signature;
        renderPalettes(body);
      })
      .catch(function () { if (!isPoll) { body.innerHTML = "<p>Could not load palettes.</p>"; } });
  }

  function renderList(body, data) {
    body.innerHTML = data.length
      ? "<pre>" + JSON.stringify(data, null, 2) + "</pre>"
      : "<p>No entries yet.</p>";
  }

  function renderFigma(body) {
    body.innerHTML = "";
    if (!cfg.canEditPalettes) {
      body.innerHTML = "<p>You need palette edit permission to import from Figma.</p>";
      return;
    }
    var button = document.createElement("button");
    button.textContent = "Import tokens from Figma";
    var status = document.createElement("p");
    button.addEventListener("click", function () {
      status.textContent = "Importing...";
      fetch("/api/figma/import/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": cfg.csrfToken },
        credentials: "same-origin",
        body: "{}"
      }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
        .then(function (res) {
          status.textContent = res.ok
            ? "Imported " + res.d.palettes + " palette(s), " + res.d.tokens + " token(s)."
            : (res.d.detail || "Import failed.");
        });
    });
    body.appendChild(button);
    body.appendChild(status);
  }

  function loadPanel(panel) {
    var slug = panel.dataset.slug;
    var body = panel.querySelector(".tab-body");
    if (loaded[slug]) { return; }
    loaded[slug] = true;

    if (slug === "palettes") {
      loadPalettes(body, false);
      setInterval(function () { loadPalettes(body, true); }, POLL_MS);
      return;
    }
    if (slug === "figma-import") { renderFigma(body); return; }

    fetch(panel.dataset.endpoint, { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (data) { renderList(body, data.results || data); })
      .catch(function () { body.innerHTML = "<p>Could not load data.</p>"; });
  }

  function activate(slug) {
    document.querySelectorAll(".tab-panel").forEach(function (panel) {
      var on = panel.dataset.slug === slug;
      panel.hidden = !on;
      if (on) { loadPanel(panel); }
    });
    document.querySelectorAll(".tab").forEach(function (tab) {
      tab.classList.toggle("active", tab.dataset.tab === slug);
    });
  }

  document.querySelectorAll(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () { activate(tab.dataset.tab); });
  });

  var first = document.querySelector(".tab");
  if (first) { activate(first.dataset.tab); }
})();
