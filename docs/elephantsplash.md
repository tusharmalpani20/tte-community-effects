# Elephant Splash

A purple elephant walks along the canvas floor as one coordinated ASCII sprite, drinks from a puddle, and sprays water to reveal the text. It raises its trunk and walks off while the completed text remains in place.

![Elephant Splash preview](../demos/elephantsplash_demo.gif)

This preview was recorded during original development; rendering may differ slightly on TTE 0.15.0.

## Setup

Follow the [installation instructions](../README.md#install) first, including `python -m pip install .`
and copying the plugin files. These examples use released **TTE 0.15.0**. Keep the same virtual
environment activated for installation and playback.

## Run

```bash
printf 'HELLO WORLD' | tte --canvas-width 80 --canvas-height 24 --anchor-text c elephantsplash
```

Global TTE options go before `elephantsplash`; animation options go after it.
Run `tte elephantsplash -h` for the complete option list, including colors and final gradients.

## Main options

| Option | Default | Purpose |
| --- | --- | --- |
| `--walk-pose-frames` | 8 | Frames to hold each walking pose. |
| `--horizontal-step-frames` | 4 | Frames between one-column walking steps. |
| `--final-hold-frames` | 120 | Frames to hold the completed text before stopping. |

A canvas of at least 41 columns by 16 rows enables the full elephant. Canvases of at least 12 columns by 6 rows use a compact elephant; smaller canvases use a text reveal without the sprite or particles. Use the walking timing options above to change pacing. The legacy `--movement-speed` option is retained for compatibility and does not control the walking pace.

## Input colors

By default, the effect uses its configured final gradient. To restore parsed ANSI foreground and
background colors at the end, put `--existing-color-handling dynamic` before the effect name:

```bash
printf '\033[31mHELLO\033[0m' | tte --existing-color-handling dynamic elephantsplash
```

Use `--existing-color-handling always` to keep input colors throughout playback. Uncolored text
finishes in terminal-default colors in dynamic mode.

## Python example

After installation, save the following as `elephantsplash_example.py` in the repository root:

```python
from effect_elephant_splash import ElephantSplash

effect = ElephantSplash("HELLO WORLD")
effect.terminal_config.canvas_width = 80
effect.terminal_config.canvas_height = 24
effect.terminal_config.anchor_text = "c"
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

From that same repository root, make the flat effect module available when running the script:

```bash
PYTHONPATH=effects python elephantsplash_example.py
```

Empty or whitespace-only library input raises
[`EmptyInputError`](../README.md#empty-input); background-colored spaces remain valid.
For setup problems, see [troubleshooting](../README.md#troubleshooting).

## Artwork credit

The full elephant is adapted from ASCII artwork by **jgs**, published at
[asciiart.website](https://asciiart.website/art/4937). The on-screen signature is omitted in the animation.
