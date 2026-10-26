"""Behavior checks for the support code used with released TTE."""

from typing import cast

import pytest

from terminaltexteffects.effects.effect_beams import Beams
from terminaltexteffects.engine.base_character import EffectCharacter, EventHandler
from terminaltexteffects.engine.base_config import BaseConfig
from terminaltexteffects.utils.geometry import Coord
from tte_community_support import CommunityEffectIterator, EmptyInputError, ParticlePool, ParticleReset


class _Iterator(CommunityEffectIterator[BaseConfig]):
    def __next__(self) -> str:
        self.update()
        return self.frame


def _iterator(input_data: str = "A") -> _Iterator:
    effect = Beams(input_data)
    effect.terminal_config.frame_rate = 0
    effect.terminal_config.ignore_terminal_dimensions = True
    return _Iterator(effect)


@pytest.mark.parametrize("input_data", ["", "   \n\t", "\x1b[0m \x1b[0m"])
def test_empty_input_has_a_clear_error(input_data: str) -> None:
    """Whitespace and formatting-only input cannot reach the engine's min/max failure."""
    with pytest.raises(EmptyInputError):
        _iterator(input_data)


@pytest.mark.parametrize("input_data", ["", "   \n\t", "\x1b[0m \x1b[0m"])
def test_terminal_output_rejects_empty_input_before_writing(
    input_data: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The documented playback context rejects empty input before touching the terminal."""
    from effect_snake import Snake

    with pytest.raises(EmptyInputError), Snake(input_data).terminal_output():
        pytest.fail("Empty input must be rejected before entering the output context")

    assert capsys.readouterr().out == ""


def test_background_colored_space_is_retained() -> None:
    """A space that visibly paints the terminal is not empty input."""
    iterator = _iterator("\x1b[48;5;106m \x1b[0m")

    assert len(iterator.terminal.get_characters()) == 1
    character = iterator.terminal.get_characters()[0]
    assert character.input_symbol == " "
    assert character.animation.input_bg_color is not None


def test_fully_clipped_input_has_a_clear_error() -> None:
    """Clipping every non-space cell also produces the collection's input error."""
    effect = Beams("   A")
    effect.terminal_config.canvas_width = 1
    effect.terminal_config.canvas_height = 1

    with pytest.raises(EmptyInputError):
        _Iterator(effect)


def test_pool_reclaims_on_completion_and_reuses_its_capacity() -> None:
    """Callbacks can return several particles while an iterator is ticking them."""
    iterator = _iterator()

    def initialize(particle: EffectCharacter) -> None:
        scene = particle.animation.new_scene(scene_id="spark")
        scene.add_frame("*", 1)

    pool = ParticlePool(
        iterator.terminal, iterator.active_characters, "*", initial_count=2, max_size=2, initializer=initialize
    )
    for particle in pool.particles:
        pool.reclaim_on_event(particle, particle.animation.query_scene("spark"))

    def activate(particle: EffectCharacter) -> None:
        particle.animation.activate_scene("spark")

    emitted = [pool.emit(Coord(1, 1), activate) for _ in range(2)]
    assert all(particle is not None for particle in emitted)
    assert pool.emit(Coord(1, 1), activate) is None

    iterator.update()

    assert len(pool.available) == 2
    assert not iterator.active_characters
    assert all(not particle.is_visible for particle in pool.particles)
    reused = pool.emit(Coord(1, 1), activate)
    assert reused in emitted
    assert len(pool) == 2
    iterator.update()
    assert len(pool.available) == 2


def test_acquire_can_clear_prior_particle_state() -> None:
    """Explicit reset policies remove per-emission paths, scenes and callbacks."""
    iterator = _iterator()
    pool = ParticlePool(iterator.terminal, iterator.active_characters, "*", initial_count=1, max_size=1)
    particle = cast("EffectCharacter", pool.acquire())
    scene = particle.animation.new_scene(scene_id="old")
    scene.add_frame("*", 1)
    particle.motion.new_path(path_id="old").new_waypoint(Coord(1, 1))
    pool.reclaim_on_event(particle, scene)
    pool.reclaim(particle)

    reused = pool.acquire(reset=ParticleReset(clear_paths=True, clear_scenes=True, clear_events=True))

    assert reused is particle
    assert not particle.motion.paths
    assert not particle.animation.scenes
    assert not particle.event_handler.registered_events


def test_callback_added_character_waits_until_the_next_update() -> None:
    """A callback can add a character without advancing it in the same frame."""
    iterator = _iterator()
    first = iterator.terminal.add_character("*", Coord(1, 1))
    second = iterator.terminal.add_character("+", Coord(1, 1))
    first_scene = first.animation.new_scene()
    first_scene.add_frame("*", 1)
    second_scene = second.animation.new_scene()
    second_scene.add_frame("+", 2)

    def activate_second(_character: EffectCharacter) -> None:
        second.animation.activate_scene(second_scene)
        iterator.active_characters.add(second)

    first.event_handler.register_event(
        EventHandler.Event.SCENE_COMPLETE,
        first_scene,
        EventHandler.Action.CALLBACK,
        EventHandler.Callback(activate_second),
    )
    first.animation.activate_scene(first_scene)
    iterator.active_characters.add(first)

    iterator.update()

    assert second in iterator.active_characters
    assert second_scene.frames[0].ticks_elapsed == 0
    iterator.update()
    assert second_scene.frames[0].ticks_elapsed == 1
