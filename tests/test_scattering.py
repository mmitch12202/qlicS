import random

import mock

import numpy as np

import pytest

from qlicS import scattering


# Fixtures
@pytest.fixture
def rand_velocity() -> list:
    return [random.gauss(0, 50), random.gauss(0, 50), random.gauss(0, 50)]


@pytest.fixture
def rand_scattering_laser() -> dict:
    k_x = random.random()
    k_y = random.random()
    k_z = random.random()
    k_mag = np.sqrt(k_x**2 + k_y**2 + k_z**2)
    return {
        "scattered_ion_indices": [
            str(random.randint(1, 10)),
            str(random.randint(10, 30)),
        ],  # TODO This is not safely done
        "target_species": random.choice(
            ["be+"]
        ),  # Other possible scattering species here
        "laser_direction": str([-k_x / k_mag, -k_y / k_mag, -k_z / k_mag]),
        "saturation_paramater": str(random.uniform(0.1, 200)),
        "frequency": str(random.gauss(957800000000000.0, 10e6)),
    }


@pytest.fixture
def fixed_species_info() -> dict:
    return {
        "natural linewidth": 113097335.52923255,
        "absorption center": 957800000000000.0,
        "saturation": 765,
    }


def test_scattering_ratecalc_succeeds(
    rand_velocity, rand_scattering_laser, fixed_species_info
):
    with mock.patch("qlicS.scattering.configur.get") as mock_config:
        mock_config.return_value = "299792458"
        scattering_rate = scattering.scattering_rate(
            rand_velocity, rand_scattering_laser, fixed_species_info
        )
        assert scattering_rate > 0


# TODO some summation tests to test we are summing correctly
# in illuminate and get_scattering

# TODO some physics tests to check limiting cases or a math test
# that tests function behavior on scattering
