"""Local iterator safeguards for the TTE 0.15.0 engine."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from copy import deepcopy
from typing import TypeVar

from terminaltexteffects.engine.base_character import EffectCharacter
from terminaltexteffects.engine.base_config import BaseConfig
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.engine.terminal import Terminal, TerminalConfig

Config = TypeVar("Config", bound=BaseConfig)


class EmptyInputError(ValueError):
    """The configured canvas contains no retained input characters."""


class _CommunityTerminal(Terminal):
    """Reject empty input before the released engine calculates text bounds."""

    def __init__(self, input_data: str, config: TerminalConfig) -> None:
        if not input_data:
            raise EmptyInputError("The effect requires visible input.")
        super().__init__(input_data, config)

    def _retained_characters(self) -> list[EffectCharacter]:
        return [
            character
            for line in self._preprocessed_character_lines
            for character in line
            if character.input_symbol != " "
            or character.animation.input_fg_color is not None
            or character.animation.input_bg_color is not None
        ]

    def _get_canvas_dimensions(self) -> tuple[int, int]:
        # Background-colored spaces are meaningful input and must not be stripped.
        if not self._retained_characters():
            raise EmptyInputError("The effect requires visible input.")
        return super()._get_canvas_dimensions()

    def _setup_input_characters(self) -> list[EffectCharacter]:
        try:
            return super()._setup_input_characters()
        except ValueError:
            # TTE 0.15.0 computes min/max after clipping. Only translate that
            # empty-canvas failure; preserve other engine validation errors.
            if not any(
                self.canvas.coord_is_in_canvas(character.input_coord) for character in self._retained_characters()
            ):
                raise EmptyInputError("The configured canvas contains no visible input.") from None
            raise


class CommunityEffect(BaseEffect[Config]):
    """Validate input consistently before preparing a terminal for playback."""

    @contextmanager
    def terminal_output(self, end_symbol: str = "\n") -> Generator[Terminal, None, None]:
        """Prepare the collection's terminal and restore it even if playback fails."""
        terminal = _CommunityTerminal(self.input_data, self.terminal_config)
        try:
            terminal.prep_canvas()
            yield terminal
        finally:
            terminal.restore_cursor(end_symbol)


class CommunityEffectIterator(BaseEffectIterator[Config]):
    """Use local empty-input handling and allow callbacks to change active particles."""

    def __init__(self, effect: BaseEffect) -> None:
        self.config: Config = deepcopy(effect.effect_config)
        self.terminal = _CommunityTerminal(effect.input_data, deepcopy(effect.terminal_config))
        self.active_characters: set[EffectCharacter] = set()
        self.preexisting_colors_present = any(
            character.animation.input_fg_color is not None or character.animation.input_bg_color is not None
            for character in self.terminal.get_characters()
        )

    def update(self) -> None:
        """Tick a stable snapshot, keeping characters added by callbacks for the next frame."""
        current_characters = tuple(self.active_characters)
        for character in current_characters:
            if character in self.active_characters:
                character.tick()
        self.active_characters.difference_update(
            character for character in current_characters if not character.is_active
        )
