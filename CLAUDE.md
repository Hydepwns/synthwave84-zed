# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Synthwave '84 is a color theme extension for the Zed editor with three variants: Classic, Soft, and High Contrast.

## Architecture

**Source files** (edit these):
- `src/base.json` - Theme structure, UI templates with `{{color}}` placeholders, syntax token-to-color mappings
- `palette.json` - All color definitions organized by variant

**Generated** (do not edit directly):
- `themes/synthwave84.json` - Built from source files via `make generate`

## Commands

```bash
make generate   # Build theme from source
make validate   # Check structure and WCAG contrast ratios
make check      # Verify theme matches source (CI uses this)
make derive     # Show programmatically derived variant colors
make coverage   # Check Zed syntax token coverage
make all        # generate + validate
```

To apply derived colors: `python3 scripts/theme.py derive --apply`

## Pre-commit Hook

```bash
git config core.hooksPath .githooks
```

Auto-regenerates theme when `src/base.json` or `palette.json` change.

## Color System

`palette.json` structure:
- `base` - Shared backgrounds, borders, foreground (used by all variants)
- `syntax` - Token colors for Classic variant
- `variants.soft` / `variants.high_contrast` - Color overrides per variant

Variant derivation uses WCAG contrast targeting:
- Soft: +6L lightness shift, 4.5:1 minimum contrast
- High Contrast: -8L lightness shift, 7.0:1 minimum contrast

## Syntax Token Mapping

In `src/base.json`, the `syntax_colors` object maps tokens to palette keys:

| Palette Key | Color   | Tokens (examples)                    |
|-------------|---------|--------------------------------------|
| function    | cyan    | function, constructor, title         |
| keyword     | yellow  | keyword, operator, attribute         |
| string      | orange  | string, text.literal                 |
| type        | pink    | type, enum, variable, tag            |
| constant    | coral   | constant, boolean, number            |
| comment     | muted   | comment, markup.quote                |
| success     | mint    | support.class, string.escape         |
| info        | blue    | hint, link_text                      |
| error       | red     | keyword.other.unsafe                 |
| foreground  | white   | punctuation, embedded, source.*      |

Font styles are defined separately in `syntax_styles` (italic, bold, underline).
