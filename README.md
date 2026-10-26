# TTE Community Effects

Custom text animations by Tushar Malpani for [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects).
The effects are maintained here, separately from the upstream TTE package.

| Command | Animation | Guide |
| --- | --- | --- |
| `elephantsplash` | An elephant drinks from a puddle and sprays water to reveal your text. | [Elephant Splash](docs/elephantsplash.md) |
| `fireflies` | Wandering, blinking fireflies gather to illuminate your text. | [Fireflies](docs/fireflies.md) |
| `fishing` | Fishing hooks catch scattered characters and reel them into place. | [Fishing](docs/fishing.md) |
| `snake` | Snakes carry characters along grid paths to assemble your text. | [Snake](docs/snake.md) |

## Compatibility

These effects currently target upstream development revision
[`b75a7ba`](https://github.com/ChrisBuilds/terminaltexteffects/commit/b75a7baefe89a25d22754bcefb7d5caae8809477).
**Released TTE 0.15.0 is not supported by this collection:** three effects need engine helpers absent from that release.
The requirements file pins the tested revision so later upstream API changes do not silently change your installation.
Use Python 3.14 for the following setup, matching the verification environment.

## Install

Clone this repository, create an isolated environment, and install the pinned TTE revision:

```bash
git clone https://github.com/tusharmalpani20/tte-community-effects.git
cd tte-community-effects
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy the four plugin files into TTE's custom-effects directory:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/terminaltexteffects/effects"
cp effects/effect_*.py "${XDG_CONFIG_HOME:-$HOME/.config}/terminaltexteffects/effects/"
```

If `XDG_CONFIG_HOME` is set, it must be an absolute path; otherwise unset it first.
Review any existing files with these names before copying, since `cp` replaces them.
The source files in this repository are Python plugins and run in your TTE environment.

## Run

Keep the virtual environment activated, then try:

```bash
printf 'HELLO WORLD' | tte snake
printf 'HELLO WORLD' | tte fishing
printf 'HELLO WORLD' | tte fireflies
printf 'HELLO WORLD' | tte --canvas-width 80 --canvas-height 24 --anchor-text c elephantsplash
```

Run `tte elephantsplash -h` (or another command above) to see every option.
For Elephant Splash, a canvas at least 41 columns by 16 rows shows the full choreography.
The effect guides contain example previews recorded during original development; they are illustrative and may differ from the pinned engine's rendering.

## Update or remove

After updating this repository, copy the desired modules into the custom-effects directory again.
To remove an animation, delete its matching `effect_*.py` file from that directory.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
ruff format --check effects tests
ruff check effects tests
python -m pyright --pythonpath "$(pwd)/.venv/bin/python" effects tests
```

For Python library usage, add `effects/` to your Python import path and import the flat module
(for example `from effect_snake import Snake`). Plugins are not installed into `terminaltexteffects.effects`.

## Credits and license

Effect code is shared under the [MIT license](LICENSE). The upstream TTE copyright notice is retained.
Elephant Splash adapts elephant ASCII artwork by **jgs**, published at
[asciiart.website](https://asciiart.website/art/4937); its on-screen signature is omitted in the animation.
That artwork credit is separate from the software license and does not assert ownership of the original drawing.

## Community

Share demos and discover more effects in
[TTE Effect Show and Tell](https://github.com/ChrisBuilds/terminaltexteffects/discussions/categories/tte-effect-show-and-tell).
For issues with these animations, use this repository's issue tracker.
Maintenance status: initial community collection; compatibility currently follows the pinned upstream revision above.
