#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
icons_packet_core.py — logica pura di Icons-Packet 📦🦉

Nessuna dipendenza da GTK: tutte le operazioni sulle icone e sul tema
vivono qui, così sono testabili e riutilizzabili. La GUI (icons_packet_gui.py)
chiama solo queste funzioni.

by Franz & Aldus
"""

import os
import re
import struct
import subprocess
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------
#  Costanti condivise
# --------------------------------------------------------------------------
ICONS_DIR = Path.home() / ".local/share/icons"
EXTENSIONS = (".png", ".svg", ".xpm")
GREY = "#bebebe"
PREFIX = "bybias-"
PNG_SIG = b"\x89PNG\r\n\x1a\n"

# I 10 Context standard riconosciuti dal selettore di Mint
STANDARD_CONTEXTS = ("Actions", "Applications", "Categories", "Devices",
                     "Emblems", "Emotes", "MimeTypes", "Places", "Status",
                     "Panel")


# --------------------------------------------------------------------------
#  Utilità sui nomi (convenzione: solo trattini)
# --------------------------------------------------------------------------
def to_hyphens(name: str) -> str:
    """Spazi e underscore → trattino singolo. La convenzione della suite."""
    name = name.replace(" ", "-").replace("_", "-")
    name = re.sub(r"-+", "-", name)
    return name.strip("-") or "noname"


def strip_accents(name: str) -> str:
    """Rimuove accenti/caratteri non-ASCII che invalidano la cache GTK."""
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in decomposed
                         if ord(c) < 128 and not unicodedata.combining(c))
    return ascii_name or "noname"


def clean_name(name: str) -> str:
    """Bonifica completa: niente accenti, solo trattini."""
    return to_hyphens(strip_accents(name))


def category_label(folder: str) -> str:
    """'5-EMAIL-e-POSTA' → 'Email e Posta' per la barra laterale."""
    label = re.sub(r"^\d+[-_]*", "", folder)
    label = label.replace("-", " ").replace("_", " ").strip()
    return label.title() if label else folder


def map_context(folder_name: str) -> str:
    """Mappa il nome di una cartella su uno dei 10 Context standard."""
    n = folder_name.upper()
    if any(k in n for k in ("FOLDER", "CARTELLE", "TRASH", "CESTIN",
                            "DESKTOP", "HOME", "DOWNLOAD", "PLACES")):
        return "Places"
    if any(k in n for k in ("ARROW", "FRECCE", "SYMBOL", "SIMBOL",
                            "EMOJI", "EMOTE")):
        return "Emotes"
    if any(k in n for k in ("DOC", "OFFICE", "UFFICIO", "BOOK", "LIBRI",
                            "MIME")):
        return "MimeTypes"
    if any(k in n for k in ("DEVICE", "DISPOSITIV", "HARDWARE")):
        return "Devices"
    if any(k in n for k in ("STATUS", "STATO", "NOTIF")):
        return "Status"
    if any(k in n for k in ("ACTION", "AZION")):
        return "Actions"
    return "Applications"


# --------------------------------------------------------------------------
#  Scansione icone
# --------------------------------------------------------------------------
def collect_icons(path):
    """Tutti i file icona sotto path, ricorsivamente."""
    path = Path(path)
    out = []
    for root, _dirs, files in os.walk(path):
        for f in sorted(files):
            if f.lower().endswith(EXTENSIONS):
                out.append(os.path.join(root, f))
    return out


def count_icons(path):
    return len(collect_icons(path))


def list_themes():
    """Temi presenti in ~/.local/share/icons (esclusi default/cache)."""
    if not ICONS_DIR.is_dir():
        return []
    out = []
    for e in sorted(os.listdir(ICONS_DIR)):
        p = ICONS_DIR / e
        if p.is_dir() and e != "default":
            out.append(e)
    return out


# --------------------------------------------------------------------------
#  1. ESTRAZIONE da .ico / .exe / .dll / .icl
# --------------------------------------------------------------------------
def _stride(bits, w):
    return ((w * bits + 31) // 32) * 4


def read_dib_to_img(data):
    """Ricostruisce un'immagine RGBA da una risorsa DIB grezza (RT_ICON).

    Ritorna un PIL.Image o None. Import di PIL locale così il core
    resta importabile anche dove PIL manca (la GUI lo richiede comunque).
    """
    from PIL import Image
    if len(data) < 40:
        return None
    hdr_sz = struct.unpack_from("<I", data, 0)[0]
    if hdr_sz not in (40, 108, 124) or len(data) < hdr_sz:
        return None
    width = struct.unpack_from("<i", data, 4)[0]
    height = struct.unpack_from("<i", data, 8)[0]
    planes = struct.unpack_from("<H", data, 12)[0]
    bpp = struct.unpack_from("<H", data, 14)[0]
    if planes != 1 or width == 0 or height == 0:
        return None
    top_down = height < 0
    height = abs(height)

    clr_used = struct.unpack_from("<I", data, 32)[0] if hdr_sz >= 40 else 0
    palette_entries = 0
    if bpp in (1, 4, 8):
        palette_entries = clr_used if clr_used else (1 << bpp)
    palette_off = hdr_sz
    pixel_off = palette_off + palette_entries * 4
    if len(data) < pixel_off:
        return None

    palette = None
    if palette_entries:
        palette = []
        for i in range(palette_entries):
            b, g, r, _ = data[palette_off + i * 4: palette_off + (i + 1) * 4]
            palette.append((r, g, b))

    if bpp == 32:
        s = _stride(32, width)
        h_real = height // 2 if (pixel_off + s * (height // 2)) <= len(data) else height
        px = data[pixel_off: pixel_off + s * h_real]
        if len(px) < s * h_real:
            return None
        img = Image.new("RGBA", (width, h_real))
        for y in range(h_real):
            sy = y if top_down else (h_real - 1 - y)
            row = px[sy * s: sy * s + width * 4]
            for x in range(width):
                b, g, r, a = row[x * 4:(x + 1) * 4]
                img.putpixel((x, y), (r, g, b, a))
        return img

    if bpp in (24, 8, 4, 1):
        h_real = height // 2
        if h_real <= 0:
            return None
        s_col = _stride(bpp, width)
        col = data[pixel_off: pixel_off + s_col * h_real]
        if len(col) < s_col * h_real:
            return None
        mask_off = pixel_off + s_col * h_real
        s_m = _stride(1, width)
        mask = data[mask_off: mask_off + s_m * h_real] \
            if (mask_off + s_m * h_real) <= len(data) else None
        img = Image.new("RGBA", (width, h_real))

        def alpha(sy, x):
            if mask is None:
                return 255
            byte = mask[sy * s_m + (x // 8)]
            bit = 7 - (x % 8)
            return 0 if ((byte >> bit) & 1) else 255

        for y in range(h_real):
            sy = y if top_down else (h_real - 1 - y)
            if bpp == 24:
                row = col[sy * s_col: sy * s_col + width * 3]
                for x in range(width):
                    b, g, r = row[x * 3:(x + 1) * 3]
                    img.putpixel((x, y), (r, g, b, alpha(sy, x)))
            elif bpp == 8 and palette:
                row = col[sy * s_col: sy * s_col + width]
                for x in range(width):
                    r, g, b = palette[row[x]]
                    img.putpixel((x, y), (r, g, b, alpha(sy, x)))
            elif bpp == 4 and palette:
                row = col[sy * s_col: sy * s_col + ((width + 1) // 2)]
                for x in range(width):
                    byte = row[x // 2]
                    idx = (byte >> 4) & 0xF if (x % 2) == 0 else (byte & 0xF)
                    r, g, b = palette[idx]
                    img.putpixel((x, y), (r, g, b, alpha(sy, x)))
            elif bpp == 1 and palette:
                row = col[sy * s_col: sy * s_col + ((width + 7) // 8)]
                for x in range(width):
                    byte = row[x // 8]
                    bit = 7 - (x % 8)
                    idx = 1 if ((byte >> bit) & 1) else 0
                    r, g, b = palette[idx]
                    img.putpixel((x, y), (r, g, b, alpha(sy, x)))
        return img

    return None


def extract_from_file(src_file, out_root="extracted", progress=None):
    """Estrae le icone da un file .ico/.exe/.dll/.icl.

    Richiede wrestool (pacchetto icoutils). Ritorna un dict con conteggi.
    `progress` opzionale: callback(str) per messaggi di avanzamento.
    """
    from PIL import Image
    src_file = Path(src_file)
    name = clean_name(src_file.stem)
    workdir = Path(out_root) / name
    rawdir, pngdir = workdir / "raw", workdir / "png"
    rawdir.mkdir(parents=True, exist_ok=True)
    pngdir.mkdir(parents=True, exist_ok=True)

    if progress:
        progress(f"Estraggo risorse da {src_file.name}...")

    subprocess.run(["wrestool", "--raw", "-x", "-t", "3",
                    "-o", str(rawdir), str(src_file)],
                   capture_output=True)

    saved = skipped = 0
    raw_files = sorted(p for p in rawdir.glob("*") if p.is_file())
    for p in raw_files:
        data = p.read_bytes()
        out_png = pngdir / (p.name + ".png")
        if data.startswith(PNG_SIG):
            out_png.write_bytes(data)
            saved += 1
            continue
        img = read_dib_to_img(data)
        if img is None:
            skipped += 1
            continue
        img.save(out_png, "PNG")
        saved += 1

    return {"file": src_file.name, "raw": len(raw_files),
            "png": saved, "skipped": skipped, "pngdir": str(pngdir)}


def wrestool_available():
    return subprocess.run(["which", "wrestool"],
                          capture_output=True).returncode == 0


# --------------------------------------------------------------------------
#  2. ICONE SIMBOLICHE (PNG → SVG 16×16 monocromatico)
# --------------------------------------------------------------------------
def _mask(img, alpha_thr=64, white_thr=242):
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    use_alpha = any(px[x, y][3] < 250 for y in range(0, h, max(1, h // 16))
                    for x in range(0, w, max(1, w // 16)))
    m = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            m[y][x] = (a >= alpha_thr) if use_alpha else \
                not (r >= white_thr and g >= white_thr and b >= white_thr)
    return m, w, h


def _reduce(m, w, h, grid, coverage):
    xs = [x for y in range(h) for x in range(w) if m[y][x]]
    ys = [y for y in range(h) for x in range(w) if m[y][x]]
    if not xs:
        return None
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    side = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, y0 = cx - side / 2, cy - side / 2
    cells = [[False] * grid for _ in range(grid)]
    step = side / grid
    for gy in range(grid):
        for gx in range(grid):
            filled = tot = 0
            ax0, ay0 = x0 + gx * step, y0 + gy * step
            for py in range(int(ay0), int(ay0 + step) + 1):
                for pxx in range(int(ax0), int(ax0 + step) + 1):
                    if 0 <= pxx < w and 0 <= py < h:
                        tot += 1
                        if m[py][pxx]:
                            filled += 1
            if tot and filled / tot >= coverage:
                cells[gy][gx] = True
    return cells


def _cells_to_svg(cells, grid):
    scale = 16 / grid
    rects = []
    for gy in range(grid):
        gx = 0
        while gx < grid:
            if cells[gy][gx]:
                start = gx
                while gx < grid and cells[gy][gx]:
                    gx += 1
                rects.append((start * scale, gy * scale,
                              (gx - start) * scale, scale))
            else:
                gx += 1
    bodies = "".join(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"/>'
                     for x, y, w, h in rects)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
            f'viewBox="0 0 16 16">\n<g fill="{GREY}">{bodies}</g>\n</svg>\n')


def make_symbolic(png_path, out_dir=None, grid=16, coverage=0.42):
    """Genera l'SVG simbolico da un PNG. Ritorna il percorso o None."""
    from PIL import Image
    png_path = Path(png_path)
    name = clean_name(png_path.stem) + "-symbolic"
    img = Image.open(png_path)
    m, w, h = _mask(img)
    cells = _reduce(m, w, h, grid, coverage)
    if cells is None:
        return None
    svg = _cells_to_svg(cells, grid)
    out_dir = Path(out_dir) if out_dir else png_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / (name + ".svg")
    dest.write_text(svg)
    return str(dest)


# --------------------------------------------------------------------------
#  3. COSTRUZIONE TEMA (index.theme + cache)
# --------------------------------------------------------------------------
def normalize_names(theme_dir):
    """Rinomina in-place file e cartelle: accenti via, spazi/underscore→-.
    Ritorna il numero di elementi rinominati.
    """
    theme_dir = Path(theme_dir)
    n = 0
    # bottom-up per rinominare prima i file, poi le cartelle
    for root, dirs, files in os.walk(theme_dir, topdown=False):
        for entry in files + dirs:
            new = clean_name(Path(entry).stem)
            ext = Path(entry).suffix
            new_full = new + ext
            if new_full != entry:
                src = os.path.join(root, entry)
                dst = os.path.join(root, new_full)
                i = 1
                while os.path.exists(dst):
                    dst = os.path.join(root, f"{new}-{i}{ext}")
                    i += 1
                os.rename(src, dst)
                n += 1
    return n


def build_index(theme_dir, theme_name=None, inherits="Mint-Y"):
    """Genera index.theme scansionando le sottocartelle con icone.
    Ritorna il numero di cartelle incluse.
    """
    theme_dir = Path(theme_dir)
    theme_name = theme_name or theme_dir.name
    dirs = []
    for d in sorted(p for p in theme_dir.rglob("*") if p.is_dir()):
        if any(f.suffix.lower() in EXTENSIONS for f in d.iterdir() if f.is_file()):
            dirs.append(str(d.relative_to(theme_dir)))
    if not dirs:
        return 0
    lines = ["[Icon Theme]", f"Name={theme_name}",
             "Comment=Generated by Icons-Packet", f"Inherits={inherits}",
             "Directories=" + ",".join(dirs), ""]
    for d in dirs:
        ctx = map_context(d.split("/")[0])
        lines += [f"[{d}]", "Size=48", "MinSize=16", "MaxSize=512",
                  f"Context={ctx}", "Type=Scalable", ""]
    (theme_dir / "index.theme").write_text("\n".join(lines))
    return len(dirs)


def update_cache(theme_dir):
    """Rigenera la cache. Ritorna (ok: bool, message: str)."""
    theme_dir = Path(theme_dir)
    cache = theme_dir / "icon-theme.cache"
    if cache.exists():
        cache.unlink()
    r = subprocess.run(["gtk-update-icon-cache", "-f", str(theme_dir)],
                       capture_output=True, text=True)
    ok = (r.returncode == 0)
    msg = (r.stderr or r.stdout).strip() or ("OK" if ok else "errore")
    return ok, msg


# --------------------------------------------------------------------------
#  4. ANTI-COLLISIONI (giganti)
# --------------------------------------------------------------------------
def _system_vocabulary(exclude_dir):
    exclude = os.path.abspath(exclude_dir)
    names = set()
    for base in ["/usr/share/icons"]:
        if not os.path.isdir(base):
            continue
        for root, _d, files in os.walk(base):
            if os.path.abspath(root).startswith(exclude):
                continue
            for f in files:
                stem = _stem(f)
                if stem:
                    names.add(stem)
                    if stem.endswith("-symbolic"):
                        names.add(stem[:-len("-symbolic")])
    return names


def _stem(filename):
    base = os.path.basename(filename)
    for ext in EXTENSIONS:
        if base.lower().endswith(ext):
            return base[:-len(ext)]
    return None


def find_collisions(theme_dir, prefix=PREFIX, allowed=None):
    """Elenca i file che scippano nomi di sistema. Ritorna lista di path."""
    theme_dir = os.path.abspath(theme_dir)
    allowed = allowed or set()
    vocab = _system_vocabulary(theme_dir)
    hits = []
    for root, _d, files in os.walk(theme_dir):
        for f in sorted(files):
            s = _stem(f)
            if not s or s.startswith(prefix):
                continue
            if s in vocab and s not in allowed:
                hits.append(os.path.join(root, f))
    return hits


def defuse_collisions(collisions, prefix=PREFIX):
    """Rinomina i file in collisione col prefisso. Ritorna il conteggio."""
    n = 0
    for c in collisions:
        folder, name = os.path.split(c)
        new = os.path.join(folder, prefix + name)
        i = 1
        while os.path.exists(new):
            root, ext = os.path.splitext(prefix + name)
            new = os.path.join(folder, f"{root}-{i}{ext}")
            i += 1
        os.rename(c, new)
        n += 1
    return n


def prefix_all(theme_dir, prefix=PREFIX):
    """Prefissa TUTTE le icone non già prefissate. Ritorna il conteggio."""
    theme_dir = Path(theme_dir)
    n = 0
    files = [p for p in theme_dir.rglob("*")
             if p.is_file() and p.suffix.lower() in EXTENSIONS
             and not p.name.startswith(prefix)]
    for p in files:
        new_stem = prefix + clean_name(p.stem)
        dst = p.with_name(new_stem + p.suffix)
        i = 1
        while dst.exists():
            dst = p.with_name(f"{new_stem}-{i}{p.suffix}")
            i += 1
        p.rename(dst)
        n += 1
    return n


# --------------------------------------------------------------------------
#  5. ATTIVAZIONE TEMA
# --------------------------------------------------------------------------
def get_active_theme():
    r = subprocess.run(["gsettings", "get",
                        "org.cinnamon.desktop.interface", "icon-theme"],
                       capture_output=True, text=True)
    return r.stdout.strip().strip("'") if r.returncode == 0 else None


def set_active_theme(theme_name):
    return subprocess.run(["gsettings", "set",
                           "org.cinnamon.desktop.interface", "icon-theme",
                           theme_name]).returncode == 0


def apply_icon_to(target, icon_path):
    """Applica un'icona a un file/cartella via gio metadata."""
    uri = icon_path if icon_path.startswith("file://") else "file://" + icon_path
    return subprocess.run(["gio", "set", target,
                           "metadata::custom-icon", uri],
                          capture_output=True, text=True).returncode == 0


# --------------------------------------------------------------------------
#  6. SOSTITUZIONE ICONE DI SISTEMA (cestino pieno/vuoto, cartelle, ecc.)
# --------------------------------------------------------------------------
# Catalogo delle "caselle" di sistema più utili: (nome_standard, etichetta).
# Installando un tuo PNG/SVG con quel nome nel tema, sostituisci l'icona
# di sistema ovunque compaia (pannello, Nemo, menu...).
SYSTEM_SLOTS = [
    ("user-trash",          "Cestino vuoto"),
    ("user-trash-full",     "Cestino pieno"),
    ("folder",              "Cartella generica"),
    ("user-home",           "Cartella Home"),
    ("folder-download",     "Scaricati"),
    ("folder-documents",    "Documenti"),
    ("folder-pictures",     "Immagini"),
    ("folder-music",        "Musica"),
    ("folder-videos",       "Video"),
    ("folder-desktop",      "Scrivania"),
    ("computer",            "Computer"),
    ("drive-harddisk",      "Disco fisso"),
    ("drive-removable-media", "Chiavetta USB"),
    ("network-workgroup",   "Rete"),
    ("text-x-generic",      "File di testo"),
    ("image-x-generic",     "Immagine generica"),
    ("application-x-executable", "Eseguibile"),
]


def install_system_icon(theme_dir, slot_name, source_image, category="places"):
    """Installa `source_image` nel tema col nome standard `slot_name`, così
    sostituisce l'icona di sistema corrispondente.

    L'icona viene messa in una sottocartella dedicata (default 'places') e
    conserva l'estensione originale (.png/.svg). Ritorna il percorso creato.
    NON prefissa il nome (deve restare quello standard per fare effetto).
    """
    theme_dir = Path(theme_dir)
    ext = Path(source_image).suffix.lower()
    if ext not in EXTENSIONS:
        ext = ".png"
    dest_dir = theme_dir / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (slot_name + ext)
    import shutil
    shutil.copy(source_image, dest)
    return str(dest)


def system_slots():
    """Ritorna la lista delle caselle di sistema disponibili."""
    return list(SYSTEM_SLOTS)


# ==========================================================================
#  GRUPPO A — MANUTENZIONE (cura della collezione)
# ==========================================================================
def find_duplicates(theme_dir, progress=None):
    """Trova icone identiche per CONTENUTO (hash del file), non per nome.
    Ritorna una lista di gruppi: ogni gruppo è la lista di path identici.
    """
    import hashlib
    theme_dir = Path(theme_dir)
    by_hash = {}
    files = [p for p in theme_dir.rglob("*")
             if p.is_file() and p.suffix.lower() in EXTENSIONS]
    for i, p in enumerate(files):
        if progress and i % 50 == 0:
            progress(f"Analizzo {i}/{len(files)}...")
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        by_hash.setdefault(h, []).append(str(p))
    return [sorted(g) for g in by_hash.values() if len(g) > 1]


def remove_duplicates(groups, keep="first"):
    """Rimuove i doppioni tenendo un file per gruppo. Ritorna quanti rimossi.
    keep='first' tiene il primo (ordine alfabetico), rimuove gli altri.
    """
    removed = 0
    for group in groups:
        survivors = group[:1] if keep == "first" else group[-1:]
        for p in group:
            if p not in survivors:
                try:
                    os.remove(p)
                    removed += 1
                except OSError:
                    pass
    return removed


def contact_sheet(theme_dir, out_path, cols=8, thumb=64, label=True):
    """Genera un mosaico PNG di tutta la collezione, con nome sotto ogni icona.
    Ritorna (percorso, numero_icone).
    """
    from PIL import Image, ImageDraw, ImageFont
    theme_dir = Path(theme_dir)
    files = [p for p in sorted(theme_dir.rglob("*"))
             if p.is_file() and p.suffix.lower() in (".png", ".xpm")]
    if not files:
        return None, 0
    pad = 8
    cell_h = thumb + (16 if label else 0) + pad
    cell_w = thumb + pad
    rows = (len(files) + cols - 1) // cols
    W, H = cols * cell_w + pad, rows * cell_h + pad
    sheet = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    for i, p in enumerate(files):
        r, c = divmod(i, cols)
        x = pad + c * cell_w
        y = pad + r * cell_h
        try:
            ic = Image.open(p).convert("RGBA")
            ic.thumbnail((thumb, thumb))
            ox = x + (thumb - ic.width) // 2
            oy = y + (thumb - ic.height) // 2
            sheet.paste(ic, (ox, oy), ic)
        except Exception:
            draw.rectangle([x, y, x + thumb, y + thumb], outline=(200, 200, 200))
        if label and font:
            name = p.stem[:10]
            draw.text((x, y + thumb + 2), name, fill=(80, 80, 80), font=font)
    out_path = str(out_path)
    sheet.save(out_path)
    return out_path, len(files)


def _dominant_color(img, size=16):
    """Colore medio (RGB) dei pixel non trasparenti, campionato a bassa risoluzione."""
    small = img.convert("RGBA").resize((size, size))
    px = small.load()
    rs = gs = bs = n = 0
    for y in range(size):
        for x in range(size):
            r, g, b, a = px[x, y]
            if a > 32:
                rs += r; gs += g; bs += b; n += 1
    if n == 0:
        return (0, 0, 0)
    return (rs // n, gs // n, bs // n)


def find_similar(reference_png, theme_dir, top=12):
    """Trova le icone graficamente più simili al riferimento, per colore
    dominante. Ritorna lista di (path, distanza) ordinata dalla più simile.
    """
    from PIL import Image
    ref = _dominant_color(Image.open(reference_png))
    theme_dir = Path(theme_dir)
    scored = []
    for p in theme_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".png", ".xpm"):
            try:
                c = _dominant_color(Image.open(p))
            except Exception:
                continue
            dist = sum((a - b) ** 2 for a, b in zip(ref, c)) ** 0.5
            scored.append((str(p), round(dist, 1)))
    scored.sort(key=lambda t: t[1])
    return scored[:top]


# ==========================================================================
#  GRUPPO B — PRODUZIONE (creare/rifinire icone)
# ==========================================================================
STANDARD_SIZES = (16, 24, 32, 48, 64, 128, 256)


def normalize_sizes(png_path, out_dir=None, sizes=STANDARD_SIZES):
    """Da un PNG (spesso sovradimensionato) genera il set completo di taglie,
    ridimensionato con qualità. Ritorna la lista dei percorsi creati.
    """
    from PIL import Image
    png_path = Path(png_path)
    out_dir = Path(out_dir) if out_dir else png_path.parent / (png_path.stem + "-sizes")
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(png_path).convert("RGBA")
    created = []
    for s in sizes:
        resized = img.resize((s, s), Image.LANCZOS)
        dest = out_dir / f"{clean_name(png_path.stem)}-{s}.png"
        resized.save(dest)
        created.append(str(dest))
    return created


def recolor(png_path, target_hex, out_path=None):
    """Ricolora un'icona (utile per le monocromatiche): sostituisce la tinta
    mantenendo l'alpha. target_hex tipo '#3b82f6'. Ritorna il percorso.
    """
    from PIL import Image
    png_path = Path(png_path)
    tr = int(target_hex[1:3], 16)
    tg = int(target_hex[3:5], 16)
    tb = int(target_hex[5:7], 16)
    img = Image.open(png_path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            _, _, _, a = px[x, y]
            if a > 0:
                px[x, y] = (tr, tg, tb, a)
    out_path = str(out_path) if out_path else str(
        png_path.with_name(clean_name(png_path.stem) + "-recolored.png"))
    img.save(out_path)
    return out_path


def invert_light_dark(png_path, out_path=None):
    """Inverte chiaro↔scuro mantenendo l'alpha (per adattare a temi opposti)."""
    from PIL import Image
    png_path = Path(png_path)
    img = Image.open(png_path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            px[x, y] = (255 - r, 255 - g, 255 - b, a)
    out_path = str(out_path) if out_path else str(
        png_path.with_name(clean_name(png_path.stem) + "-inverted.png"))
    img.save(out_path)
    return out_path


def trim_and_pad(png_path, out_path=None, pad_ratio=0.08):
    """Rifila i margini trasparenti, ricentra e applica un padding uniforme.
    pad_ratio = frazione del lato usata come margine. Ritorna il percorso.
    """
    from PIL import Image
    png_path = Path(png_path)
    img = Image.open(png_path).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    side = max(img.size)
    pad = int(side * pad_ratio)
    canvas = side + 2 * pad
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    ox = (canvas - img.width) // 2
    oy = (canvas - img.height) // 2
    out.paste(img, (ox, oy), img)
    out_path = str(out_path) if out_path else str(
        png_path.with_name(clean_name(png_path.stem) + "-trimmed.png"))
    out.save(out_path)
    return out_path


# ==========================================================================
#  GRUPPO C — DISTRIBUZIONE (condividere)
# ==========================================================================
def export_theme_package(theme_dir, out_zip=None, author="Francesco",
                         license_name="MIT"):
    """Crea uno zip pronto per la pubblicazione: tema + LICENSE + README.
    Ritorna il percorso dello zip.
    """
    import zipfile
    theme_dir = Path(theme_dir)
    name = theme_dir.name
    out_zip = str(out_zip) if out_zip else str(theme_dir.parent / f"{name}.zip")

    readme = (f"# {name}\n\nIcon theme created with Icons-Packet.\n\n"
              f"## Install\nCopy the `{name}` folder into "
              f"`~/.local/share/icons/`, then select it in "
              f"Settings → Themes → Icons.\n\n"
              f"Author: {author}\nLicense: {license_name}\n")
    license_txt = (f"{license_name} License\n\n"
                   f"Copyright (c) {author}\n\n"
                   "Permission is hereby granted, free of charge, to any "
                   "person obtaining a copy of this icon theme...\n")

    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in theme_dir.rglob("*"):
            if p.is_file():
                z.write(p, arcname=os.path.join(name, str(p.relative_to(theme_dir))))
        z.writestr(f"{name}/README.md", readme)
        z.writestr(f"{name}/LICENSE", license_txt)
    return out_zip


def make_showcase(theme_dir, out_path, picks=12, bg=(40, 42, 54)):
    """Immagine promozionale: una selezione di icone disposta con gusto su
    uno sfondo. Ritorna (percorso, numero_icone_usate).
    """
    from PIL import Image
    theme_dir = Path(theme_dir)
    files = [p for p in sorted(theme_dir.rglob("*"))
             if p.is_file() and p.suffix.lower() in (".png", ".xpm")]
    if not files:
        return None, 0
    # scegli fino a `picks` icone distribuite lungo la collezione
    step = max(1, len(files) // picks)
    chosen = files[::step][:picks]
    cols = min(len(chosen), 4)
    rows = (len(chosen) + cols - 1) // cols
    cell, pad = 96, 32
    W = cols * cell + (cols + 1) * pad
    H = rows * cell + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), bg)
    for i, p in enumerate(chosen):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = pad + r * (cell + pad)
        try:
            ic = Image.open(p).convert("RGBA")
            ic.thumbnail((cell, cell))
            ox = x + (cell - ic.width) // 2
            oy = y + (cell - ic.height) // 2
            sheet.paste(ic, (ox, oy), ic)
        except Exception:
            pass
    out_path = str(out_path)
    sheet.save(out_path)
    return out_path, len(chosen)


# ==========================================================================
#  GRUPPO D — SICUREZZA & COMODITÀ (per tutti)
# ==========================================================================
def backup_theme(theme_dir, backup_root=None):
    """Snapshot compresso del tema, con timestamp. Ritorna il percorso.
    """
    import zipfile
    import datetime
    theme_dir = Path(theme_dir)
    backup_root = Path(backup_root) if backup_root else \
        Path.home() / ".local/share/icons-packet-backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = backup_root / f"{theme_dir.name}-{stamp}.zip"
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for p in theme_dir.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(p.relative_to(theme_dir)))
    return str(dest)


def list_backups(theme_name, backup_root=None):
    """Elenca i backup disponibili per un tema, dal più recente."""
    backup_root = Path(backup_root) if backup_root else \
        Path.home() / ".local/share/icons-packet-backups"
    if not backup_root.is_dir():
        return []
    out = [str(p) for p in backup_root.glob(f"{theme_name}-*.zip")]
    return sorted(out, reverse=True)


def restore_backup(zip_path, theme_dir):
    """Ripristina un tema da un backup (sovrascrive). Ritorna True."""
    import zipfile
    import shutil
    theme_dir = Path(theme_dir)
    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(theme_dir)
    return True


def health_check(theme_dir):
    """Diagnostica il tema secondo la checklist della FAQ.
    Ritorna una lista di (esito, messaggio): esito è 'ok' | 'warn' | 'err'.
    """
    theme_dir = Path(theme_dir)
    report = []

    # 1. index.theme esiste?
    idx = theme_dir / "index.theme"
    if not idx.is_file():
        report.append(("err", "Manca index.theme: il tema è invisibile al sistema."))
        return report
    report.append(("ok", "index.theme presente."))

    text = idx.read_text(errors="ignore")

    # 2. Inherits da tema completo?
    inh = None
    for line in text.splitlines():
        if line.startswith("Inherits="):
            inh = line.split("=", 1)[1].strip()
            break
    if not inh:
        report.append(("warn", "Nessun Inherits: icone mancanti diventeranno triangoli."))
    elif inh in ("Mint-Y", "Mint-Y-Dark", "hicolor", "Adwaita",
                 "gnome", "breeze"):
        report.append(("ok", f"Inherits da tema completo ({inh})."))
    else:
        report.append(("warn", f"Inherits='{inh}': verifica che sia un tema COMPLETO "
                               "(le varianti colorate come Mint-X-Red danno triangoli)."))

    # 3. accenti nei nomi?
    accented = [str(p.relative_to(theme_dir)) for p in theme_dir.rglob("*")
                if any(ord(c) > 127 for c in p.name)]
    if accented:
        report.append(("err", f"{len(accented)} file/cartelle con accenti: "
                              "la cache sarà invalida. Bonifica i nomi."))
    else:
        report.append(("ok", "Nessun accento nei nomi."))

    # 4. spazi/underscore?
    dirty = [p for p in theme_dir.rglob("*")
             if " " in p.name or "_" in p.name]
    if dirty:
        report.append(("warn", f"{len(dirty)} nomi con spazi/underscore "
                               "(convenzione: solo trattini)."))
    else:
        report.append(("ok", "Nomi conformi (solo trattini)."))

    # 5. collisioni con icone di sistema?
    cols = find_collisions(str(theme_dir))
    if cols:
        report.append(("warn", f"{len(cols)} collisioni di nome con icone di "
                               "sistema (possibili giganti). Usa 'Caccia ai giganti'."))
    else:
        report.append(("ok", "Nessuna collisione con icone di sistema."))

    # 6. cache presente e valida?
    cache = theme_dir / "icon-theme.cache"
    if not cache.is_file():
        report.append(("warn", "Cache assente (non grave: il tema funziona comunque)."))
    else:
        report.append(("ok", "Cache presente."))

    return report


if __name__ == "__main__":
    # smoke test minimo delle funzioni pure
    print("to_hyphens('My Icon_set'):", to_hyphens("My Icon_set"))
    print("strip_accents('icòna'):", strip_accents("icòna"))
    print("category_label('5-EMAIL-e-POSTA'):", category_label("5-EMAIL-e-POSTA"))
    print("map_context('3-CESTINI-TRASH'):", map_context("3-CESTINI-TRASH"))
    print("map_context('5-FRECCE-EMOJI'):", map_context("5-FRECCE-EMOJI"))
