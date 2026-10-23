#!/usr/bin/env python3
##########################################################
##                 byBias Icons Packet                  ##
##               Right-click: paste icon                ##
##                 written in Python 3                  ##
##                          🌞                          ##
##       by FranzBias 2026 · github.com/FranzBias       ##
##            Licensed under the MIT License            ##
##          See LICENSE file for full license.          ##
##########################################################
# SPDX-License-Identifier: MIT
"""
icons_packet_paste.py — paste the clipboard image as a folder/file icon
(right-click action).

WHY: copy an image (browser, screenshot, GIMP) or an image file in Nemo,
right-click a folder → "Paste icon", and the folder takes it. The image is
saved so the icon keeps working: raster images are scaled down to 256 px at
most, SVG files are copied as they are.

Where the images go:
    $ICONS_PACKET_PASTE_DIR if set, otherwise <Pictures>/Icons-Packet/pasted/
    (<Pictures> is the user's pictures folder: ~/Pictures, ~/Bilder, ...).

Usage:  icons_packet_paste.py PATH
"""

import os
import shutil
import subprocess
import sys
import time
from urllib.parse import unquote, urlparse

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons_packet_core as core  # noqa: E402
from icons_packet_i18n import set_language_from_locale, tr  # noqa: E402

MAX_SIZE = 256
IMAGE_EXT = (".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
             ".xpm", ".ico", ".tif", ".tiff")


def paste_dir():
    custom = os.environ.get("ICONS_PACKET_PASTE_DIR")
    if custom:
        return os.path.expanduser(custom)
    pictures = (GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)
                or os.path.expanduser("~/Pictures"))
    return os.path.join(pictures, "Icons-Packet", "pasted")


def notify(text, icon="folder-pictures"):
    subprocess.run(["notify-send", "-i", icon, tr("Paste icon"), text], check=False)


def copied_image_file(clipboard):
    """An image FILE copied in Nemo (Ctrl+C) or as a uri-list, else None."""
    paths = []
    sel = clipboard.wait_for_contents(Gdk.Atom.intern("x-special/gnome-copied-files", False))
    if sel and sel.get_data():
        lines = sel.get_data().decode("utf-8", "replace").splitlines()
        paths = [unquote(urlparse(l).path) for l in lines[1:] if l.startswith("file://")]
    if not paths:
        uris = clipboard.wait_for_uris() or []
        paths = [unquote(urlparse(u).path) for u in uris if u.startswith("file://")]
    for p in paths:
        if os.path.isfile(p) and p.lower().endswith(IMAGE_EXT):
            return p
    return None


def unique_path(dest, ext):
    """pasted-YYYY-MM-DD-HHMMSS.<ext> in dest, never overwriting."""
    base = time.strftime("pasted-%Y-%m-%d-%H%M%S")
    path = os.path.join(dest, base + ext)
    n = 2
    while os.path.exists(path):
        path = os.path.join(dest, f"{base}-{n}{ext}")
        n += 1
    return path


def save_pixbuf(pixbuf, dest):
    """Scale down to MAX_SIZE (keeping proportions) and save as PNG."""
    w, h = pixbuf.get_width(), pixbuf.get_height()
    if max(w, h) > MAX_SIZE:
        k = MAX_SIZE / max(w, h)
        pixbuf = pixbuf.scale_simple(max(1, round(w * k)), max(1, round(h * k)),
                                     GdkPixbuf.InterpType.HYPER)
    path = unique_path(dest, ".png")
    pixbuf.savev(path, "png", [], [])
    return path


def main():
    set_language_from_locale()
    targets = [a for a in sys.argv[1:] if os.path.exists(a)]
    if not targets:
        notify(tr("No folder or file selected."), "dialog-warning")
        return 1
    target = targets[0]
    dest = paste_dir()
    os.makedirs(dest, exist_ok=True)
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    saved = None
    src = copied_image_file(clipboard)
    if src and src.lower().endswith(".svg"):
        saved = unique_path(dest, ".svg")
        shutil.copy2(src, saved)
    elif src:
        try:
            saved = save_pixbuf(GdkPixbuf.Pixbuf.new_from_file(src), dest)
        except GLib.Error:
            saved = None
    else:
        pixbuf = clipboard.wait_for_image()
        if pixbuf:
            saved = save_pixbuf(pixbuf, dest)

    if not saved:
        notify(tr("There is no image in the clipboard.\n"
                  "Copy an image (or an image file in Nemo) and try again."),
               "dialog-warning")
        return 1

    name = os.path.basename(target.rstrip("/"))
    if not core.apply_icon_to(target, saved):
        notify(tr("Icon saved, but not applied to «{name}».").format(name=name),
               "dialog-error")
        return 1
    # Nemo shows the new icon only after reloading the folder
    notify(tr("Icon applied to «{name}».\nSaved as {file}\nPress F5 in Nemo to see it.")
           .format(name=name, file=saved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
