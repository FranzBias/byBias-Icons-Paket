# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet) [![GitLab mirror](https://img.shields.io/badge/mirror-GitLab-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/FranzBias/byBias-Icons-Paket)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![byBias-Icons-Packet icon](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

**A unified GTK app for managing a personal icon collection on Linux Mint / Cinnamon.**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 A moment of honesty

> Over the past few months I've been going through a rough patch: too few
> jobs, and the few there are pay too little. If things don't turn around
> soon, I'll need to look for work elsewhere — nothing wrong with that, but
> I'd much rather keep building projects like this one.
>
> If **byBias-Icons-Packet** is useful to you and you'd like to support it,
> a donation — even just one euro — makes a real difference if enough
> people chip in. And if you can't donate, simply **spreading the word**
> helps just as much. Thank you, sincerely, for reading this far. 🙏

---

**byBias-Icons-Packet** gathers the whole byBias icon toolkit into a single
GTK3 app, built to manage *your own* icon collection: extract, clean up,
name consistently and turn it into a theme. A free icon theme made with it
(GPL-3) is on its way. The main window is a
dashboard: every action is a visible card, and clicking one opens its panel
in the same window — no digging through menus, no memorising commands.

## Actions

The **Main flow** covers the everyday work of building and maintaining an
icon theme, start to finish:

- **Extract icons** — pulls the icons out of `.ico`, `.exe`, `.dll`, `.icl`
  files (even ones renamed to look like something else), rebuilding clean
  PNGs with transparency preserved. Handy when you've downloaded an icon
  pack that's really just a Windows executable in disguise.
- **Create / update theme** — copies a source folder into a proper icon
  theme: cleans up file and folder names (spaces/underscores → hyphen,
  accents stripped), generates a correct `index.theme` and rebuilds the
  icon cache, and can activate the theme system-wide in one click.
- **Apply icon** — a picker organised in *your own* categories (not the
  generic system ones) lets you browse the collection visually and apply
  any icon to a folder.
- **Symbolic icons** — turns a full-colour PNG into a monochrome 16×16 SVG
  "symbolic" icon, the kind used in panels and menus that automatically
  recolour to match light or dark themes.
- **Hunt the giants** — scans for name collisions between your icons and
  system icons; a collision is the classic cause of icons that suddenly
  render giant, or show up as broken-image triangles.
- **Prefix everything** — the safe, hands-off option: adds a `bybias-`
  prefix to every icon in the theme so none of them can ever accidentally
  substitute a system icon.
- **Replace system icons** — pick a system slot (full/empty trash, generic
  folder, home folder, and more) and one of your own images: it's
  installed under the exact standard name, so it takes over everywhere
  that icon appears across the desktop.
- **Right-click in Nemo** — *Change icon…* opens your collection and applies the icon to the selected folder or file; *Paste icon* uses the image in the clipboard. Installed by `install.sh` (press F5 in Nemo to see the new icon).

Beyond the main flow, the dashboard groups more specialised tools into four
sections, each one solving a specific kind of headache:

**Maintenance** — keeping a large collection tidy over time.
- *Find duplicates* compares icons by actual image content (a hash of the
  pixels), not by filename, so it catches the same icon saved twice under
  two different names.
- *Contact sheet* renders the entire collection as a single labelled PNG
  mosaic — a genuinely useful way to actually *see* what you have instead
  of clicking through folders one by one.
- *Find similar* takes one reference icon and ranks the rest of the
  collection by how close their dominant colour is, useful for building a
  visually coherent subset.

**Production** — shaping icons for actual use.
- *Normalize sizes* takes one oversized source PNG and generates the full
  standard set (16 through 256 px), properly resized rather than left for
  the system to scale badly on the fly.
- *Recolor / invert* applies a chosen tint to monochrome icons, or flips
  light and dark, so a symbolic set can be adapted to the opposite theme.
- *Trim & center* removes uneven transparent margins and re-centers the
  icon with consistent padding — the fix for a mixed set that looks
  slightly "off" for no obvious reason.

**Distribution** — sharing what you've built.
- *Export package* zips up the theme together with an auto-generated
  `LICENSE` and `README`, ready to publish.
- *Make showcase* builds a promotional image from a selection of icons,
  the kind you'd want on a download page.

**Safety & convenience** — the safety net.
- *Backup / restore* takes a timestamped snapshot of the theme before a
  risky change, with a one-click way back if something goes wrong.
- *Health-check* runs the whole theme through a diagnostic checklist
  (inheritance, accented names, collisions, cache validity) and flags
  problems *before* they turn into giant icons or broken-image triangles.

A menu at the top-left of the window (☰) gives quick access to **About**
(including the GitHub link), a **language switcher** covering all 10
languages of this README, and a **light/dark theme** toggle for the app
itself.

## Requirements

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils python3-icoextract
```

On first run, if any dependency is missing, byBias-Icons-Packet detects it,
lists exactly what's needed, asks for your explicit consent, and installs
it through the system's own graphical authentication (pkexec) or sudo — so
you can also just launch it and let it set itself up. Your password is
always handled by the system, never by the app itself.

## Run

```bash
python3 icons-packet
```

**Structure** — `icons_packet_core.py` holds all the logic (GTK-free and
independently testable); `icons_packet_gui.py` is the GTK3 dashboard;
`icons-packet` is the launcher, which also handles the dependency
check above.

**Naming convention** — file and folder names use hyphens only (`-`),
never spaces or underscores; the app converts both automatically whenever
it touches a theme.

## 🌱 To err is human

This project was built fast, by one person, in their spare time — so it's
entirely possible it still has rough edges: a bug, an odd behaviour, a
mistranslated string, an imprecise sentence in this very README. If you
spot anything at all, please open an issue — bug reports,
language corrections, and general imprecisions are all genuinely welcome.
The same goes for **feature requests**: if there's something you wish the
app did, or did differently, say so. Suggestions shape where this goes
next.

---

*Made with ❤️ by FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
