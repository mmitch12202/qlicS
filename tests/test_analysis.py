from unittest.mock import patch

import numpy as np

import pytest

from qlicS.analysis import velocities


# Mocking configur and pl_func
@pytest.fixture
def mock_configur():
    with patch("qlicS.analysis.configur") as mock:
        yield mock


@pytest.fixture
def mock_readdump():
    with patch("qlicS.analysis.pl_func.readdump") as mock:
        yield mock


# Helpers


def assert_dict_of_arrays_equal(expected, result):
    assert (
        expected.keys() == result.keys()
    ), "The keys of the dictionaries are not the same"
    for key in result:
        np.testing.assert_array_equal(
            expected[key],
            result[key],
            err_msg=f"The arrays for key {key} are not the same",
        )


# Predefined numpy arrays for reuse
mock_data_array = np.array(
    [
        [
            [9.0, 25.3, 27.79, 14.12, 32.1, 19.02],
            [15.68, 39.01, 20.34, 36.63, 1.26, 31.58],
            [5.72, 8.72, 48.29, 40.23, 33.82, 19.88],
            [1.29, 13.77, 25.35, 45.1, 23.52, 30.96],
        ],
        [
            [35.28, 8.68, 29.03, 0.54, 17.65, 44.18],
            [9.06, 5.07, 13.17, 7.26, 5.67, 39.15],
            [28.49, 11.74, 46.2, 5.51, 35.26, 25.89],
            [48.12, 18.45, 26.69, 7.21, 40.53, 29.14],
        ],
        [
            [19.8, 17.4, 9.19, 5.34, 42.17, 30.99],
            [23.22, 30.48, 39.48, 18.8, 9.06, 14.63],
            [31.53, 17.14, 29.56, 48.13, 4.84, 10.39],
            [11.25, 4.57, 39.0, 47.05, 6.83, 29.12],
        ],
        [
            [9.96, 31.21, 33.98, 10.69, 22.69, 9.28],
            [14.97, 45.3, 35.88, 21.6, 33.41, 41.15],
            [35.12, 17.15, 0.07, 27.23, 10.63, 2.3],
            [1.49, 13.05, 37.68, 46.36, 17.08, 20.75],
        ],
        [
            [27.25, 21.2, 37.04, 20.95, 23.26, 47.86],
            [23.96, 15.51, 17.75, 34.52, 29.79, 31.13],
            [12.53, 10.12, 1.15, 4.71, 39.59, 34.02],
            [29.4, 32.97, 2.17, 1.56, 37.99, 40.24],
        ],
    ],
    dtype=np.float64,
)


@pytest.mark.parametrize(
    "atom_range, step_range, velocity_indices, mock_data, expected",
    [
        # Happy path tests
        (
            (0, 2),
            [1, 3],
            [3, 6],
            ([0, 1, 2, 3, 4], mock_data_array),
            {
                0: np.array(
                    [[0.54, 17.65, 44.18], [7.26, 5.67, 39.15]], dtype=np.float64
                ),
                1: np.array(
                    [[5.34, 42.17, 30.99], [18.8, 9.06, 14.63]], dtype=np.float64
                ),
            },
        )
    ],
    ids=["happy_path_1"],
)
def test_velocities_custom_params(
    mock_configur,
    mock_readdump,
    atom_range,
    step_range,
    velocity_indices,
    mock_data,
    expected,
):
    # Arrange
    mock_configur.get.return_value = "/mock/directory/"
    mock_readdump.return_value = mock_data

    # Act
    result = velocities(atom_range, step_range, velocity_indices)

    # Assert
    assert_dict_of_arrays_equal(expected, result)


@pytest.mark.parametrize(
    "mock_data, expected",
    [
        # Happy path tests
        (
            ([0, 1, 2, 3, 4], mock_data_array),
            {
                0: np.array(
                    [
                        [14.12, 32.1, 19.02],
                        [36.63, 1.26, 31.58],
                        [40.23, 33.82, 19.88],
                        [45.1, 23.52, 30.96],
                    ],
                    dtype=np.float64,
                ),
                1: np.array(
                    [
                        [0.54, 17.65, 44.18],
                        [7.26, 5.67, 39.15],
                        [5.51, 35.26, 25.89],
                        [7.21, 40.53, 29.14],
                    ],
                    dtype=np.float64,
                ),
                2: np.array(
                    [
                        [5.34, 42.17, 30.99],
                        [18.8, 9.06, 14.63],
                        [48.13, 4.84, 10.39],
                        [47.05, 6.83, 29.12],
                    ],
                    dtype=np.float64,
                ),
                3: np.array(
                    [
                        [10.69, 22.69, 9.28],
                        [21.6, 33.41, 41.15],
                        [27.23, 10.63, 2.3],
                        [46.36, 17.08, 20.75],
                    ],
                    dtype=np.float64,
                ),
                4: np.array(
                    [
                        [20.95, 23.26, 47.86],
                        [34.52, 29.79, 31.13],
                        [4.71, 39.59, 34.02],
                        [1.56, 37.99, 40.24],
                    ],
                    dtype=np.float64,
                ),
            },
        )
    ],
    ids=["happy_path_1"],
)
def test_velocities_default_params(mock_configur, mock_readdump, mock_data, expected):
    # Arrange
    mock_configur.get.return_value = "/mock/directory/"
    mock_readdump.return_value = mock_data

    # Act
    result = velocities()

    # Assert
    assert_dict_of_arrays_equal(expected, result)
