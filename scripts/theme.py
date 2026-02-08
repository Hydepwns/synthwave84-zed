#!/usr/bin/env python3
"""Synthwave84 theme management CLI.

Usage:
  python scripts/theme.py generate    # Build theme from source
  python scripts/theme.py validate    # Check theme structure and accessibility
  python scripts/theme.py check       # Verify theme matches source
  python scripts/theme.py derive      # Show programmatically derived colors
  python scripts/theme.py coverage    # Check Zed token coverage
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parent.parent
VARIANT_KEYS = ("classic", "soft", "high_contrast")


# --- Result Type ---


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str

    @staticmethod
    def success(msg: str) -> "Result":
        return Result(True, f"OK: {msg}")

    @staticmethod
    def failure(msg: str) -> "Result":
        return Result(False, f"FAIL: {msg}")


# --- File Loading ---


load_json = lambda p: json.loads(p.read_text())
load_base = lambda: load_json(ROOT / "src" / "base.json")
load_palette = lambda: load_json(ROOT / "palette.json")
load_theme = lambda: load_json(ROOT / "themes" / "synthwave84.json")


# --- Color Utilities ---


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")[:6]
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def hex_to_hsl(hex_color: str) -> tuple[float, float, float]:
    r, g, b = (c / 255 for c in hex_to_rgb(hex_color))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2

    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return (h * 360, s * 100, l * 100)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    h, s, l = h / 360, s / 100, l / 100

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q

        def hue2rgb(t):
            t = t % 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        r, g, b = hue2rgb(h + 1/3), hue2rgb(h), hue2rgb(h - 1/3)

    return rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))


def luminance(rgb: tuple[int, int, int]) -> float:
    channel = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c / 255) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = luminance(hex_to_rgb(c1)), luminance(hex_to_rgb(c2))
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def adjust_lightness(hex_color: str, delta: float) -> str:
    """Adjust lightness by delta (-100 to +100)."""
    h, s, l = hex_to_hsl(hex_color)
    return hsl_to_hex(h, s, max(0, min(100, l + delta)))


def ensure_contrast(fg: str, bg: str, min_ratio: float = 4.5, direction: str = "auto") -> str:
    """Adjust foreground color to meet minimum contrast ratio against background.

    direction: 'lighter', 'darker', or 'auto' (picks based on bg luminance)
    """
    if contrast_ratio(fg, bg) >= min_ratio:
        return fg

    h, s, l = hex_to_hsl(fg)
    bg_lum = luminance(hex_to_rgb(bg))

    # Determine direction: lighten if bg is dark, darken if bg is light
    go_lighter = direction == "lighter" or (direction == "auto" and bg_lum < 0.5)
    step = 1 if go_lighter else -1

    for _ in range(100):
        l = max(0, min(100, l + step))
        candidate = hsl_to_hex(h, s, l)
        if contrast_ratio(candidate, bg) >= min_ratio:
            return candidate

    return hsl_to_hex(h, s, l)


# Variant adjustment parameters
VARIANT_ADJUSTMENTS = {
    "soft": {"lightness_delta": 6, "target_contrast": 4.5},
    "high_contrast": {"lightness_delta": -8, "target_contrast": 7.0},
}


def derive_variant_color(base_color: str, bg_color: str, variant: str) -> str:
    """Derive a variant color from base, ensuring WCAG contrast."""
    if variant == "classic":
        return base_color

    adj = VARIANT_ADJUSTMENTS.get(variant, {})
    delta = adj.get("lightness_delta", 0)
    target = adj.get("target_contrast", 4.5)

    adjusted = adjust_lightness(base_color, delta)
    return ensure_contrast(adjusted, bg_color, target)


# --- Color Resolution ---


def get_variant_colors(palette: dict, variant: str) -> dict:
    base = {
        **{f"background.{k}": v for k, v in palette["base"]["background"].items()},
        **{f"foreground.{k}": v for k, v in palette["base"]["foreground"].items()},
        **{f"border.{k}": v for k, v in palette["base"]["border"].items()},
        **{f"syntax.{k}": v for k, v in palette["syntax"].items() if not k.startswith("$")},
        **{f"terminal.{k}": v for k, v in palette["terminal"].items()},
    }
    if variant != "classic":
        overrides = palette.get("variants", {}).get(variant, {})
        base = {**base, **{k: v for k, v in overrides.items() if not k.startswith("$")}}
    return base


def resolve_template(template: str, colors: dict) -> str:
    replacer = lambda m: colors.get(m.group(1), m.group(0))
    return re.sub(r"\{\{([^}]+)\}\}", replacer, template)


def resolve_value(value, colors: dict):
    match value:
        case str() if "{{" in value:
            return resolve_template(value, colors)
        case dict():
            return {k: resolve_value(v, colors) for k, v in value.items()}
        case list():
            return [resolve_value(v, colors) for v in value]
        case _:
            return value


# --- Generation ---


def generate_players(palette: dict) -> list[dict]:
    return [{"cursor": c, "background": c, "selection": f"{c}40"} for c in palette["players"]]


def generate_syntax(base: dict, colors: dict) -> dict:
    color_map = base["syntax_colors"]
    style_map = base["syntax_styles"]
    special_map = base.get("syntax_special", {})

    token_colors = {
        token: key
        for key, tokens in color_map.items()
        if not key.startswith("$")
        for token in tokens
    }
    token_styles = {
        token: style
        for style, tokens in style_map.items()
        if not style.startswith("$")
        for token in tokens
    }

    get_color = lambda t: (
        colors.get("foreground.primary")
        if token_colors.get(t) == "foreground"
        else colors.get(f"syntax.{token_colors.get(t, 'type')}")
    )

    syntax = {
        token: {
            "color": get_color(token),
            "font_style": token_styles.get(token) if token_styles.get(token) != "normal" else "normal",
            "font_weight": 700 if token_styles.get(token) == "bold" else None,
        }
        for token in sorted(set(token_colors) | set(token_styles))
    }

    for key, template in special_map.items():
        if not key.startswith("$"):
            syntax[key] = {"color": resolve_template(template, colors)}

    return syntax


def generate_variant(base: dict, palette: dict, variant_key: str) -> dict:
    colors = get_variant_colors(palette, variant_key)
    config = base["variants"][variant_key]

    ui = resolve_value(base["ui"], colors)
    terminal = {f"terminal.{k}": resolve_value(v, colors) for k, v in base["terminal"].items()}
    syntax = generate_syntax(base, colors)

    style = {
        "background": colors["background.deep"],
        "foreground": colors["foreground.primary"],
        "accent": colors["syntax.type"],
        "border": colors["border.default"],
        "border.focused": colors["border.focused"],
        "elevated_surface.background": colors["background.surface"],
        "surface.background": colors["background.surface"],
        "element.background": colors["background.surface"],
        "element.hover": colors["background.elevated"],
        "element.active": colors["background.active"],
        "element.selected": colors["background.active"],
        "text": colors["foreground.primary"],
        "editor.background": colors["background.surface"],
        "editor.active_line.background": colors["background.elevated"],
        "editor.line_number": f"{colors['foreground.primary']}{config['line_number_alpha']}",
        **ui,
        **terminal,
        "players": generate_players(palette),
        "syntax": syntax,
    }

    return {"name": config["name"], "appearance": "dark", "style": style}


def generate_theme(base: dict, palette: dict) -> dict:
    return {
        "$schema": base["$schema"],
        "name": base["name"],
        "author": base["author"],
        "themes": [generate_variant(base, palette, k) for k in VARIANT_KEYS],
    }


# --- Validation ---


def find_colors(obj, path: str = "") -> list[tuple[str, str]]:
    match obj:
        case dict():
            return [item for k, v in obj.items() for item in find_colors(v, f"{path}.{k}")]
        case str() if obj.startswith("#"):
            return [(path, obj)]
        case _:
            return []


def validate_structure(data: dict) -> list[Result]:
    required_root = ["$schema", "themes"]
    required_theme = ["name", "appearance", "style"]

    errors = [f"Missing {k}" for k in required_root if k not in data] + [
        f"Theme {i}: missing {k}"
        for i, t in enumerate(data.get("themes", []))
        for k in required_theme
        if k not in t
    ]
    return [Result.failure(e) for e in errors] or [Result.success("Valid structure")]


def validate_colors(data: dict) -> list[Result]:
    pattern = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")
    invalid = [(p, c) for p, c in find_colors(data) if not pattern.match(c)]
    return (
        [Result.failure(f"{p}: invalid '{c}'") for p, c in invalid[:10]]
        or [Result.success("All colors valid hex format")]
    )


def validate_contrast(data: dict) -> list[Result]:
    results = []
    for t in data.get("themes", []):
        style = t["style"]
        bg = style.get("editor.background", style.get("background"))
        fg = style.get("editor.foreground", style.get("foreground"))
        comment = style.get("syntax", {}).get("comment", {})
        comment_color = comment.get("color") if isinstance(comment, dict) else None

        if bg and fg:
            ratio = contrast_ratio(bg, fg)
            results.append(
                Result.success(f"{t['name']} text contrast {ratio:.1f}:1")
                if ratio >= 4.5
                else Result.failure(f"{t['name']}: text contrast {ratio:.1f}:1 < 4.5:1")
            )
        if bg and comment_color:
            ratio = contrast_ratio(bg, comment_color)
            results.append(
                Result.success(f"{t['name']} comment contrast {ratio:.1f}:1")
                if ratio >= 3.0
                else Result.failure(f"{t['name']}: comment contrast {ratio:.1f}:1 < 3.0:1")
            )
    return results


def validate_players(data: dict) -> list[Result]:
    return [
        Result.success(f"{t['name']} has {len(p)} player colors")
        if len(p) >= 8
        else Result.failure(f"{t['name']}: only {len(p)} players")
        for t in data.get("themes", [])
        for p in [t["style"].get("players", [])]
    ]


def validate_consistency(data: dict) -> list[Result]:
    themes = data.get("themes", [])
    if len(themes) < 2:
        return [Result.success("Single theme")]

    base_keys = set(themes[0]["style"].keys())
    errors = [
        msg
        for t in themes[1:]
        for keys in [set(t["style"].keys())]
        for msg in (
            [f"{t['name']}: missing {base_keys - keys}"] if base_keys - keys else []
        ) + ([f"{t['name']}: extra {keys - base_keys}"] if keys - base_keys else [])
    ]
    return [Result.failure(e) for e in errors] or [Result.success(f"All {len(themes)} variants consistent")]


# --- Commands ---


def cmd_generate() -> int:
    base, palette = load_base(), load_palette()
    theme = generate_theme(base, palette)
    output = ROOT / "themes" / "synthwave84.json"
    output.write_text(json.dumps(theme, indent=2) + "\n")
    print(f"Generated {output}")
    return 0


def cmd_validate() -> int:
    print("Validating theme...\n")
    data = load_theme()

    validators = [validate_structure, validate_colors, validate_contrast, validate_players, validate_consistency]
    results = [r for v in validators for r in v(data)]

    for r in results:
        print(r.message)

    success = all(r.ok for r in results)
    print("\nValidation complete." if success else "\nValidation failed.")
    return 0 if success else 1


def cmd_check() -> int:
    print("Checking theme matches source...\n")
    current = load_theme()
    generated = generate_theme(load_base(), load_palette())

    current_str = json.dumps(current, sort_keys=True)
    generated_str = json.dumps(generated, sort_keys=True)

    if current_str == generated_str:
        print("OK: Theme matches source")
        return 0

    for i, (c, g) in enumerate(zip(current_str, generated_str)):
        if c != g:
            print(f"FAIL: Differs at position {i}")
            print(f"  Run 'make generate' to regenerate")
            return 1

    print("FAIL: Length mismatch")
    return 1


def cmd_derive() -> int:
    """Show what colors would be derived programmatically vs current palette."""
    palette = load_palette()
    base_syntax = {k: v for k, v in palette["syntax"].items() if not k.startswith("$")}

    # Background colors for each variant
    backgrounds = {
        "classic": palette["base"]["background"]["surface"],
        "soft": palette["variants"]["soft"].get("background.surface", palette["base"]["background"]["surface"]),
        "high_contrast": palette["variants"]["high_contrast"].get("background.surface", palette["base"]["background"]["surface"]),
    }

    print("Derived vs Manual Colors (WCAG contrast in parentheses)")
    print("=" * 75)
    print(f"{'Token':<10} {'Variant':<12} {'Manual':<10} {'Derived':<10} {'Diff':>6} {'Contrast':>10}")
    print("-" * 75)

    for token, base_color in base_syntax.items():
        for variant in ["soft", "high_contrast"]:
            bg = backgrounds[variant]
            derived = derive_variant_color(base_color, bg, variant)

            # Get manual color from palette
            manual_key = f"syntax.{token}"
            manual = palette["variants"][variant].get(manual_key, base_color)

            manual_contrast = contrast_ratio(manual, bg)
            derived_contrast = contrast_ratio(derived, bg)

            diff = "same" if manual.lower() == derived.lower() else "DIFF"

            print(f"{token:<10} {variant:<12} {manual:<10} {derived:<10} {diff:>6} {manual_contrast:.1f}/{derived_contrast:.1f}")

    print()
    print("Use '--apply' to update palette.json with derived colors")

    if len(sys.argv) > 2 and sys.argv[2] == "--apply":
        print("\nApplying derived colors...")
        for variant in ["soft", "high_contrast"]:
            bg = backgrounds[variant]
            for token, base_color in base_syntax.items():
                derived = derive_variant_color(base_color, bg, variant)
                palette["variants"][variant][f"syntax.{token}"] = derived

        (ROOT / "palette.json").write_text(json.dumps(palette, indent=2) + "\n")
        print("Updated palette.json")

    return 0


def cmd_coverage() -> int:
    """Check Zed syntax token coverage."""
    theme = load_theme()
    our_tokens = set(theme["themes"][0]["style"]["syntax"].keys())

    core = {
        "attribute", "boolean", "comment", "comment.doc", "constant", "constructor",
        "embedded", "emphasis", "emphasis.strong", "enum", "function", "hint",
        "keyword", "label", "link_text", "link_uri", "number", "operator",
        "predictive", "preproc", "property", "punctuation", "string", "tag",
        "text.literal", "title", "type", "variable", "variant"
    }

    missing = core - our_tokens
    covered = core - missing

    print(f"Token Coverage")
    print(f"=" * 40)
    print(f"Our tokens:     {len(our_tokens)}")
    print(f"Core tokens:    {len(covered)}/{len(core)} covered")

    if missing:
        print(f"\nMissing core tokens:")
        for t in sorted(missing):
            print(f"  - {t}")
    else:
        print(f"\nAll core tokens covered!")

    print(f"\nLanguage-specific: {len(our_tokens - core)} extra tokens")
    return 0 if not missing else 1


COMMANDS = {
    "generate": cmd_generate,
    "validate": cmd_validate,
    "check": cmd_check,
    "derive": cmd_derive,
    "coverage": cmd_coverage,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"Commands: {', '.join(COMMANDS)}")
        return 1
    return COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
