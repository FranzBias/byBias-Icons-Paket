#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################
##                 byBias Icons Packet                  ##
##                    GTK3 dashboard                    ##
##                 written in Python 3                  ##
##                          🌞                          ##
##       by FranzBias 2026 · github.com/FranzBias       ##
##            Licensed under the MIT License            ##
##          See LICENSE file for full license.          ##
##########################################################
# SPDX-License-Identifier: MIT
"""
icons_packet_gui.py — GTK3 interface of Icons-Packet 📦🦉

Main window as a "dashboard": every action is visible as a clickable
tile. Clicking an action opens its panel in the same window (stack),
with a "← Back" button to return to the menu.

All the logic lives in icons_packet_core.py: this file is only the interface.

by Franz & Aldus
"""

import os
import sys
import threading
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk  # noqa: E402

try:
    gi.require_version("XApp", "1.0")
    from gi.repository import XApp
    HAVE_XAPP = True
except (ValueError, ImportError):
    HAVE_XAPP = False

import icons_packet_core as core
from icons_packet_i18n import tr, set_language, get_language, LANGUAGES

APP_NAME = "Icons-Packet"
APP_VERSION = "1.0"
WEBSITE_URL = "https://www.xxxxx.yy"  # TODO Franz: update with the final URL

# Grouped actions. Each group: (group_title, [actions]).
# Each action: (id, icon, title, short_description)
# Base language is English; strings are looked up via tr() at render time.
ACTION_GROUPS = [
    ("Main flow", [
        ("extract",  "application-x-executable",
         "Extract icons", "From .ico, .exe, .dll, .icl files"),
        ("build",    "folder-new",
         "Create / update theme", "Generate index.theme and cache from a folder"),
        ("choose",   "insert-image-symbolic",
         "Apply icon", "Pick from the collection and apply to a folder"),
        ("symbolic", "emblem-system",
         "Symbolic icons", "Generate 16×16 monochrome SVGs from PNGs"),
        ("giants",   "edit-find-replace",
         "Hunt the giants", "Find and defuse name collisions"),
        ("prefix",   "emblem-important",
         "Prefix everything", "Zero substitutions: only your collection"),
        ("system",   "user-trash-full",
         "Replace system icons", "Full/empty trash, folders, etc."),
    ]),
    ("Maintenance — care for the collection", [
        ("duplicates", "edit-copy",
         "Find duplicates", "Identical icons by content, not name"),
        ("contact", "view-grid-symbolic",
         "Contact sheet", "Mosaic of the whole collection, exportable PNG"),
        ("similar", "edit-find",
         "Find similar", "Icons graphically close by colour"),
    ]),
    ("Production — create / refine", [
        ("sizes", "zoom-fit-best",
         "Normalize sizes", "From one big PNG to the full 16→256 set"),
        ("recolor", "applications-graphics",
         "Recolor / invert", "Apply a tint or invert light↔dark"),
        ("trim", "object-flip-horizontal",
         "Trim & center", "Uniform margins, centered icon"),
    ]),
    ("Distribution — share", [
        ("export", "package-x-generic",
         "Export package", "Zip with index.theme, LICENSE and README"),
        ("showcase", "image-x-generic",
         "Make showcase", "Promotional image of the theme"),
    ]),
    ("Safety & convenience", [
        ("backup", "document-save",
         "Backup / restore", "Snapshot of the theme, with 'go back'"),
        ("health", "object-select-symbolic",
         "Health-check", "Diagnoses the theme against the checklist"),
    ]),
]

# flat list for dispatching the panels
ACTIONS = [a for _grp, acts in ACTION_GROUPS for a in acts]


# --------------------------------------------------------------------------
#  GUI helpers
# --------------------------------------------------------------------------
def run_in_thread(fn, on_done):
    """Run fn() in a thread, then call on_done(result) in the main loop."""
    def worker():
        try:
            result = ("ok", fn())
        except Exception as e:  # noqa: BLE001
            result = ("err", str(e))
        GLib.idle_add(on_done, result)
    threading.Thread(target=worker, daemon=True).start()


def pick_folder(parent, title):
    dlg = Gtk.FileChooserDialog(
        title=title, parent=parent,
        action=Gtk.FileChooserAction.SELECT_FOLDER)
    dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
    dlg.set_current_folder(str(Path.home()))
    path = dlg.get_filename() if dlg.run() == Gtk.ResponseType.OK else None
    dlg.destroy()
    return path


def pick_files(parent, title):
    dlg = Gtk.FileChooserDialog(
        title=title, parent=parent, action=Gtk.FileChooserAction.OPEN)
    dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
    dlg.set_select_multiple(True)
    dlg.set_current_folder(str(Path.home()))
    files = dlg.get_filenames() if dlg.run() == Gtk.ResponseType.OK else []
    dlg.destroy()
    return files


def info(parent, text, kind=Gtk.MessageType.INFO):
    d = Gtk.MessageDialog(transient_for=parent, message_type=kind,
                          buttons=Gtk.ButtonsType.OK, text=text)
    d.run()
    d.destroy()


# --------------------------------------------------------------------------
#  Main window
# --------------------------------------------------------------------------
class IconsPacketWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_NAME)
        # WM_CLASS: the panel uses it to find icons-packet.desktop
        self.set_wmclass("icons-packet", "Icons-Packet")
        self.set_default_size(720, 540)
        self.set_position(Gtk.WindowPosition.CENTER)
        self._set_window_icon()
        self.set_titlebar(self._build_header_bar())

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.add(self.stack)

        self.stack.add_named(self._build_dashboard(), "dashboard")
        # one list page per group, and one panel per action, on demand
        self._group_pages = {}
        self._panels = {}
        # remember which group each action belongs to, for the Back button
        self._action_group = {
            action_id: gi
            for gi, (_title, actions) in enumerate(ACTION_GROUPS)
            for action_id, *_r in actions
        }

        self.show_all()

    def _set_window_icon(self):
        """Set the window icon from the file shipped in icon/."""
        here = Path(__file__).resolve().parent
        for name in ("icon/icons-packet-256.png", "icon/icons-packet.svg",
                     "icon/icons-packet-128.png"):
            p = here / name
            if p.exists():
                try:
                    self.set_icon_from_file(str(p))
                    return
                except Exception:
                    continue

    def _safe_icon(self, name, size, fallback="image-x-generic-symbolic"):
        """Return a Gtk.Image for `name` ONLY if the active icon theme
        really has it; otherwise use `fallback` (and if that is missing
        too, fall back again to 'image-missing' — never a broken triangle
        for no reason). Avoids the wrong generic icon when the system icon
        theme lacks a name we had taken for granted.
        """
        theme = Gtk.IconTheme.get_default()
        chosen = name if theme.has_icon(name) else fallback
        if not theme.has_icon(chosen):
            chosen = "image-missing"
        return Gtk.Image.new_from_icon_name(chosen, size)

    # ---- title bar with the menu at the top left ----
    def _build_header_bar(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title(APP_NAME)

        menu_btn = Gtk.MenuButton()
        menu_icon = Gtk.Image.new_from_icon_name("open-menu-symbolic",
                                                  Gtk.IconSize.BUTTON)
        menu_btn.set_image(menu_icon)
        menu_btn.set_tooltip_text(tr("Menu"))

        menu = Gtk.Menu()

        info_item = Gtk.MenuItem.new_with_label(tr("About Icons-Packet"))
        info_item.connect("activate", self._on_show_about)
        menu.append(info_item)

        link_item = Gtk.MenuItem.new_with_label(tr("Website"))
        link_item.connect("activate", self._on_open_website)
        menu.append(link_item)

        menu.append(Gtk.SeparatorMenuItem())

        # ---- Language submenu: the 10 README languages, with flags ----
        lang_item = Gtk.MenuItem.new_with_label(tr("Language"))
        lang_submenu = Gtk.Menu()
        current = get_language()
        group_ref = []
        for code, name, flag in LANGUAGES:
            radio = Gtk.RadioMenuItem.new_with_label(group_ref, f"{flag}  {name}")
            group_ref = radio.get_group()
            if code == current:
                radio.set_active(True)
            radio.connect("toggled", self._on_language_selected, code)
            lang_submenu.append(radio)
        lang_item.set_submenu(lang_submenu)
        menu.append(lang_item)

        menu.append(Gtk.SeparatorMenuItem())

        self._dark_item = Gtk.CheckMenuItem.new_with_label(tr("Dark theme"))
        settings = Gtk.Settings.get_default()
        theme_name = settings.get_property("gtk-theme-name") or ""
        is_dark_now = bool(settings.get_property("gtk-application-prefer-dark-theme")) \
            or theme_name.endswith("-Dark")
        self._dark_item.set_active(is_dark_now)
        self._dark_item.connect("toggled", self._on_toggle_dark_theme)
        menu.append(self._dark_item)

        menu.show_all()
        menu_btn.set_popup(menu)

        header.pack_start(menu_btn)
        return header

    def _on_language_selected(self, radio_item, code):
        """Change language and rebuild the pages, so every text updates
        right away, without restarting the app."""
        if not radio_item.get_active():
            return  # the toggled event fires twice (old one off, new one on)
        set_language(code)
        self._rebuild_all_pages()

    def _rebuild_all_pages(self):
        """Rebuild dashboard, group pages and action panels in the current
        language. Pages already open are removed from the stack and
        recreated the next time they are used."""
        current_name = self.stack.get_visible_child_name()

        for name in list(self._group_pages.keys()):
            page = self._group_pages.pop(name)
            self.stack.remove(page)
        for name in list(self._panels.keys()):
            panel = self._panels.pop(name)
            self.stack.remove(panel)

        old_dashboard = self.stack.get_child_by_name("dashboard")
        if old_dashboard:
            self.stack.remove(old_dashboard)
        new_dashboard = self._build_dashboard()
        self.stack.add_named(new_dashboard, "dashboard")
        new_dashboard.show_all()

        # also refresh the title bar (menu tooltip, etc.)
        new_header = self._build_header_bar()
        self.set_titlebar(new_header)
        new_header.show_all()

        # go back to the dashboard if the current page no longer exists
        if current_name and current_name != "dashboard" and \
           current_name.startswith("group-"):
            idx = int(current_name.split("-")[1])
            self._open_group(idx)
        else:
            self.stack.set_visible_child_name("dashboard")

    def _on_show_about(self, _item):
        dlg = Gtk.AboutDialog(transient_for=self)
        dlg.set_program_name(APP_NAME)
        dlg.set_version(APP_VERSION)
        dlg.set_comments(
            tr("Icon workshop for Cinnamon.") + "\n\n" +
            tr("Made with ❤️ by FranzBias"))
        dlg.set_website("https://github.com/FranzBias/byBias-Icons-Paket")
        dlg.set_website_label("GitHub")
        dlg.set_authors(["FranzBias"])
        dlg.set_license_type(Gtk.License.MIT_X11)

        here = Path(__file__).resolve().parent
        icon_path = here / "icon" / "icons-packet-256.png"
        logo_set = False
        if icon_path.exists():
            try:
                from gi.repository import GdkPixbuf
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    str(icon_path), 128, 128, True)
                dlg.set_logo(pixbuf)
                logo_set = True
            except Exception:
                logo_set = False
        if not logo_set:
            # no loadable pixbuf: use a safe system icon
            # instead of leaving the broken placeholder
            theme = Gtk.IconTheme.get_default()
            fallback = "image-x-generic" if theme.has_icon("image-x-generic") \
                else "image-missing"
            dlg.set_logo_icon_name(fallback)

        dlg.run()
        dlg.destroy()

    def _on_open_website(self, _item):
        try:
            Gtk.show_uri_on_window(self, WEBSITE_URL, Gdk.CURRENT_TIME)
        except Exception:
            info(self, f"Apri manualmente:\n{WEBSITE_URL}")

    def _on_toggle_dark_theme(self, item):
        """Cinnamon re-applies the theme from XSettings right after an app
        changes it at runtime (set_property), so the change was always
        undone at once. The only reliable way is to force GTK_THEME in
        the environment BEFORE GTK initialises.

        I use os.execvpe instead of opening a new process and closing this one:
        execvpe REPLACES the current process in place, reusing exactly the
        arguments the app was first started with (sys.argv), whatever the
        path — no ambiguity about script/folder, no race between "close"
        and "reopen".
        """
        want_dark = item.get_active()
        theme_name = "Mint-Y-Dark" if want_dark else "Mint-Y"

        env = os.environ.copy()
        env["GTK_THEME"] = theme_name

        os.execvpe(sys.executable, [sys.executable] + sys.argv, env)

    # ---- dashboard: only the 5 group buttons ----
    def _build_dashboard(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.set_margin_top(24)
        header.set_margin_bottom(12)
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large' weight='bold'>📦 {APP_NAME}</span>")
        subtitle = Gtk.Label()
        subtitle.set_text(tr('Icon workshop for Cinnamon'))
        subtitle.get_style_context().add_class("ip-dim")
        header.pack_start(title, False, False, 0)
        header.pack_start(subtitle, False, False, 0)
        box.pack_start(header, False, False, 0)

        groups_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        groups_box.set_margin_start(24)
        groups_box.set_margin_end(24)
        groups_box.set_margin_bottom(24)
        groups_box.set_margin_top(8)

        for group_index, (group_title, actions) in enumerate(ACTION_GROUPS):
            groups_box.pack_start(
                self._group_card(group_index, group_title, len(actions)),
                False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.add(groups_box)
        box.pack_start(scroll, True, True, 0)

        # footer with the active theme
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer.set_margin_start(24)
        footer.set_margin_end(24)
        footer.set_margin_bottom(12)
        active = core.get_active_theme() or "—"
        self.footer_label = Gtk.Label()
        self.footer_label.set_markup(
            f"<span size='medium'>{tr('Active theme')}: {GLib.markup_escape_text(active)}</span>")
        self.footer_label.get_style_context().add_class("ip-dim")
        self.footer_label.set_halign(Gtk.Align.START)
        footer.pack_start(self.footer_label, True, True, 0)
        box.pack_start(footer, False, False, 0)

        return box

    def _group_card(self, group_index, title, n_actions):
        """A large button for a whole group, styled as a clickable row."""
        btn = Gtk.Button()
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.set_margin_top(14)
        row.set_margin_bottom(14)
        row.set_margin_start(16)
        row.set_margin_end(16)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        name = Gtk.Label()
        name.set_markup(f"<b>{GLib.markup_escape_text(tr(title))}</b>")
        name.set_halign(Gtk.Align.START)
        count = Gtk.Label()
        count.set_markup(
            f"<span size='medium'>{n_actions} {tr('actions')}</span>")
        count.get_style_context().add_class("ip-dim")
        count.set_halign(Gtk.Align.START)
        text_box.pack_start(name, False, False, 0)
        text_box.pack_start(count, False, False, 0)

        arrow = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.BUTTON)

        row.pack_start(text_box, True, True, 0)
        row.pack_start(arrow, False, False, 0)
        btn.add(row)
        btn.connect("clicked", lambda _w: self._open_group(group_index))
        return btn

    # ---- group page: actions in a vertical list ----
    def _open_group(self, group_index):
        name = f"group-{group_index}"
        if name not in self._group_pages:
            page = self._build_group_page(group_index)
            self._group_pages[name] = page
            self.stack.add_named(page, name)
            page.show_all()
        self.stack.set_visible_child_name(name)

    def _build_group_page(self, group_index):
        group_title, actions = ACTION_GROUPS[group_index]
        outer, inner = self._panel_shell(group_title, back_target="dashboard")

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        for action_id, icon_name, label, desc in actions:
            listbox.add(self._action_row(action_id, icon_name, label, desc))
        inner.pack_start(listbox, False, False, 0)
        return outer

    def _action_row(self, action_id, icon_name, label, desc):
        """A clickable row of the action list (inside a group page)."""
        row = Gtk.ListBoxRow()
        row.set_selectable(False)
        btn = Gtk.Button()
        btn.set_relief(Gtk.ReliefStyle.NONE)

        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(8)
        content.set_margin_end(8)

        img = self._safe_icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        name = Gtk.Label()
        name.set_markup(f"<b>{GLib.markup_escape_text(tr(label))}</b>")
        name.set_halign(Gtk.Align.START)
        d = Gtk.Label(label=tr(desc))
        d.set_halign(Gtk.Align.START)
        d.get_style_context().add_class("dim-label")
        text_box.pack_start(name, False, False, 0)
        text_box.pack_start(d, False, False, 0)

        arrow = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.BUTTON)

        content.pack_start(img, False, False, 0)
        content.pack_start(text_box, True, True, 0)
        content.pack_start(arrow, False, False, 0)
        btn.add(content)
        btn.connect("clicked", lambda _w: self._open_panel(action_id))
        row.add(btn)
        return row

    # ---- navigation ----
    def _open_panel(self, action_id):
        if action_id not in self._panels:
            panel = self._make_panel(action_id)
            self._panels[action_id] = panel
            self.stack.add_named(panel, action_id)
            panel.show_all()
        self.stack.set_visible_child_name(action_id)

    def _go_home(self):
        self.footer_label.set_markup(
            f"<span size='medium'>{tr('Active theme')}: "
            f"{GLib.markup_escape_text(core.get_active_theme() or '—')}</span>")
        self.stack.set_visible_child_name("dashboard")

    def _go_back_from_panel(self, action_id):
        """From an action panel, go back to the page of its group."""
        group_index = self._action_group.get(action_id)
        if group_index is not None:
            self.stack.set_visible_child_name(f"group-{group_index}")
        else:
            self._go_home()

    def _panel_shell(self, title, back_target=None):
        """Standard panel container: header with Back + content area.
        back_target: 'dashboard' or an action_id (to go back to the group
        that holds it). If None, the caller of the action panels works it out.
        """
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        bar.set_margin_top(12)
        bar.set_margin_start(12)
        bar.set_margin_bottom(12)
        back = Gtk.Button.new_with_label(tr("← Back"))
        if back_target == "dashboard":
            back.connect("clicked", lambda _w: self._go_home())
        else:
            # back_target is the action_id of the panel itself: go back to its group
            back.connect("clicked",
                        lambda _w: self._go_back_from_panel(back_target))
        bar.pack_start(back, False, False, 0)
        lbl = Gtk.Label()
        lbl.set_markup(f"<b>{GLib.markup_escape_text(tr(title))}</b>")
        bar.pack_start(lbl, False, False, 8)
        outer.pack_start(bar, False, False, 0)
        outer.pack_start(Gtk.Separator(), False, False, 0)
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        inner.set_margin_top(16)
        inner.set_margin_start(24)
        inner.set_margin_end(24)
        inner.set_margin_bottom(16)
        outer.pack_start(inner, True, True, 0)
        return outer, inner

    # ---- specific panels ----
    def _make_panel(self, action_id):
        builder = {
            "extract": self._panel_extract,
            "build": self._panel_build,
            "choose": self._panel_choose,
            "symbolic": self._panel_symbolic,
            "giants": self._panel_giants,
            "prefix": self._panel_prefix,
            "system": self._panel_system,
            "duplicates": self._panel_duplicates,
            "contact": self._panel_contact,
            "similar": self._panel_similar,
            "sizes": self._panel_sizes,
            "recolor": self._panel_recolor,
            "trim": self._panel_trim,
            "export": self._panel_export,
            "showcase": self._panel_showcase,
            "backup": self._panel_backup,
            "health": self._panel_health,
        }[action_id]
        return builder()

    def _status_label(self):
        lbl = Gtk.Label(label="")
        lbl.set_line_wrap(True)
        lbl.set_halign(Gtk.Align.START)
        return lbl

    def _panel_extract(self):
        outer, inner = self._panel_shell(tr("Extract icons from .ico / .exe / .dll / .icl"), back_target="extract")
        desc = Gtk.Label(label=tr("Choose one or more files: the icons inside will be "
                               "extracted as PNGs with transparency into ./extracted/."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)
        status = self._status_label()

        if not core.wrestool_available() and not core.icoextract_available():
            warn = Gtk.Label()
            warn.set_markup("<span foreground='red'>" + GLib.markup_escape_text(
                tr("⚠ Neither 'wrestool' nor 'icoextract' is installed. "
                   "Install: sudo apt install icoutils python3-icoextract")) + "</span>")
            inner.pack_start(warn, False, False, 0)

        def on_click(_w):
            files = pick_files(self, "Scegli file da cui estrarre")
            if not files:
                return
            status.set_text("Estrazione in corso...")

            def work():
                res = [core.extract_from_file(f) for f in files]
                tot = sum(r["png"] for r in res)
                return tot, res

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                tot, res = val
                via_ico = sum(1 for r in res if r.get("method") == "icoextract")
                extra = (" " + tr("({count} via icoextract)").format(count=via_ico)
                         if via_ico else "")
                status.set_text(
                    f"✔ {tot} PNG estratti da {len(res)} file. "
                    f"Cartella: ./extracted/" + extra)
            run_in_thread(work, done)

        btn = Gtk.Button.new_with_label(tr("Choose files and extract..."))
        btn.connect("clicked", on_click)
        inner.pack_start(btn, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_build(self):
        outer, inner = self._panel_shell(tr("Create / update theme"), back_target="build")
        status = self._status_label()

        # source
        src_row = Gtk.Box(spacing=8)
        src_lbl = Gtk.Label(label=tr("Icon source: (none)"))
        src_lbl.set_halign(Gtk.Align.START)
        self._build_src = None

        def choose_src(_w):
            p = pick_folder(self, "Cartella con le icone da aggiungere")
            if p:
                self._build_src = p
                src_lbl.set_text(f"Sorgente: {p}")
        src_btn = Gtk.Button.new_with_label(tr("Choose..."))
        src_btn.connect("clicked", choose_src)
        src_row.pack_start(src_lbl, True, True, 0)
        src_row.pack_start(src_btn, False, False, 0)
        inner.pack_start(src_row, False, False, 0)

        # theme name
        name_row = Gtk.Box(spacing=8)
        name_row.pack_start(Gtk.Label(label=tr("Theme name:")), False, False, 0)
        name_entry = Gtk.Entry()
        name_entry.set_text("byBias-Icons")
        name_row.pack_start(name_entry, True, True, 0)
        inner.pack_start(name_row, False, False, 0)

        # inherits
        inh_row = Gtk.Box(spacing=8)
        inh_row.pack_start(Gtk.Label(label=tr("Inherits from:")), False, False, 0)
        inh_combo = Gtk.ComboBoxText()
        for t in ["Mint-Y", "Mint-Y-Dark", "hicolor"] + core.list_themes():
            inh_combo.append_text(t)
        inh_combo.set_active(0)
        inh_row.pack_start(inh_combo, True, True, 0)
        inner.pack_start(inh_row, False, False, 0)

        clean_chk = Gtk.CheckButton(label="Bonifica nomi (spazi/underscore→-, accenti)")
        clean_chk.set_active(True)
        inner.pack_start(clean_chk, False, False, 0)

        def on_build(_w):
            if not self._build_src:
                info(self, "Scegli prima una cartella sorgente.")
                return
            theme_name = core.clean_name(name_entry.get_text()) or "byBias-Icons"
            inherits = inh_combo.get_active_text() or "Mint-Y"
            dest = core.ICONS_DIR / theme_name
            status.set_text("Costruzione tema in corso...")

            def work():
                import shutil
                dest.mkdir(parents=True, exist_ok=True)
                src = Path(self._build_src)
                if os.path.abspath(src) not in (os.path.abspath(dest),):
                    group = core.clean_name(src.name)
                    shutil.copytree(src, dest / group, dirs_exist_ok=True)
                if clean_chk.get_active():
                    core.normalize_names(dest)
                ndirs = core.build_index(dest, theme_name, inherits)
                ok, msg = core.update_cache(dest)
                return ndirs, ok, msg, theme_name

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                ndirs, ok, msg, tname = val
                mark = "✔" if ok else "⚠"
                status.set_text(f"{mark} Tema '{tname}': {ndirs} cartelle, cache: {msg}")
            run_in_thread(work, done)

        build_btn = Gtk.Button.new_with_label(tr("Build theme"))
        build_btn.connect("clicked", on_build)
        inner.pack_start(build_btn, False, False, 0)

        # activate
        def on_activate(_w):
            tname = core.clean_name(name_entry.get_text())
            if core.set_active_theme(tname):
                status.set_text(f"✔ Tema '{tname}' attivato.")
            else:
                status.set_markup("<span foreground='red'>Attivazione fallita.</span>")
        act_btn = Gtk.Button.new_with_label(tr("Activate this theme"))
        act_btn.connect("clicked", on_activate)
        inner.pack_start(act_btn, False, False, 0)

        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_choose(self):
        outer, inner = self._panel_shell(tr("Apply icon to a folder"), back_target="choose")
        status = self._status_label()
        if not HAVE_XAPP:
            warn = Gtk.Label()
            warn.set_markup("<span foreground='red'>⚠ XApp non disponibile: "
                            "il selettore con categorie richiede libxapp.</span>")
            inner.pack_start(warn, False, False, 0)

        desc = Gtk.Label(label=tr("Choose a destination folder, then an icon "
                               "from the byBias-Icons theme collection."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_choose(_w):
            target = pick_folder(self, "Cartella a cui applicare l'icona")
            if not target:
                return
            if not HAVE_XAPP:
                info(self, "Selettore non disponibile senza XApp.")
                return
            theme = core.ICONS_DIR / "byBias-Icons"
            if not theme.is_dir():
                info(self, tr("The byBias-Icons theme was not found in "
                              "~/.local/share/icons: build it first with "
                              "\"Create / update theme\"."))
                return
            # XApp custom categories show icon NAMES from the current icon
            # theme, not file paths (with paths they stay empty). So, only
            # while the chooser is open, the app uses byBias-Icons as its icon
            # theme; the chosen name is then mapped back to its file.
            settings = Gtk.Settings.get_default()
            old_theme = settings.get_property("gtk-icon-theme-name")
            settings.set_property("gtk-icon-theme-name", theme.name)
            paths = {}
            icon = None
            try:
                dlg = XApp.IconChooserDialog()
                dlg.set_property("allow-paths", True)
                for folder in sorted(os.listdir(theme)):
                    p = theme / folder
                    if p.is_dir():
                        names = []
                        for f in core.collect_icons(p):
                            stem = os.path.splitext(os.path.basename(f))[0]
                            if stem not in paths:   # first file wins on duplicates
                                paths[stem] = f
                                names.append(stem)
                        if names:
                            dlg.add_custom_category(core.category_label(folder), names)
                resp = dlg.run()
                icon = dlg.get_icon_string() if resp == Gtk.ResponseType.OK else None
                dlg.destroy()
                if icon:
                    icon = paths.get(icon, icon)
                    if not icon.startswith(("/", "file://")):
                        # a name from the standard categories: resolve to a file
                        found = Gtk.IconTheme.get_default().lookup_icon(icon, 256, 0)
                        if found and found.get_filename():
                            icon = found.get_filename()
            finally:
                settings.set_property("gtk-icon-theme-name", old_theme)
            if icon and core.apply_icon_to(target, icon):
                status.set_text(f"✔ Icona applicata a {target}")
            elif icon:
                status.set_markup("<span foreground='red'>Applicazione fallita.</span>")

        btn = Gtk.Button.new_with_label(tr("Choose folder and icon..."))
        btn.connect("clicked", on_choose)
        inner.pack_start(btn, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_symbolic(self):
        outer, inner = self._panel_shell(tr("Generate symbolic icons"), back_target="symbolic")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Choose PNGs: their symbolic 16×16 monochrome "
                               "SVG versions will be generated."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        cov_row = Gtk.Box(spacing=8)
        cov_row.pack_start(Gtk.Label(label=tr("Coverage:")), False, False, 0)
        cov = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.2, 0.7, 0.01)
        cov.set_value(0.42)
        cov.set_hexpand(True)
        cov_row.pack_start(cov, True, True, 0)
        inner.pack_start(cov_row, False, False, 0)

        def on_click(_w):
            files = pick_files(self, "Scegli PNG da convertire")
            if not files:
                return
            coverage = cov.get_value()
            status.set_text("Generazione in corso...")

            def work():
                done_n = 0
                for f in files:
                    if core.make_symbolic(f, coverage=coverage):
                        done_n += 1
                return done_n, len(files)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                n, tot = val
                status.set_text(f"✔ {n}/{tot} icone simboliche generate "
                                "(accanto ai PNG originali).")
            run_in_thread(work, done)

        btn = Gtk.Button.new_with_label(tr("Choose PNGs and generate..."))
        btn.connect("clicked", on_click)
        inner.pack_start(btn, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_giants(self):
        outer, inner = self._panel_shell(tr("Hunt the giants (collisions)"), back_target="giants")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Scans the byBias-Icons theme for files that hijack "
                               "system names (the cause of giant icons/triangles)."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        self._giants_found = []

        def on_report(_w):
            theme = core.ICONS_DIR / "byBias-Icons"
            if not theme.is_dir():
                info(self, "Tema byBias-Icons non trovato.")
                return
            status.set_text("Analisi in corso...")

            def work():
                return core.find_collisions(str(theme))

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                self._giants_found = val
                if not val:
                    status.set_text("✔ Nessuna collisione: niente giganti.")
                else:
                    status.set_text(f"⚠ {len(val)} file scippano nomi di sistema. "
                                    "Premi 'Disinnesca' per prefissarli.")
            run_in_thread(work, done)

        def on_defuse(_w):
            if not self._giants_found:
                info(self, "Esegui prima l'analisi.")
                return
            n = core.defuse_collisions(self._giants_found)
            theme = core.ICONS_DIR / "byBias-Icons"
            core.build_index(theme)
            core.update_cache(theme)
            self._giants_found = []
            status.set_text(f"✔ {n} file disinnescati, tema rigenerato.")

        rep = Gtk.Button.new_with_label(tr("Scan (report)"))
        rep.connect("clicked", on_report)
        inner.pack_start(rep, False, False, 0)
        dfz = Gtk.Button.new_with_label(tr("Defuse the culprits"))
        dfz.connect("clicked", on_defuse)
        inner.pack_start(dfz, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_prefix(self):
        outer, inner = self._panel_shell(tr("Prefix everything (zero substitutions)"), back_target="prefix")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Adds the 'bybias-' prefix to ALL icons in the "
                               "theme: none of them substitutes a system icon anymore.\n"
                               "The collection stays pickable by hand from the chooser."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_prefix(_w):
            theme = core.ICONS_DIR / "byBias-Icons"
            if not theme.is_dir():
                info(self, "Tema byBias-Icons non trovato.")
                return
            status.set_text("Prefisso in corso...")

            def work():
                n = core.prefix_all(str(theme))
                core.build_index(theme)
                ok, msg = core.update_cache(theme)
                return n, ok, msg

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                n, ok, msg = val
                status.set_text(f"✔ {n} icone prefissate, tema rigenerato ({msg}).")
            run_in_thread(work, done)

        btn = Gtk.Button.new_with_label(tr("Prefix all icons"))
        btn.connect("clicked", on_prefix)
        inner.pack_start(btn, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_system(self):
        outer, inner = self._panel_shell(tr("Replace system icons"), back_target="system")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Choose a system slot (e.g. Full trash) "
                               "and one of your images: it will be installed under the "
                               "standard name, replacing the system icon everywhere."))
        desc.set_line_wrap(True)
        desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        # drop-down menu with the system slots
        slot_row = Gtk.Box(spacing=8)
        slot_row.pack_start(Gtk.Label(label=tr("Slot:")), False, False, 0)
        slot_combo = Gtk.ComboBoxText()
        slots = core.system_slots()
        for name, label in slots:
            slot_combo.append(name, f"{label}  ({name})")
        slot_combo.set_active(1)  # default: user-trash-full
        slot_row.pack_start(slot_combo, True, True, 0)
        inner.pack_start(slot_row, False, False, 0)

        # chosen image
        self._sys_image = None
        img_row = Gtk.Box(spacing=8)
        img_lbl = Gtk.Label(label=tr("Image: (none)"))
        img_lbl.set_halign(Gtk.Align.START)

        def choose_img(_w):
            files = pick_files(self, "Scegli l'immagine (PNG o SVG)")
            if files:
                self._sys_image = files[0]
                img_lbl.set_text(f"Immagine: {os.path.basename(files[0])}")
        img_btn = Gtk.Button.new_with_label(tr("Choose..."))
        img_btn.connect("clicked", choose_img)
        img_row.pack_start(img_lbl, True, True, 0)
        img_row.pack_start(img_btn, False, False, 0)
        inner.pack_start(img_row, False, False, 0)

        hint = Gtk.Label()
        hint.set_markup(f"<span size='medium'>"
                        f"{tr('Tip: for the trash bin, install <b>both</b> slots ')}"
                        f"{tr('(full and empty) for a consistent result.')}"
                        f"</span>")
        hint.get_style_context().add_class("ip-dim")
        hint.set_line_wrap(True)
        hint.set_halign(Gtk.Align.START)
        inner.pack_start(hint, False, False, 0)

        def on_install(_w):
            if not self._sys_image:
                info(self, "Scegli prima un'immagine.")
                return
            slot = slot_combo.get_active_id()
            theme = core.ICONS_DIR / "byBias-Icons"
            if not theme.is_dir():
                info(self, "Tema byBias-Icons non trovato. Crealo prima "
                           "dalla sezione 'Crea / aggiorna tema'.")
                return
            status.set_text("Installazione in corso...")

            def work():
                dest = core.install_system_icon(theme, slot, self._sys_image)
                core.build_index(theme)
                ok, msg = core.update_cache(theme)
                return slot, dest, ok, msg

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                slot, dest, ok, msg = val
                status.set_text(f"✔ '{slot}' installata. Tema rigenerato ({msg}).\n"
                                "Riavvia Nemo (nemo -q) per vedere il cambiamento.")
            run_in_thread(work, done)

        install_btn = Gtk.Button.new_with_label(tr("Install as system icon"))
        install_btn.connect("clicked", on_install)
        inner.pack_start(install_btn, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    # ===== Helpers for the "action on the theme" panels =====
    def _theme_or_warn(self):
        theme = core.ICONS_DIR / "byBias-Icons"
        if not theme.is_dir():
            info(self, "Tema byBias-Icons non trovato. Crealo prima dalla "
                       "sezione 'Crea / aggiorna tema'.")
            return None
        return theme

    # ---- Maintenance ----
    def _panel_duplicates(self):
        outer, inner = self._panel_shell(tr("Find duplicates (by content)"), back_target="duplicates")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Finds identical icons saved under different names, "
                               "comparing content (hash), not the name."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)
        self._dup_groups = []

        def on_scan(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            status.set_text("Analisi in corso...")

            def work():
                return core.find_duplicates(theme)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                self._dup_groups = val
                if not val:
                    status.set_text("✔ Nessun duplicato trovato.")
                else:
                    tot = sum(len(g) - 1 for g in val)
                    status.set_text(f"⚠ {len(val)} gruppi di duplicati "
                                    f"({tot} file ridondanti). "
                                    "Premi 'Rimuovi' per tenerne uno per gruppo.")
            run_in_thread(work, done)

        def on_remove(_w):
            if not self._dup_groups:
                info(self, "Esegui prima l'analisi.")
                return
            n = core.remove_duplicates(self._dup_groups)
            self._dup_groups = []
            status.set_text(f"✔ {n} duplicati rimossi (un file conservato per gruppo).")

        b1 = Gtk.Button.new_with_label(tr("Scan"))
        b1.connect("clicked", on_scan)
        inner.pack_start(b1, False, False, 0)
        b2 = Gtk.Button.new_with_label(tr("Remove redundant ones"))
        b2.connect("clicked", on_remove)
        inner.pack_start(b2, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_contact(self):
        outer, inner = self._panel_shell(tr("Contact sheet (mosaic)"), back_target="contact")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Generates a PNG with the whole collection in a grid, "
                               "the name under each icon. Handy for a quick overview."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            out = Path.home() / "byBias-Icons-contact.png"
            status.set_text("Generazione in corso...")

            def work():
                return core.contact_sheet(theme, out)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                path, n = val
                status.set_text(f"✔ Contact sheet con {n} icone salvato in:\n{path}")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Generate contact sheet"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_similar(self):
        outer, inner = self._panel_shell(tr("Find similar (by colour)"), back_target="similar")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Choose a reference icon: finds the ones in the "
                               "collection graphically closest by colour."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            files = pick_files(self, "Icona di riferimento")
            if not files:
                return
            status.set_text("Ricerca in corso...")

            def work():
                return core.find_similar(files[0], theme, top=12)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                lines = "\n".join(f"  • {os.path.basename(p)}  (dist {d})"
                                  for p, d in val[:12])
                status.set_text(f"Icone più simili:\n{lines}")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Choose reference and search"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    # ---- Production ----
    def _panel_sizes(self):
        outer, inner = self._panel_shell(tr("Normalize sizes (16 → 256)"), back_target="sizes")
        status = self._status_label()
        desc = Gtk.Label(label=tr("From a PNG (even oversized) generates the full "
                               "set of standard sizes, properly resized."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            files = pick_files(self, "Scegli PNG da normalizzare")
            if not files:
                return
            status.set_text("Generazione in corso...")

            def work():
                tot = 0
                for f in files:
                    tot += len(core.normalize_sizes(f))
                return tot, len(files)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                tot, nf = val
                status.set_text(f"✔ {tot} file generati da {nf} icone "
                                "(in cartelle '<nome>-sizes').")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Choose PNGs and normalize"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_recolor(self):
        outer, inner = self._panel_shell(tr("Recolor / invert"), back_target="recolor")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Applies a tint to monochrome icons, or inverts "
                               "light↔dark to fit an opposite theme."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        color_row = Gtk.Box(spacing=8)
        color_row.pack_start(Gtk.Label(label=tr("Tint:")), False, False, 0)
        color_btn = Gtk.ColorButton()
        color_row.pack_start(color_btn, False, False, 0)
        inner.pack_start(color_row, False, False, 0)

        def on_recolor(_w):
            files = pick_files(self, "Scegli PNG da ricolorare")
            if not files:
                return
            rgba = color_btn.get_rgba()
            hex_col = "#%02x%02x%02x" % (int(rgba.red*255),
                                         int(rgba.green*255), int(rgba.blue*255))
            status.set_text("Ricolorazione in corso...")

            def work():
                for f in files:
                    core.recolor(f, hex_col)
                return len(files), hex_col

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                n, hc = val
                status.set_text(f"✔ {n} icone ricolorate in {hc}.")
            run_in_thread(work, done)

        def on_invert(_w):
            files = pick_files(self, "Scegli PNG da invertire")
            if not files:
                return

            def work():
                for f in files:
                    core.invert_light_dark(f)
                return len(files)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                status.set_text(f"✔ {val} icone invertite chiaro↔scuro.")
            run_in_thread(work, done)

        b1 = Gtk.Button.new_with_label(tr("Recolor with the chosen tint"))
        b1.connect("clicked", on_recolor)
        inner.pack_start(b1, False, False, 0)
        b2 = Gtk.Button.new_with_label(tr("Invert light↔dark"))
        b2.connect("clicked", on_invert)
        inner.pack_start(b2, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_trim(self):
        outer, inner = self._panel_shell(tr("Trim & center"), back_target="trim")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Removes transparent margins, recenters the icon "
                               "and applies uniform padding: makes mixed sets more coherent."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            files = pick_files(self, "Scegli PNG da rifilare")
            if not files:
                return
            status.set_text("Elaborazione in corso...")

            def work():
                for f in files:
                    core.trim_and_pad(f)
                return len(files)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                status.set_text(f"✔ {val} icone rifilate e ricentrate.")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Choose PNGs and trim"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    # ---- Distribution ----
    def _panel_export(self):
        outer, inner = self._panel_shell(tr("Export theme package"), back_target="export")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Creates a zip ready for publishing: the theme "
                               "plus an auto-generated LICENSE and README."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            status.set_text("Creazione pacchetto...")

            def work():
                return core.export_theme_package(theme)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                status.set_text(f"✔ Pacchetto creato:\n{val}")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Export zip"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    def _panel_showcase(self):
        outer, inner = self._panel_shell(tr("Make showcase"), back_target="showcase")
        status = self._status_label()
        desc = Gtk.Label(label=tr("A promotional image: a selection of icons "
                               "arranged on a background, for the download page."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        def on_go(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            out = Path.home() / "byBias-Icons-showcase.png"
            status.set_text("Generazione in corso...")

            def work():
                return core.make_showcase(theme, out)

            def done(result):
                kind, val = result
                if kind == "err":
                    status.set_markup(f"<span foreground='red'>Errore: "
                                f"{GLib.markup_escape_text(str(val))}</span>")
                    return
                path, n = val
                status.set_text(f"✔ Showcase con {n} icone salvato in:\n{path}")
            run_in_thread(work, done)

        b = Gtk.Button.new_with_label(tr("Generate showcase"))
        b.connect("clicked", on_go)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer

    # ---- Safety & convenience ----
    def _panel_backup(self):
        outer, inner = self._panel_shell(tr("Backup / restore"), back_target="backup")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Saves a snapshot of the theme before major "
                               "changes, and restores it if needed."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        combo = Gtk.ComboBoxText()

        def refresh_list():
            combo.remove_all()
            for b in core.list_backups("byBias-Icons"):
                combo.append(b, os.path.basename(b))
            if combo.get_model().iter_n_children(None):
                combo.set_active(0)

        def on_backup(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            dest = core.backup_theme(theme)
            refresh_list()
            status.set_text(f"✔ Backup creato:\n{dest}")

        def on_restore(_w):
            zip_path = combo.get_active_id()
            if not zip_path:
                info(self, "Nessun backup selezionato.")
                return
            theme = core.ICONS_DIR / "byBias-Icons"
            core.restore_backup(zip_path, theme)
            core.update_cache(theme)
            status.set_text("✔ Tema ripristinato dal backup. Riavvia Nemo (nemo -q).")

        b1 = Gtk.Button.new_with_label(tr("Create backup now"))
        b1.connect("clicked", on_backup)
        inner.pack_start(b1, False, False, 0)
        inner.pack_start(Gtk.Label(label=tr("Available backups:")), False, False, 0)
        inner.pack_start(combo, False, False, 0)
        b2 = Gtk.Button.new_with_label(tr("Restore the selected backup"))
        b2.connect("clicked", on_restore)
        inner.pack_start(b2, False, False, 0)
        inner.pack_start(status, False, False, 0)
        refresh_list()
        return outer

    def _panel_health(self):
        outer, inner = self._panel_shell(tr("Theme health-check"), back_target="health")
        status = self._status_label()
        desc = Gtk.Label(label=tr("Diagnoses the theme against the checklist: "
                               "inheritance, accents, collisions, cache, names."))
        desc.set_line_wrap(True); desc.set_halign(Gtk.Align.START)
        inner.pack_start(desc, False, False, 0)

        result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        inner.pack_start(result_box, False, False, 0)

        def on_check(_w):
            theme = self._theme_or_warn()
            if not theme:
                return
            for child in result_box.get_children():
                result_box.remove(child)
            for esito, msg in core.health_check(theme):
                icon = {"ok": "✔", "warn": "⚠", "err": "✘"}[esito]
                color = {"ok": "#2a2", "warn": "#c80", "err": "#c00"}[esito]
                lbl = Gtk.Label()
                lbl.set_markup(f"<span foreground='{color}'>{icon}</span> "
                       f"{GLib.markup_escape_text(msg)}")
                lbl.set_line_wrap(True)
                lbl.set_halign(Gtk.Align.START)
                result_box.pack_start(lbl, False, False, 0)
            result_box.show_all()

        b = Gtk.Button.new_with_label(tr("Run diagnostics"))
        b.connect("clicked", on_check)
        inner.pack_start(b, False, False, 0)
        inner.pack_start(status, False, False, 0)
        return outer


def _load_css():
    """Apply a CSS with APPLICATION priority: it beats the rules of the
    active GTK theme for the .ip-dim class, which Pango foreground=
    markup alone could not override (the theme overwrote it)."""
    css = b"""
    .ip-dim {
        color: #aaaaaa;
    }
    """
    provider = Gtk.CssProvider()
    provider.load_from_data(css)
    screen = Gdk.Screen.get_default()
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def main():
    _load_css()
    # WM_CLASS must match the name of the .desktop file (icons-packet.desktop)
    # so that the Cinnamon panel associates the right icon.
    GLib.set_prgname("icons-packet")
    GLib.set_application_name(APP_NAME)

    # default icon for ALL the app's windows (also used
    # in alt-tab and as fallback by the panel)
    here = Path(__file__).resolve().parent
    for name in ("icon/icons-packet-256.png", "icon/icons-packet.svg"):
        p = here / name
        if p.exists():
            try:
                Gtk.Window.set_default_icon_from_file(str(p))
                break
            except Exception:
                continue

    win = IconsPacketWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
