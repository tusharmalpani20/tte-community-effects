# Fishing

Fishing hooks catch scattered, swimming characters and reel them into their final text positions. Hooks briefly tug at each catch, transport it across the canvas, and disappear after the text settles.

## Setup

Follow the [installation instructions](../README.md#install) first, including `python -m pip install .`
and copying the plugin files. These examples use released **TTE 0.15.0**. Keep the same virtual
environment activated for installation and playback.

## Run

```bash
printf 'HELLO WORLD' | tte fishing --hook-count 3 --wrong-catch-chance 0
```

Global TTE options go before `fishing`; animation options go after it.
Run `tte fishing -h` for the complete option list, including colors and final gradients.

## Main options

| Option | Default | Purpose |
| --- | --- | --- |
| `--hook-count` | 3 | Maximum number of hooks working concurrently. |
| `--cast-speed` | 0.75 | Hook casting speed. |
| `--reel-speed` | 1.25 | Reeling and return speed. |
| `--cast-delay` | 4 | Frames between casts and initial hook starts. |
| `--wrong-catch-chance` | 0.05 | Chance of one harmless junk catch per hook; use 0 to disable it. |

Fishing uses at most one hook per catchable character and canvas column. Junk catches use auxiliary symbols and never replace input text. Each hook can make at most one junk catch.

## Input colors

By default, the effect uses its configured final gradient. To restore parsed ANSI foreground and
background colors at the end, put `--existing-color-handling dynamic` before the effect name:

```bash
printf '\033[31mHELLO\033[0m' | tte --existing-color-handling dynamic fishing
```

Use `--existing-color-handling always` to keep input colors throughout playback. Uncolored text
finishes in terminal-default colors in dynamic mode.

## Python example

After installation, save the following as `fishing_example.py` in the repository root:

```python
from effect_fishing import Fishing

effect = Fishing("HELLO WORLD")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

From that same repository root, make the flat effect module available when running the script:

```bash
PYTHONPATH=effects python fishing_example.py
```

Empty or whitespace-only library input raises
[`EmptyInputError`](../README.md#empty-input); background-colored spaces remain valid.
For setup problems, see [troubleshooting](../README.md#troubleshooting).
