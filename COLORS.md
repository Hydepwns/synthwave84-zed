# Synthwave '84 Color Palette

All colors are defined in `palette.json`. This document provides a quick reference.

## Base Colors (Classic Variant)

| Role                | Hex       | Usage                      |
| ------------------- | --------- | -------------------------- |
| Background Deep     | `#241b2f` | Main background, panels    |
| Background Surface  | `#262335` | Editor, elevated surfaces  |
| Background Elevated | `#2a2139` | Hover states, active lines |
| Background Active   | `#463465` | Selected elements          |
| Foreground          | `#ffffff` | Primary text               |
| Border              | `#495495` | Default borders            |
| Border Focused      | `#880088` | Focus indicators           |

## Syntax Colors

| Role        | Classic   | Soft      | High Contrast | Delta     |
| ----------- | --------- | --------- | ------------- | --------- |
| Function    | `#36f9f6` | `#5af5f3` | `#00f5f0`     | `#edff98` |
| Heading     | `#36f9f6` | `#5af5f3` | `#00f5f0`     | `#c0ff98` |
| Keyword     | `#fede5d` | `#fee380` | `#ffdc00`     | `#ff67d4` |
| Declaration | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#ff67d4` |
| String      | `#ff8b39` | `#ffa15a` | `#ff7700`     | `#d598ff` |
| Type        | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#c0ff98` |
| Variable    | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#efeffd` |
| Tag         | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#ff67d4` |
| Markup      | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#ffd298` |
| List        | `#ff7edb` | `#ff92e0` | `#ff6bd6`     | `#d598ff` |
| Constant    | `#f97e72` | `#fa9890` | `#ff6b5d`     | `#ff98b3` |
| Number      | `#f97e72` | `#fa9890` | `#ff6b5d`     | `#98fffb` |
| Parameter   | `#f97e72` | `#fa9890` | `#ff6b5d`     | `#ffd298` |
| Comment     | `#848bbd` | `#848bbd` | `#9da5d5`     | `#a562a6` |
| Success     | `#72f1b8` | `#85f3c3` | `#5fffaf`     | `#c0ff98` |
| Info        | `#03edf9` | `#33f0fc` | `#00e5ff`     | `#98fffb` |
| Error       | `#fe4450` | `#fe6670` | `#ff2030`     | `#ff98b3` |

`Heading`, `Declaration`, `Variable`, `Tag`, `Markup`, `List`, `Number`, and
`Parameter` were split out of the coarser `Function` / `Type` / `Constant` buckets so
Delta can reassign them independently. They hold their original values in the three
Synthwave variants, which are unchanged.

## Delta Base Colors

| Role                | Hex       | Usage                            |
| ------------------- | --------- | -------------------------------- |
| Background Deep     | `#251d2b` | Main background, panels          |
| Background Surface  | `#2b2233` | Editor, elevated surfaces        |
| Background Elevated | `#352a3f` | Hover states, active lines       |
| Background Active   | `#492949` | Selected elements                |
| Foreground          | `#efeffd` | Primary text                     |
| Border              | `#925393` | Default borders                  |
| Border Focused      | `#ff67d4` | Focus indicators                 |

## Terminal Colors

| ANSI    | Color     |
| ------- | --------- |
| Black   | `#241b2f` |
| Red     | `#fe4450` |
| Green   | `#72f1b8` |
| Yellow  | `#fede5d` |
| Blue    | `#03edf9` |
| Magenta | `#ff7edb` |
| Cyan    | `#36f9f6` |
| White   | `#ffffff` |

## Player Colors (Collaboration)

| #   | Synthwave         | Delta             |
| --- | ----------------- | ----------------- |
| 1   | `#f97e72` Coral   | `#ff67d4` Pink    |
| 2   | `#36f9f6` Cyan    | `#98fffb` Cyan    |
| 3   | `#ff7edb` Pink    | `#c0ff98` Green   |
| 4   | `#fede5d` Yellow  | `#edff98` Yellow  |
| 5   | `#72f1b8` Mint    | `#d598ff` Purple  |
| 6   | `#03edf9` Blue    | `#ff98b3` Red     |
| 7   | `#ff8b39` Orange  | `#ffd298` Orange  |
| 8   | `#b893ce` Purple  | `#b279b3` Mauve   |

## Alpha Variants

Use hex alpha suffix for transparency:

- `40` = 25% opacity (selections, backgrounds)
- `80` = 50% opacity (muted text, dim states)
- `20` = 12% opacity (subtle highlights)

Example: `#ff7edb40` = pink at 25% opacity
