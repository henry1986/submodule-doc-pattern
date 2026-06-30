# Interne Projekt-Dokumentation (Developer Guide)

Diese Dokumentation beschreibt die interne Struktur und Funktionsweise dieser Webseite. Sie dient als Leitfaden für Entwickler, die an diesem Projekt mitarbeiten.

> [!NOTE]
> Dies ist eine **interne Projektdokumentation** und liegt daher direkt im Haupt-Repository unter `/docs/internal/`. Sie unterscheidet sich fundamental von den Dokumentationen, die nach dem **Git Submodule Docs Pattern** ausgelagert werden.

---

## 📂 Verzeichnisstruktur von `/docs`

Um Ordnung im Projekt zu halten, wird der `/docs`-Ordner wie folgt strukturiert:

1. **`docs/internal/` (Diese Dokumentation):**
   * Enthält die interne Dokumentation für Entwickler, die direkt an dieser Anwendung arbeiten (Design-Entscheidungen, Architektur, Setup). Sie wird direkt im Git-Repository versioniert.
2. **`docs/lib-docs/` (Für externe Bibliotheken):**
   * **Reservierter Pfad** für das Submodule-Pattern. Hier werden die Dokumentations-Repositorys von externen Bibliotheken (z. B. `docs/lib-docs/my-library`) als Read-Only Submodule eingebunden und auf die verwendete Version fixiert.
3. **`docs/releases/` (Optional - Nur für eigene Bibliotheks-Releases):**
   * Wird nur benötigt, wenn dieses Projekt selbst eine Bibliothek/Library ist, die von anderen konsumiert wird. In diesem Fall wird hier das eigene Doku-Repository mit Schreibrechten als Submodul eingebunden, um synchrone Dokumentations-Releases zu erstellen. Für reine Endanwender-Apps (Endconsumer Apps) ist dieser Ordner nicht notwendig und entfällt.

---

## 🛠️ Mehrsprachiges Build-System

Die Webseite unterstützt 8 Sprachen. Um den Wartungsaufwand minimal zu halten, wird die Seite über ein Vorlagen-System generiert.

### Die Komponenten:
* **`template.html`:** Das HTML-Grundgerüst. Texte sind durch Platzhalter wie `{{title}}` ersetzt. Enthält auch das Stylesheet, die JavaScript-Logik für Tabs/Simulator und den Sprachwähler.
* **`translations.json`:** Die zentrale Übersetzungsdatenbank. Hier sind alle Text-Schlüssel für alle 8 unterstützten Sprachen hinterlegt.
* **`build.py`:** Ein einfaches Python-Skript. Es liest das Template und die Übersetzungen, fügt die entsprechenden Sprachen ein, generiert die SEO-optimierten `<link rel="alternate" hreflang="...">` Tags und schreibt die fertigen HTML-Dateien:
  * `index.html` (Standard-Sprache: Deutsch)
  * `index_[lang].html` (z. B. `index_en.html`, `index_pl.html`, etc.)

### Lokales Generieren:
Wenn du Texte in `translations.json` oder das Layout in `template.html` änderst, führe lokal folgenden Befehl aus, um die HTML-Dateien neu zu generieren:
```bash
python build.py
```

---

## 💬 Giscus Kommentar-System

Die Kommentarfunktion wird über [Giscus](https://giscus.app) bereitgestellt und nutzt GitHub Discussions.

### Konfiguration:
Im Template ist das Giscus-Skript mit folgenden Repository-IDs konfiguriert:
* **Repo-ID:** `R_kgDOTJUC4g` (henry1986/submodule-doc-pattern)
* **Kategorie-ID:** `DIC_kwDOTJUC4s4DAM6U` (Kategorie: "General")

Das Skript ist so eingestellt, dass es sich automatisch an die geladene Seitensprache anpasst:
```html
data-lang="{{giscus_lang}}"
```
Die Übersetzung von Sprachcodes (z. B. `zh` zu `zh-CN`) wird automatisch vom Build-Skript `build.py` vorgenommen.

---

## 🚀 GitHub Actions Deployment

Bei jedem Push auf den `main`-Branch baut und veröffentlicht eine GitHub Action die Seite vollautomatisch:
* Die Pipeline ist in `.github/workflows/deploy.yml` definiert.
* Sie führt `python build.py` auf dem Runner aus, um sicherzustellen, dass alle Sprachversionen aktuell sind.
* Anschließend lädt sie das Ergebnis als GitHub-Pages-Artefakt hoch und nimmt das Deployment vor.
