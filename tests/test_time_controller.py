from unittest.mock import MagicMock, mock_open, patch

import pytest

from qlicS.time_controller import evolve

int_pattern = r"\d+"
expected_pattern = {rf"run {int_pattern}\n"}


# Helper to generate side_effect lambda
def generate_side_effect(time_sequence, current_timeblock_num, dump_dir):
    return lambda section, key: {
        ("sim_parameters", "timesequence"): time_sequence,
        ("live_vars", "current_timesequence_pos"): current_timeblock_num,
        ("directory", "dump_dir"): dump_dir,
    }[(section, key)]


# Mocking the dependencies
@pytest.fixture
def mock_configur():
    configur = MagicMock()
    configur.get.side_effect = generate_side_effect(
        "[[0.1, 10], [0.2, 20]]", "0", "/mock/path/"
    )
    return configur


@pytest.fixture
def mock_dump_dir():
    return (
        lambda setup: "/mock/path/"
    )  # TODO: this mock path is hardcoded in two places - fix


# Helpers
def mock_pl_func(steps_to_evolve):
    pl_func = MagicMock()
    pl_func.evolve.return_value = {
        "code": ["\n# Run simulation", {f"run {steps_to_evolve}\\n"}]
    }
    return pl_func


# Basic Tests
@pytest.mark.parametrize(
    "time_sequence, "
    "current_timeblock_num, "
    "expected_code, "
    "expected_timeblock_num, "
    "expected_evolution_steps",
    [
        (
            "[[1e-08, 10000.0], [1e-07, 10000.0]]",
            "0",
            ["timestep 1e-08", "\n# Run simulation", {"run 10000\\n"}],
            1,
            10000,
        ),
        (
            "[[1e-08, 10000.0], [1e-09, 500.0], [1e-7, 20000]]",
            "1",
            ["timestep 1e-09", "\n# Run simulation", {"run 500\\n"}],
            1,
            500,
        ),
        (
            "[[1e-010, 10000.0], [1e-09, 30000.0], [1e-09, 500.0]]",
            "2",
            ["timestep 1e-09", "\n# Run simulation", {"run 500\\n"}],
            1,
            500,
        ),
    ],
    ids=["first_timeblock", "second_timeblock", "third_timeblock"],
)
def test_evolve_happy_path(
    time_sequence,
    current_timeblock_num,
    expected_code,
    expected_timeblock_num,
    expected_evolution_steps,
    mock_configur,
    mock_dump_dir,
):

    # Arrange
    mock_configur.get.side_effect = generate_side_effect(
        time_sequence, current_timeblock_num, mock_dump_dir
    )

    # Act
    with patch("qlicS.time_controller.configur", mock_configur), patch(
        "qlicS.time_controller.pl_func", mock_pl_func(expected_evolution_steps)
    ), patch("builtins.open", mock_open(read_data="data")), patch(
        "qlicS.config_controller.configur", mock_configur
    ):
        result = evolve()

    # Assert
    assert result["code"] == expected_code


# TODO Physics Tests - I'm not sure how / if this is necessary
