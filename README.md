# Synthwave '84 for Zed

A vibrant, retro-inspired theme for the Zed editor based on the synthwave aesthetic of the 1980s.
Inspired by the music and cover artwork of modern Synthwave bands like FM-84, Timecop 1983, and The Midnight.

## Quick Start

1. **Install from Zed Extensions** (Recommended)
   - Open Zed > Command Palette (`Cmd/Ctrl + Shift + P`)
   - Search "zed: Extensions" > Search "Synthwave 84" > Install

2. **Apply the theme**
   - Open Settings (`Cmd/Ctrl + ,`)
   - Set `"theme": "Synthwave84"`

3. **Choose your variant**
   - `"Synthwave84"` - Classic vibrant experience
   - `"Synthwave84 Soft"` - Lower contrast for extended coding
   - `"Synthwave84 High Contrast"` - Enhanced visibility

![Theme Preview](preview_synthwave84.png)
![Theme Preview](preview_high_contrast.png)
![Theme Preview](preview_soft.png)

## Features

- Dark synthwave-inspired color palette
- Neon-like syntax highlighting with vibrant purples, pinks, and cyans
- Carefully crafted contrast for comfortable long coding sessions
- Retro-futuristic UI elements
- AI/LLM support for predictive text and inline completions
- Language-specific optimizations for 15+ languages
- Monaspace variable font support
- Three theme variants:
  - **Synthwave84** - The classic vibrant synthwave experience
  - **Synthwave84 Soft** - Lower contrast for extended coding sessions
  - **Synthwave84 High Contrast** - Enhanced visibility with more vibrant colors

### Terminal Support

The Zed built-in terminal automatically inherits the Synthwave '84 colors. For external terminals, check out the [Synthwave '84 Terminal](https://github.com/hydepwns/synthwave84-terminal) repository for matching color schemes.

## Installation

### From Zed Extensions

1. Open Zed
2. Open the command palette (`Cmd/Ctrl + Shift + P`)
3. Search for "zed: Extensions"
4. Search for "Synthwave 84"
5. Click "Install"

### Manual Installation

1. Clone this repository or download the files
2. Copy the entire folder to `~/.config/zed/extensions/synthwave84`
3. Restart Zed
4. Open settings (`Cmd/Ctrl + ,`)
5. Add the following to your settings.json:

```json
{
  "theme": "Synthwave84"
}
```

## Recommended Font Configuration

### Monaspace Variable Fonts

This theme is optimized for use with the [Monaspace](https://monaspace.githubnext.com/) font family. Monaspace offers five unique variants, each with variable weight, width, and slant axes:

- **Monaspace Neon** - Neo-grotesque sans (clean and modern)
- **Monaspace Argon** - Humanist sans (friendly and readable)
- **Monaspace Xenon** - Slab serif (structured and bold)
- **Monaspace Radon** - Handwriting (expressive and unique)
- **Monaspace Krypton** - Mechanical sans (technical and precise)

#### Recommended Settings

Add to your Zed settings.json:

```json
{
  "buffer_font_family": "Monaspace Neon",
  "buffer_font_features": {
    "calt": true, // Contextual alternates (texture healing)
    "liga": true, // Ligatures
    "ss01": true, // Style set 1 (varies by font)
    "ss02": true, // Style set 2 (varies by font)
    "ss03": true, // Style set 3 (varies by font)
    "ss04": true, // Style set 4 (varies by font)
    "ss05": true, // Style set 5 (varies by font)
    "ss06": true, // Style set 6 (varies by font)
    "ss07": true, // Style set 7 (varies by font)
    "ss08": true // Style set 8 (varies by font)
  },
  "buffer_font_weight": 400,
  "buffer_font_size": 14,
  "ui_font_family": "Monaspace Argon",
  "ui_font_size": 14
}
```

#### Variable Font Axes

You can customize the font appearance using variable axes:

```json
{
  "buffer_font_weight": 300, // 200-800 (Light to Extra Bold)
  "buffer_font_features": {
    "wdth": 100, // Width: 100-125 (Normal to Wide)
    "slnt": -12 // Slant: 0 to -12 (Upright to Italic)
  }
}
```

#### Font Pairing Suggestions

- **General Coding**: Monaspace Neon (buffer) + Monaspace Argon (UI)
- **Data Science/Notebooks**: Monaspace Xenon (buffer) + Monaspace Neon (UI)
- **Creative Coding**: Monaspace Radon (buffer) + Monaspace Krypton (UI)
- **Systems Programming**: Monaspace Krypton (buffer) + Monaspace Argon (UI)

### Alternative Font Options

If you prefer other fonts, the theme also works well with:

- JetBrains Mono
- Fira Code
- Cascadia Code
- Victor Mono (for italic emphasis)

## Color Palette

See [COLORS.md](COLORS.md) for the complete color palette reference.

## Accessibility

- **WCAG AA Compliant**: All text meets contrast ratio requirements (4.5:1+)
- **High Contrast Variant**: Enhanced visibility with 7:1+ contrast ratios
- **Color Blind Friendly**: Tested with deuteranopia and protanopia simulators
- **Reduced Motion**: No animations, suitable for vestibular sensitivity

## Troubleshooting

### Theme not appearing in Zed

- Ensure you're using the exact theme names: `"Synthwave84"`, `"Synthwave84 Soft"`, `"Synthwave84 High Contrast"`
- Restart Zed after installation
- Check that the extension is enabled in Extensions panel

### Colors look different than expected

- Verify your monitor's color profile and brightness settings
- Some terminals may not support true color - use Zed's built-in terminal
- Update to the latest Zed version for best compatibility

### Installation issues

- **Linux/NixOS**: Ensure `~/.config/zed/extensions/` directory exists and is writable
- **Permission errors**: Run `chmod -R 755 ~/.config/zed/extensions/synthwave84`
- **Manual installation**: Copy the entire theme folder, not just individual files

### Font rendering issues

- Install [Monaspace fonts](https://monaspace.githubnext.com/) for optimal experience
- Enable font features in settings: `"liga": true, "calt": true`
- Clear font cache if using custom fonts: `fc-cache -f -v` (Linux)

## Development

Theme is generated from source files:

```bash
make generate   # Build theme from src/base.json + palette.json
make validate   # Check WCAG contrast ratios
make check      # Verify theme matches source
```

See [CLAUDE.md](CLAUDE.md) for architecture details.

## License

[MIT License](LICENSE)

## Credits

- Original Synthwave '84 concept by [Robb Owen](https://github.com/robb0wen/synthwave-vscode)
- Ported to Zed by DROO
