#!/bin/bash

# Synthwave84 Terminal Theme Installer
# Automatically installs theme for detected terminals

set -e

THEME_DIR="$(cd "$(dirname "$0")" && pwd)/terminal"
CONFIG_DIR="$HOME/.config"

echo "🌊 Synthwave84 Terminal Theme Installer"
echo "======================================"

# Detect and install for Alacritty
if command -v alacritty &> /dev/null; then
    echo "📦 Installing for Alacritty..."
    mkdir -p "$CONFIG_DIR/alacritty"
    if [ -f "$CONFIG_DIR/alacritty/alacritty.yml" ]; then
        echo "⚠️  Backing up existing alacritty.yml..."
        cp "$CONFIG_DIR/alacritty/alacritty.yml" "$CONFIG_DIR/alacritty/alacritty.yml.backup"
    fi
    echo -e "\n# Synthwave84 Theme\n[colors]" >> "$CONFIG_DIR/alacritty/alacritty.yml"
    cat "$THEME_DIR/synthwave84.toml" | grep -A 100 "^\\[colors\\]" >> "$CONFIG_DIR/alacritty/alacritty.yml"
    echo "✅ Alacritty theme installed"
fi

# Detect and install for Kitty
if command -v kitty &> /dev/null; then
    echo "📦 Installing for Kitty..."
    mkdir -p "$CONFIG_DIR/kitty/themes"
    cp "$THEME_DIR/synthwave84.conf" "$CONFIG_DIR/kitty/themes/"
    
    if ! grep -q "include themes/synthwave84.conf" "$CONFIG_DIR/kitty/kitty.conf" 2>/dev/null; then
        echo "include themes/synthwave84.conf" >> "$CONFIG_DIR/kitty/kitty.conf"
    fi
    
    # Reload if kitty is running
    if pgrep -x "kitty" > /dev/null; then
        kitty @ set-colors "$CONFIG_DIR/kitty/themes/synthwave84.conf" 2>/dev/null || true
    fi
    echo "✅ Kitty theme installed"
fi

# Detect and install for Wezterm
if command -v wezterm &> /dev/null; then
    echo "📦 Installing for Wezterm..."
    mkdir -p "$CONFIG_DIR/wezterm"
    echo "-- Add to your wezterm.lua:" > "$CONFIG_DIR/wezterm/synthwave84-setup.lua"
    echo "-- local synthwave84 = require('synthwave84')" >> "$CONFIG_DIR/wezterm/synthwave84-setup.lua"
    echo "-- config.color_scheme = 'Synthwave84'" >> "$CONFIG_DIR/wezterm/synthwave84-setup.lua"
    echo "⚠️  Manual setup required for Wezterm - see $CONFIG_DIR/wezterm/synthwave84-setup.lua"
fi

echo ""
echo "🎉 Installation complete!"
echo "💡 Restart your terminal or reload config to see changes"
echo "🔧 For manual installation, see README.md"