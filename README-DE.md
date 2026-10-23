# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet) [![GitLab mirror](https://img.shields.io/badge/mirror-GitLab-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/FranzBias/byBias-Icons-Paket)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![byBias-Icons-Packet Icon](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

**Eine einheitliche GTK-App zur Verwaltung einer persönlichen Icon-Sammlung unter Linux Mint / Cinnamon.**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 Ein ehrlicher Moment

> Seit einigen Monaten durchlebe ich eine schwierige Phase: zu wenige
> Aufträge, und die wenigen zahlen zu schlecht. Wenn sich das nicht bald
> ändert, muss ich mir woanders Arbeit suchen — nichts Schlimmes daran,
> aber ich würde viel lieber weiter Projekte wie dieses bauen.
>
> Wenn dir **byBias-Icons-Packet** nützlich ist und du es unterstützen
> möchtest: Eine Spende — und sei es nur ein Euro — macht einen echten
> Unterschied, wenn genug Menschen mitmachen. Und falls du nicht spenden
> kannst, hilft es genauso viel, es **weiterzuerzählen**. Danke von
> Herzen, dass du bis hierhin gelesen hast. 🙏

---

**byBias-Icons-Packet** vereint das gesamte byBias-Icon-Toolkit in einer
einzigen GTK3-App, gemacht für *deine eigene* Icon-Sammlung: extrahieren,
aufräumen, einheitlich benennen und daraus ein Thema machen. Ein freies
Icon-Thema (GPL-3), mit der App erstellt, ist in Arbeit. Das Hauptfenster
ist ein Dashboard: Jede Aktion ist eine sichtbare
Kachel, ein Klick öffnet das zugehörige Panel im selben Fenster — kein
Durchsuchen von Menüs, keine Befehle zum Auswendiglernen.

## Aktionen

Der **Hauptablauf** deckt die tägliche Arbeit beim Aufbau und der Pflege
eines Icon-Themas ab, von Anfang bis Ende:

- **Icons extrahieren** — holt Icons aus `.ico`-, `.exe`-, `.dll`-,
  `.icl`-Dateien (auch umbenannten), erzeugt saubere PNGs mit erhaltener
  Transparenz. Praktisch, wenn ein heruntergeladenes Icon-Paket eigentlich
  eine getarnte Windows-Anwendung ist.
- **Thema erstellen / aktualisieren** — kopiert einen Quellordner in ein
  echtes Icon-Thema: bereinigt Datei- und Ordnernamen (Leerzeichen/
  Unterstriche → Bindestrich, Akzente entfernt), erzeugt eine korrekte
  `index.theme` und baut den Cache neu auf, und kann das Thema mit einem
  Klick systemweit aktivieren.
- **Icon anwenden** — ein nach *deinen eigenen* Kategorien organisierter
  Auswähler lässt dich die Sammlung visuell durchstöbern und jedes Icon
  auf einen Ordner anwenden.
- **Symbolische Icons** — verwandelt ein farbiges PNG in ein monochromes
  16×16-SVG-"Symbol-Icon", wie sie in Panels und Menüs verwendet werden
  und sich automatisch an helle oder dunkle Themen anpassen.
- **Jagd auf die Riesen** — sucht nach Namenskollisionen zwischen deinen
  Icons und System-Icons; eine Kollision ist die klassische Ursache für
  Icons, die plötzlich riesig erscheinen oder als kaputte Bild-Dreiecke
  angezeigt werden.
- **Alles mit Präfix** — die sichere, unbeaufsichtigte Option: fügt jedem
  Icon im Thema ein `bybias-`-Präfix hinzu, sodass keines je versehentlich
  ein System-Icon ersetzen kann.
- **System-Icons ersetzen** — wähle einen Systemplatz (Papierkorb voll/
  leer, allgemeiner Ordner, Home-Ordner und mehr) und eines deiner
  eigenen Bilder: Es wird unter dem exakten Standardnamen installiert und
  übernimmt damit überall auf dem Desktop, wo dieses Icon erscheint.
- **Rechtsklick in Nemo** — *Symbol ändern…* öffnet deine Sammlung und wendet das Symbol auf den gewählten Ordner oder die Datei an; *Symbol einfügen* nimmt das Bild aus der Zwischenablage. Wird von `install.sh` installiert (drücke F5 in Nemo, um das neue Symbol zu sehen).

Über den Hauptablauf hinaus bündelt das Dashboard spezialisiertere
Werkzeuge in vier Bereichen, jeder für eine bestimmte Art von Kopfzerbrechen:

**Wartung** — eine große Sammlung dauerhaft aufgeräumt halten.
- *Duplikate finden* vergleicht Icons anhand des tatsächlichen Bildinhalts
  (ein Hash der Pixel), nicht des Dateinamens, und findet so dasselbe
  Icon, das zweimal unter verschiedenen Namen gespeichert wurde.
- *Kontaktabzug* stellt die gesamte Sammlung als ein einziges beschriftetes
  PNG-Mosaik dar — eine wirklich nützliche Art, tatsächlich zu *sehen*,
  was man hat, statt sich durch Ordner zu klicken.
- *Ähnliche finden* nimmt ein Referenz-Icon und ordnet den Rest der
  Sammlung danach, wie nah ihre dominante Farbe ist — nützlich für den
  Aufbau eines visuell stimmigen Teilsatzes.

**Produktion** — Icons für den tatsächlichen Einsatz formen.
- *Größen normalisieren* nimmt ein übergroßes Quell-PNG und erzeugt den
  vollständigen Standardsatz (16 bis 256 px), korrekt skaliert statt vom
  System schlecht spontan hochgerechnet.
- *Umfärben / invertieren* wendet einen gewählten Farbton auf monochrome
  Icons an oder kehrt hell und dunkel um, sodass ein symbolisches Set an
  das entgegengesetzte Thema angepasst werden kann.
- *Zuschneiden & zentrieren* entfernt ungleichmäßige transparente Ränder
  und zentriert das Icon mit einheitlichem Abstand neu — die Lösung für
  ein gemischtes Set, das ohne offensichtlichen Grund leicht "schief"
  wirkt.

**Verteilung** — teilen, was du gebaut hast.
- *Paket exportieren* packt das Thema zusammen mit automatisch erzeugter
  `LICENSE` und `README`, bereit zur Veröffentlichung.
- *Showcase erstellen* baut ein Werbebild aus einer Auswahl von Icons, wie
  man es auf einer Download-Seite haben möchte.

**Sicherheit & Komfort** — das Sicherheitsnetz.
- *Sicherung / Wiederherstellung* erstellt einen zeitgestempelten Snapshot
  des Themas vor einer riskanten Änderung, mit einem Ein-Klick-Weg zurück,
  falls etwas schiefgeht.
- *Gesundheitscheck* prüft das gesamte Thema anhand einer diagnostischen
  Checkliste (Vererbung, akzentuierte Namen, Kollisionen, Cache-
  Gültigkeit) und meldet Probleme, *bevor* sie zu riesigen Icons oder
  kaputten Bild-Dreiecken werden.

Ein Menü oben links im Fenster (☰) bietet schnellen Zugriff auf **Info**
(inklusive GitHub-Link), einen **Sprachumschalter** für alle 10 Sprachen
dieses READMEs sowie einen **Hell/Dunkel-Thema**-Schalter für die App
selbst.

## Voraussetzungen

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils python3-icoextract
```

Fehlt beim ersten Start eine Abhängigkeit, erkennt byBias-Icons-Packet
dies, listet genau auf, was benötigt wird, bittet um deine ausdrückliche
Zustimmung und installiert es über die grafische Systemauthentifizierung
(pkexec) oder sudo — du kannst die App also auch einfach starten und sie
sich selbst einrichten lassen. Dein Passwort verwaltet immer das System,
nie die App selbst.

## Starten

```bash
python3 icons-packet
```

**Struktur** — `icons_packet_core.py` enthält die gesamte Logik (ohne
GTK, unabhängig testbar); `icons_packet_gui.py` ist das GTK3-Dashboard;
`icons-packet` ist der Launcher, der auch die oben beschriebene
Abhängigkeitsprüfung übernimmt.

**Namenskonvention** — Datei- und Ordnernamen verwenden ausschließlich
Bindestriche (`-`), niemals Leerzeichen oder Unterstriche; die App
wandelt beides automatisch um, sobald sie ein Thema bearbeitet.

## 🌱 Irren ist menschlich

Dieses Projekt wurde schnell, von einer einzelnen Person, in der Freizeit
gebaut — es ist also durchaus möglich, dass es noch Ecken und Kanten hat:
ein Bug, ein merkwürdiges Verhalten, eine falsch übersetzte Zeichenkette,
ein ungenauer Satz in genau diesem README. Wenn dir etwas auffällt, eröffne
bitte ein Issue — Bug-Meldungen, Sprachkorrekturen und
allgemeine Ungenauigkeiten sind allesamt wirklich willkommen. Das Gleiche
gilt für **Funktionswünsche**: Wenn es etwas gibt, das die App tun sollte
oder anders tun sollte, sag es ruhig. Vorschläge bestimmen, wohin sich
dieses Projekt als Nächstes entwickelt.

---

*Mit ❤️ gemacht von FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
