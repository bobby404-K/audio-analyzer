import math
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from audio_utils import calculate_rms_energy


def test_calculate_rms_energy_for_known_signal():
    signal = [1.0, -1.0, 1.0, -1.0]
    assert math.isclose(calculate_rms_energy(signal), 1.0)


def test_calculate_rms_energy_for_silent_signal():
    signal = [0.0, 0.0, 0.0]
    assert calculate_rms_energy(signal) == 0.0


def test_calculate_rms_energy_raises_for_empty_signal():
    with pytest.raises(ValueError, match="must not be empty"):
        calculate_rms_energy([])
