"""Exercise the installed CLI with the filenames users actually copy."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("command", ["snake", "fishing", "elephantsplash", "fireflies"])
def test_installed_cli_loads_and_runs_community_effects(
    command: str,
    tmp_path: Path,
) -> None:
    """A fresh process must discover all four plugins without import conflicts."""
    config_home = tmp_path / "cli_config"
    plugin_directory = config_home / "terminaltexteffects" / "effects"
    shutil.copytree(
        Path(__file__).parents[1] / "effects", plugin_directory, ignore=shutil.ignore_patterns("__pycache__")
    )
    environment = os.environ.copy()
    environment["XDG_CONFIG_HOME"] = str(config_home)
    environment.pop("TTE_DEV_EFFECTS_DIR", None)
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "terminaltexteffects",
            "--frame-rate",
            "0",
            "--ignore-terminal-dimensions",
            command,
        ],
        input="Hello!",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=environment,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout
