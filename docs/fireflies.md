# Fireflies

Fireflies drift in from the canvas edges, blink independently, gather around hidden character positions, and gradually illuminate the text. The effect emphasizes wandering and staggered illumination rather than coordinated flock movement.

## Setup

Follow the [installation instructions](../README.md#install) first, including `python -m pip install .`
and copying the plugin files. These examples use released **TTE 0.15.0**. Keep the same virtual
environment activated for installation and playback.

## Run

```bash
printf 'HELLO WORLD' | tte fireflies --movement-speed 0.18 --wander-cycles 3 --auxiliary-count 6
```

Global TTE options go before `fireflies`; animation options go after it.
Run `tte fireflies -h` for the complete option list, including colors and final gradients.

## Main options

| Option | Default | Purpose |
| --- | --- | --- |
| `--movement-speed` | 0.18 | Base movement speed; individual fireflies vary around it. |
| `--wander-cycles` | 3 | Maximum number of wandering waypoints before gathering. |
| `--auxiliary-count` | 6 | Maximum atmospheric helpers; use 0 to disable them. |

The original input symbols and positions are restored when the animation finishes. Final colors follow the selected color-handling mode described below. Tiny canvases automatically reduce atmospheric helpers and orbiting.

## Input colors

By default, the effect uses its configured final gradient. To restore parsed ANSI foreground and
background colors at the end, put `--existing-color-handling dynamic` before the effect name:

```bash
printf '\033[31mHELLO\033[0m' | tte --existing-color-handling dynamic fireflies
```

Use `--existing-color-handling always` to keep input colors throughout playback. Uncolored text
finishes in terminal-default colors in dynamic mode.

## Python example

After installation, save the following as `fireflies_example.py` in the repository root:

```python
from effect_fireflies import Fireflies

effect = Fireflies("HELLO WORLD")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

From that same repository root, make the flat effect module available when running the script:

```bash
PYTHONPATH=effects python fireflies_example.py
```

Empty or whitespace-only library input raises
[`EmptyInputError`](../README.md#empty-input); background-colored spaces remain valid.
For setup problems, see [troubleshooting](../README.md#troubleshooting).
