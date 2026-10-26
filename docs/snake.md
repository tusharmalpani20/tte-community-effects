# Snake

Multiple snakes enter from the canvas edges, carry input characters along orthogonal paths, and deposit them into their final text positions.

## Setup

Follow the [installation instructions](../README.md#install) first, including `python -m pip install .`
and copying the plugin files. These examples use released **TTE 0.15.0**. Keep the same virtual
environment activated for installation and playback.

## Run

```bash
printf 'HELLO WORLD' | tte snake --snake-count 4 --movement-speed 1 --spawn-delay 3
```

Global TTE options go before `snake`; animation options go after it.
Run `tte snake -h` for the complete option list, including colors and final gradients.

## Main options

| Option | Default | Purpose |
| --- | --- | --- |
| `--snake-count` | 4 | Maximum number of snakes; reduced when there are fewer characters. |
| `--movement-speed` | 1.0 | Head movement speed. |
| `--spawn-delay` | 3 | Frames between snake spawns; use 0 to start them together. |
| `--head-symbol` | ● | Symbol used for each snake head. |

On small canvases, snakes animate the input retained by TTE. Each snake shrinks as it deposits its characters, and its head disappears when finished.

## Input colors

By default, the effect uses its configured final gradient. To restore parsed ANSI foreground and
background colors at the end, put `--existing-color-handling dynamic` before the effect name:

```bash
printf '\033[31mHELLO\033[0m' | tte --existing-color-handling dynamic snake
```

Use `--existing-color-handling always` to keep input colors throughout playback. Uncolored text
finishes in terminal-default colors in dynamic mode.

## Python example

After installation, save the following as `snake_example.py` in the repository root:

```python
from effect_snake import Snake

effect = Snake("HELLO WORLD")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

From that same repository root, make the flat effect module available when running the script:

```bash
PYTHONPATH=effects python snake_example.py
```

Empty or whitespace-only library input raises
[`EmptyInputError`](../README.md#empty-input); background-colored spaces remain valid.
For setup problems, see [troubleshooting](../README.md#troubleshooting).
