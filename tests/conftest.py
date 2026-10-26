"""Test external effects through TTE's user-plugin discovery."""

from pathlib import Path
import shutil

import pytest


@pytest.fixture(autouse=True)
def user_effect_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Discover only this collection's effects, independent of user configuration."""
    config = tmp_path / "config"
    effects = config / "terminaltexteffects" / "effects"
    effects.mkdir(parents=True)
    for source in (Path(__file__).parents[1] / "effects").glob("*.py"):
        # Keep CLI-loaded modules distinct from directly imported library modules.
        shutil.copy2(source, effects / f"community_test_{source.name}")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config))
    monkeypatch.delenv("TTE_DEV_EFFECTS_DIR", raising=False)
