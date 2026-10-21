#!/usr/bin/env bash
##########################################################
##                 byBias Icons Packet                  ##
##            Installer for the current user            ##
##                   written in Bash                    ##
##                          🌞                          ##
##       by FranzBias 2026 · github.com/FranzBias       ##
##            Licensed under the MIT License            ##
##          See LICENSE file for full license.          ##
##########################################################
# SPDX-License-Identifier: MIT
#############################################################
#  install.sh — installs Icons-Packet 📦🦉
#
#  Copies the app to ~/.local/share/icons-packet/, installs the
#  .desktop file (so it shows up in the menu and the panel
#  shows the right icon) and registers the icon in the hicolor theme.
#
#  Usage:      bash install.sh
#  Uninstall:  bash install.sh --uninstall
#############################################################
set -Eeuo pipefail

APP_DIR="$HOME/.local/share/icons-packet"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_HICOLOR="$HOME/.local/share/icons/hicolor"
SRC="$(cd "$(dirname "$0")" && pwd)"

uninstall() {
    echo "Uninstalling Icons-Packet..."
    rm -rf "$APP_DIR"
    rm -f "$DESKTOP_DIR/icons-packet.desktop"
    for size in 16 24 32 48 64 128 256; do
        rm -f "$ICON_HICOLOR/${size}x${size}/apps/icons-packet.png"
    done
    rm -f "$ICON_HICOLOR/scalable/apps/icons-packet.svg"
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    gtk-update-icon-cache -f "$ICON_HICOLOR" 2>/dev/null || true
    echo "✔ Uninstalled."
    exit 0
}

[ "${1:-}" = "--uninstall" ] && uninstall

echo "Installing Icons-Packet in $APP_DIR ..."
mkdir -p "$APP_DIR" "$DESKTOP_DIR"

# 1. copy the app files
cp -r "$SRC/icons_packet_core.py" "$SRC/icons_packet_gui.py" "$SRC/icons_packet_i18n.py" \
      "$SRC/icons-packet" "$SRC/icon" "$APP_DIR/"
chmod +x "$APP_DIR/icons-packet"

# 2. register the icon in the hicolor theme (so the system finds it by name)
for size in 16 24 32 48 64 128 256; do
    dest="$ICON_HICOLOR/${size}x${size}/apps"
    mkdir -p "$dest"
    cp "$SRC/icon/icons-packet-${size}.png" "$dest/icons-packet.png"
done
mkdir -p "$ICON_HICOLOR/scalable/apps"
cp "$SRC/icons-packet.svg" "$ICON_HICOLOR/scalable/apps/icons-packet.svg"

# 3. install the .desktop file, with the right paths for THIS user
cat > "$DESKTOP_DIR/icons-packet.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Icons-Packet
Comment=Manage a personal icon collection on Cinnamon
Comment[it]=Gestisci una collezione personale di icone su Cinnamon
Exec=python3 $APP_DIR/icons-packet
Icon=icons-packet
Terminal=false
Categories=Utility;Graphics;
Keywords=icons;theme;cinnamon;bybias;
StartupWMClass=icons-packet
EOF

# 4. update the databases
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache -f "$ICON_HICOLOR" 2>/dev/null || true

echo ""
echo "✔ Installed!"
echo "  App:     $APP_DIR"
echo "  Menu:    Icons-Packet (Accessories/Graphics category)"
echo ""
echo "Note: if an instance was already open, close it and reopen it from the menu"
echo "so that the panel shows the right icon."
