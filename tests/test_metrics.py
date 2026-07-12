import pytest
from src.metrics import pumping_power, thermal_resistance


def test_thermal_resistance():
    assert thermal_resistance(85, 25, 100) == pytest.approx(0.6)


def test_pumping_power():
    expected = 3000 * (0.2 / 1000 / 60)
    assert pumping_power(3000, 0.2) == pytest.approx(expected)
