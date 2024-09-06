import pytest
from unittest.mock import MagicMock, patch

from qlicS.exp_sequence_controller import append_iter


# TODO also check that we are scanning the variables correctly
# FIXME this is a broken test that needs to be fixed carefully
@pytest.mark.parametrize(
    "iter_config, config_ids, expected_calls",
    [
        (
            [
                (
                    "scan_objects",
                    '["modulation_0", "scattering_laser", "cooling_laser_0"]',
                ),
                ("scan_var", '["modulation_0", "frequency"]'),
                (
                    "scan_var_seq",
                    "[500000, 600000, 650000, 700000, 710000, 715000, 720000, 725000, 730000, 750000, 800000, 900000]",
                ),
                ("iter_timesequence", "[[1e-08, 1e5], [1e-09, 1e6], [1e-08, 20000]]"),
                ("iter_detection_seq", "[[1e5, 1.1e6]]"),
                ("com_list", "tickle,evolve,evolve,cooling_laser,evolve"),
            ],
            "3",
            [["create_tickle", "evolve", "evolve", "cooling_laser", "evolve"] * 12],
        )
    ],
    ids=["path1"],
)
def test_iter_appending(iter_config, config_ids, expected_calls):
    pylion_dumping = MagicMock(name="pylion_dumping")
    pylion_cloud = MagicMock(name="pylion_cloud")
    gen_trap_lammps = MagicMock(name="gen_trap_lammps")
    create_cooling_laser = MagicMock(name="create_cooling_laser")
    evolve = MagicMock(name="evolve")
    create_tickle = MagicMock(name="create_tickle")

    with patch(
        "qlicS.exp_sequence_controller.configur.items", return_value=iter_config
    ), patch(
        "qlicS.exp_sequence_controller.give_command_mapping",
        return_value={
            "dumping": pylion_dumping,
            "cloud": pylion_cloud,
            "trap": gen_trap_lammps,
            "cooling_laser": create_cooling_laser,
            "evolve": evolve,
            "tickle": create_tickle,
        },
    ), patch(
        "qlicS.exp_sequence_controller.configur.get", return_value=config_ids
    ), patch(
        "qlicS.exp_sequence_controller.configur.set"
    ):
        mock_s = MagicMock()

        append_iter(mock_s)
        all_append_args = [
            call[0][0]._extract_mock_name()
            for call in mock_s.append.call_args_list
            if not isinstance(call[0][0], dict)
        ]

        mock_e_calls = []
        # sourcery skip: no-loop-in-tests
        for e_call in expected_calls[0]:
            # sourcery skip: no-conditionals-in-tests
            if e_call == "create_tickle":
                mock_e_calls.append(create_tickle()._extract_mock_name())
            elif e_call == "evolve":
                mock_e_calls.append(evolve()._extract_mock_name())
            elif e_call == "cooling_laser":
                mock_e_calls.append(create_cooling_laser()._extract_mock_name())
        # TODO add the others here as well
        print(all_append_args)
        print(mock_e_calls)

        assert all_append_args == mock_e_calls
