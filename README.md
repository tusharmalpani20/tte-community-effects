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

The collection targets **released TerminalTextEffects 0.15.0**, installed automatically with
our shared support package. No TTE development checkout is needed.
Use Python 3.14 for the setup below, matching the verification environment.

## Install

Clone this repository, create an isolated environment, and install the collection’s shared support code and TTE:

```bash
git clone https://github.com/tusharmalpani20/tte-community-effects.git
cd tte-community-effects
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

The install command above also installs support code required by the plugins; copying the
plugin files alone is not enough. Then copy the four files into TTE's custom-effects directory:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/terminaltexteffects/effects"
cp effects/effect_*.py "${XDG_CONFIG_HOME:-$HOME/.config}/terminaltexteffects/effects/"
```

If `XDG_CONFIG_HOME` is set, it must be an absolute path; otherwise unset it first.
Review any existing files with these names before copying, since `cp` replaces them.
The source files in this repository are Python plugins and run in your TTE environment.

## Run

Keep the virtual environment activated so the `tte` command uses the environment containing
our support package. Then try:

```bash
printf 'HELLO WORLD' | tte snake
printf 'HELLO WORLD' | tte fishing
printf 'HELLO WORLD' | tte fireflies
printf 'HELLO WORLD' | tte --canvas-width 80 --canvas-height 24 --anchor-text c elephantsplash
```

Run `tte elephantsplash -h` (or another command above) to see every option.
For Elephant Splash, a canvas at least 41 columns by 16 rows shows the full choreography.
The Elephant Splash guide includes a preview recorded during original development; it is illustrative
and may differ slightly from TTE 0.15.0’s rendering.

## Empty input

For Python library usage, empty or whitespace-only input raises
`tte_community_support.base.EmptyInputError` (a `ValueError`). Background-colored spaces
remain valid input. The CLI follows TTE 0.15.0’s own input handling.

## Update or remove

After updating this repository, rerun `python -m pip install .` in the activated environment,
then copy the desired modules into the custom-effects directory again.

If you used this collection’s earlier development-based installation, create a fresh virtual
environment using the installation steps above, or explicitly replace that TTE build first:

```bash
python -m pip install --force-reinstall terminaltexteffects==0.15.0
python -m pip install .
```

The older development build also reported version 0.15.0, so a normal install can otherwise
mistake it for the released package.

To remove an animation, delete its matching `effect_*.py` file from that directory.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
ruff format --check effects tte_community_support tests
ruff check effects tte_community_support tests
python -m pyright --pythonpath "$(pwd)/.venv/bin/python" effects tte_community_support tests
```

For Python library usage, first install the support package as above, then add `effects/` to your
Python import path and import the flat module
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
Maintenance status: maintained by the author; this collection currently supports TTE 0.15.0.
Newer TTE releases require a compatibility check before upgrading.
