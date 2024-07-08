import pytest
from unittest.mock import patch, MagicMock
from qlicS.exp_sequence_controller import create_and_run_sim_gen

# FIXME replaces this with real runs from the examples .ini examples.  Basically just test that they run w/out error and then move on to physics testing
@pytest.mark.parametrize(
    "input_sequence, expected_calls",
    [
        ("dumping", [("pylion_dumping")]),
        ("cloud", [("pylion_cloud")]),
        ("cloud,trap", [("pylion_cloud"), ("gen_trap_lammps")]),
        ("cooling_laser", [("create_cooling_laser")]),
        ("evolve", [("evolve")]),
        ("tickle", [("create_tickle")]),
        ("dumping,cloud", [("pylion_dumping"), ("pylion_cloud")]),
        (
            "cloud,trap,cooling_laser",
            [
                ("pylion_cloud"),
                ("gen_trap_lammps"),
                ("create_cooling_laser"),
            ],
        ),
        ("evolve,tickle", [("evolve"), ("create_tickle")]),
        ("", []),
        ("invalid_command", []),
    ],
    ids=[
        "single_command_dumping",
        "single_command_cloud",
        "single_command_trap_plus_create_ions",
        "single_command_cooling_laser",
        "single_command_evolve",
        "single_command_tickle",
        "multiple_commands_dumping_cloud",
        "multiple_commands_trap_cooling_laser",
        "multiple_commands_evolve_tickle",
        "empty_input_sequence",
        "invalid_command",
    ],
)
def test_create_and_run_sim_gen(input_sequence, expected_calls):
    with patch("qlicS.exp_sequence_controller.pl.Simulation"), patch(
        "qlicS.exp_sequence_controller.configur.get"
    ) as mock_get, patch(
        "qlicS.exp_sequence_controller.get_scattering"
    ) as mock_get_scattering, patch(
        "qlicS.sim_controller.pylion_dumping"
    ) as mock_pylion_dumping, patch(
        "qlicS.exp_sequence_controller.pylion_cloud"
    ) as mock_pylion_cloud, patch(
        "qlicS.exp_sequence_controller.gen_trap_lammps"
    ) as mock_gen_trap_lammps, patch(
        "qlicS.exp_sequence_controller.create_cooling_laser"
    ) as mock_create_cooling_laser, patch(
        "qlicS.exp_sequence_controller.evolve"
    ) as mock_evolve, patch(
        "qlicS.exp_sequence_controller.create_tickle"
    ) as mock_create_tickle:
        mock_get.side_effect = [input_sequence,"['be+', 'some_value']"]
        mock_functions = {
            "pylion_dumping": mock_pylion_dumping,
            "pylion_cloud": mock_pylion_cloud,
            "gen_trap_lammps": mock_gen_trap_lammps,
            "create_cooling_laser": mock_create_cooling_laser,
            "evolve": mock_evolve,
            "create_tickle": mock_create_tickle,
        }

        if input_sequence == "invalid_command" or input_sequence == "":
            with pytest.raises(ValueError):
                create_and_run_sim_gen()
        else:
            create_and_run_sim_gen()
            mock_get_scattering.assert_called_once()

        print(expected_calls)
        # sourcery skip: no-loop-in-tests
        for func_name, _args in expected_calls:
            mock_functions[func_name].assert_called_once()
