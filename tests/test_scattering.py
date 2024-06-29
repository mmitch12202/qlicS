import random

import mock

import numpy as np

import pytest

from qlicS import scattering

# Objects
species_info = {
    "natural linewidth": 113097335.52923255,
    "absorption center": 957800000000000.0,
    "saturation": 765,
}


# Fixtures
@pytest.fixture
def rand_velocity() -> list:
    return [random.gauss(0, 50), random.gauss(0, 50), random.gauss(0, 50)]


@pytest.fixture
def rand_velocity_list(rand_velocity) -> list:
    max_timestep = 5000
    max_atom = 50
    return [[rand_velocity for _ in range(max_atom)] for _ in range(max_timestep)]


@pytest.fixture
def rand_scattering_laser() -> dict:
    k_x = random.random()
    k_y = random.random()
    k_z = random.random()
    k_mag = np.sqrt(k_x**2 + k_y**2 + k_z**2)
    return {
        "scattered_ion_indices": str(
            [
                random.randint(1, 10),
                random.randint(10, 30),
            ]
        ),  # TODO This is not safely done
        "target_species": random.choice(
            ["be+"]
        ),  # Other possible scattering species here
        "laser_direction": str([-k_x / k_mag, -k_y / k_mag, -k_z / k_mag]),
        "saturation_paramater": str(random.uniform(0.1, 200)),
        "frequency": str(random.gauss(957800000000000.0, 10e6)),
    }


@pytest.fixture
def fixed_species_info() -> dict:
    return species_info


# Helpers
def configur_side_kick(s: str, t: str) -> dict:
    if s == "sim_parameters" and t == "log_steps":
        return "10"
    elif s == "ions" and t == "be+":
        return str(
            [
                None,
                species_info,
            ]
        )
    elif s == "constants" and t == "c":
        return "299792458"


# Tests
def test_scattering_ratecalc_is_sensible(
    rand_velocity, rand_scattering_laser, fixed_species_info
):
    with mock.patch("qlicS.scattering.configur.get", configur_side_kick):
        scattering_rate = scattering.scattering_rate(
            rand_velocity, rand_scattering_laser, fixed_species_info
        )
        assert scattering_rate > 0
        assert type(scattering_rate) is np.float64


def test_illuminate_sum_is_sensible(rand_scattering_laser, rand_velocity_list):
    dt = 1e-9
    with mock.patch("qlicS.scattering.configur.get", configur_side_kick), mock.patch(
        "qlicS.scattering.get_dt_given_timestep", return_value=dt
    ), mock.patch("qlicS.scattering.velocities", return_value=rand_velocity_list):
        start_stop_pair = [1000, 2000]
        photon_count = scattering.illuminate(start_stop_pair, rand_scattering_laser)
        assert photon_count > 0
        assert type(photon_count) is np.float64
