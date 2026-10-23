#!/usr/bin/env python3
##########################################################
##                 byBias Icons Packet                  ##
##               Right-click: change icon               ##
##                 written in Python 3                  ##
##                          🌞                          ##
##       by FranzBias 2026 · github.com/FranzBias       ##
##            Licensed under the MIT License            ##
##          See LICENSE file for full license.          ##
##########################################################
# SPDX-License-Identifier: MIT
"""
icons_packet_pick.py — pick an icon from your collection (right-click action).

WHY: a quick way, straight from Nemo, to give a folder or file one of YOUR
icons, organised in YOUR categories (the top-level folders of the
byBias-Icons theme built with Icons-Packet), using the Linux Mint XApp
icon chooser.

Usage:
    icons_packet_pick.py               pick an icon, its path goes to the clipboard
    icons_packet_pick.py PATH          pick an icon and apply it to PATH

Remove a custom icon:  gio set -t unset PATH metadata::custom-icon
"""

import os
import subprocess
import sys

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gdk, Gtk, XApp  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons_packet_core as core  # noqa: E402
from icons_packet_i18n import set_language_from_locale, tr  # noqa: E402

THEME_NAMES = ("byBias-Icons", "byBias-Icone")   # current name, old name


def message(kind, text):
    d = Gtk.MessageDialog(message_type=kind, buttons=Gtk.ButtonsType.OK, text=text)
    d.run()
    d.destroy()


def notify(text):
    subprocess.run(["notify-send", "-i", "folder-pictures", tr("Change icon"), text],
                   check=False)


def main():
    set_language_from_locale()
    theme = next((core.ICONS_DIR / n for n in THEME_NAMES if (core.ICONS_DIR / n).is_dir()),
                 None)
    if theme is None:
        message(Gtk.MessageType.ERROR,
                tr("The byBias-Icons theme was not found in ~/.local/share/icons: "
                   "build it first with \"Create / update theme\"."))
        return 1

    # XApp custom categories show icon NAMES from the current icon theme, not
    # file paths (with paths they stay empty). So this process alone uses the
    # theme as its icon theme; the chosen name is mapped back to its file.
    Gtk.Settings.get_default().set_property("gtk-icon-theme-name", theme.name)
    paths = {}

    dialog = XApp.IconChooserDialog()
    dialog.set_property("allow-paths", True)
    dialog.set_title(tr("Choose an icon from the collection"))
    for folder in sorted(os.listdir(theme)):
        p = theme / folder
        if not p.is_dir():
            continue
        names = []
        for f in core.collect_icons(p):
            stem = os.path.splitext(os.path.basename(f))[0]
            if stem not in paths:            # first file wins on duplicate names
                paths[stem] = f
                names.append(stem)
        if names:
            dialog.add_custom_category(core.category_label(folder), names)

    if not paths:
        dialog.destroy()
        message(Gtk.MessageType.ERROR, tr("No icons found in the theme."))
        return 1

    response = dialog.run()
    icon = dialog.get_icon_string() if response == Gtk.ResponseType.OK else None
    dialog.destroy()
    if not icon:
        return 0
    icon = paths.get(icon, icon)
    if not icon.startswith(("/", "file://")):
        # a name from the standard categories: resolve it to a real file
        info = Gtk.IconTheme.get_default().lookup_icon(icon, 256, 0)
        if info and info.get_filename():
            icon = info.get_filename()

    if len(sys.argv) > 1:
        target = sys.argv[1]
        name = os.path.basename(target.rstrip("/"))
        if not core.apply_icon_to(target, icon):
            message(Gtk.MessageType.ERROR,
                    tr("Could not apply the icon to «{name}».").format(name=name))
            return 1
        # Nemo shows the new icon only after reloading the folder
        notify(tr("Icon applied to «{name}».\nPress F5 in Nemo to see it.").format(name=name))
    else:
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(icon, -1)
        clipboard.store()
        message(Gtk.MessageType.INFO,
                tr("Path copied to the clipboard:\n{path}").format(path=icon))
    return 0


if __name__ == "__main__":
    sys.exit(main())
