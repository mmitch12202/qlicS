import random

import mock

import numpy as np

import pytest

from qlicS import laser_cooling_force

from .resources import check_string_format

# Objects

default_laser = [
    ("beam_radius", "0.1e-3"),
    ("saturation_paramater", "100"),
    ("detunning", "3e8"),
    ("laser_direction", "[-1 / 2,-1 / 2,-1 / np.sqrt(2)]"),
    ("laser_origin_position", "[0, 0, 0]"),
]
float_pattern = r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
expected_pattern = (
    rf"variable coolx atom \({float_pattern}\+?\({float_pattern}\*vx\)\)\*{float_pattern}\n"
    rf"variable cooly atom \({float_pattern}\+?{float_pattern}\*vy\)\*{float_pattern}\n"
    rf"variable coolz atom \({float_pattern}\+?{float_pattern}\*vz\)\*{float_pattern}\n"
    rf"fix {float_pattern} {float_pattern} addforce v_coolx v_cooly v_coolz"
)

# Fixtures


@pytest.fixture
def determ_F_0_test_values():
    return {"k": 1, "s": 1, "gamma": 1, "F_0": 1}


@pytest.fixture
def default_laser_fixture() -> dict:
    return default_laser


@pytest.fixture
def cycle_info() -> dict:
    return {
        "natural linewidth": 2 * np.pi * 18e6,
        "absorption center": 9.578e14,
        "saturation": 765,
    }


@pytest.fixture
def be_cloud() -> dict:
    return {"uid": 1}


@pytest.fixture
def type_pos():
    return 0


# Helpers


def configur_side_kick(s: str, t: str) -> dict:
    if s == "constants" and t == "h":
        return "6.626e-34"
    elif s == "constants" and t == "c":
        return "299792458"
    elif s == "ions" and t == "be+":
        return str(
            [
                {"mass": 9, "charge": 1},
                {
                    "natural linewidth": 2 * np.pi * 18e6,
                    "absorption center": 9.578e14,
                    "saturation": 765,
                },
            ]
        )


# Function Tests
def test_F_0_is_sensible():
    with mock.patch("qlicS.laser_cooling_force.configur.get", configur_side_kick):
        F_0 = laser_cooling_force.get_F_0(
            random.uniform(0, 5e8), random.uniform(0.001, 1e3), random.uniform(1e5, 1e7)
        )
        assert type(F_0) is float
        assert F_0 > 0


def test_beta_is_sensible():
    with mock.patch("qlicS.laser_cooling_force.configur.get", configur_side_kick):
        beta = laser_cooling_force.get_beta(
            random.uniform(0, 5e8),
            random.uniform(0.001, 1e3),
            random.uniform(1e5, 1e7),
            random.uniform(-10e6, -90e6),
        )
        assert type(beta) is float
        assert beta > 0


def test_total_force_is_sensible(be_cloud: dict, default_laser_fixture: dict, type_pos):
    with mock.patch.multiple(
        "qlicS.laser_cooling_force.configur",
        get=configur_side_kick,
        items=lambda x: default_laser_fixture,
    ):
        # Test implementation code here
        cooling_force = laser_cooling_force.create_cooling_laser(
            569202603907006,
            eval(configur_side_kick("ions", "be+"))[1],
            be_cloud["uid"],
            type_pos,
        )
        assert type(cooling_force) is dict
        print("***")
        print("".join(cooling_force["code"]))
        assert (
            check_string_format("".join(cooling_force["code"]), expected_pattern)
            is True
        )


# Physics Checks
# TODO Damping rate: damped oscillator decays appropriatly
# TODO F_0 test: displacement of single body in the potential in arbitrary direction
# TODO Limiting case tests
