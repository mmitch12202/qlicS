from unittest.mock import MagicMock, patch

import pytest

from src.qlicS.tickle_efield import create_tickle

# Basic Tests


@pytest.mark.parametrize(
    "config_values, current_dt, test_pos, expected_uid, expected_code",
    [
        # Happy path test case
        (
            {
                "modulation_0": {
                    "frequency": "1.0",
                    "uid": "'test_uid'",
                    "amp": "0.5",
                    "static": "[0.1, 0.2, 0.3]",
                    "Ex0": "1.0",
                    "Exx1": "0.1",
                    "Exx2": "0.01",
                    "Exy1": "0.2",
                    "Exy2": "0.02",
                    "Exz1": "0.3",
                    "Exz2": "0.03",
                    "Ey0": "1.1",
                    "Eyx1": "0.11",
                    "Eyx2": "0.011",
                    "Eyy1": "0.21",
                    "Eyy2": "0.021",
                    "Eyz1": "0.31",
                    "Eyz2": "0.031",
                    "Ez0": "1.2",
                    "Ezx1": "0.12",
                    "Ezx2": "0.012",
                    "Ezy1": "0.22",
                    "Ezy2": "0.022",
                    "Ezz1": "0.32",
                    "Ezz2": "0.032",
                    "x_shift": "0.1",
                    "y_shift": "0.2",
                    "z_shift": "0.3",
                }
            },
            2.0,
            0,
            "test_uid",
            [
                "variable E equal 0.1\n"
                "variable Ex atom (0.5*(1.0+0.1*(x-0.1)+0.01*(x-0.1)^2+0.2*(y-0.2)+"
                "0.02*(y-0.2)^2+0.3*(z-0.3)+0.03*(z-0.3)^2))*"
                "cos((2*3.141592653589793)*2.0*step)\n"
                "variable B equal 0.2\n"
                "variable Ey atom (0.5*(1.1+0.11*(x-0.1)+0.011*(x-0.1)^2+0.21*(y-0.2)+"
                "0.021*(y-0.2)^2+0.31*(z-0.3)+0.031*(z-0.3)^2))*"
                "cos((2*3.141592653589793)*2.0*step)\n"
                "variable C equal 0.3\n"
                "variable Ez atom (0.5*(1.2+0.12*(x-0.1)+0.012*(x-0.1)^2+0.22*(y-0.2)+"
                "0.022*(y-0.2)^2+0.32*(z-0.3)+0.032*(z-0.3)^2))*"
                "cos((2*3.141592653589793)*2.0*step)\n"
                "fix test_uid all efield v_Ex v_Ey v_Ez"
            ],
        ),
        # Edge case: zero frequency
        (
            {
                "modulation_0": {
                    "frequency": "0.0",
                    "uid": "'zero_freq_uid'",
                    "amp": "0.5",
                    "static": "[0.1, 0.2, 0.3]",
                    "Ex0": "1.0",
                    "Exx1": "0.1",
                    "Exx2": "0.01",
                    "Exy1": "0.2",
                    "Exy2": "0.02",
                    "Exz1": "0.3",
                    "Exz2": "0.03",
                    "Ey0": "1.1",
                    "Eyx1": "0.11",
                    "Eyx2": "0.011",
                    "Eyy1": "0.21",
                    "Eyy2": "0.021",
                    "Eyz1": "0.31",
                    "Eyz2": "0.031",
                    "Ez0": "1.2",
                    "Ezx1": "0.12",
                    "Ezx2": "0.012",
                    "Ezy1": "0.22",
                    "Ezy2": "0.022",
                    "Ezz1": "0.32",
                    "Ezz2": "0.032",
                    "x_shift": "0.1",
                    "y_shift": "0.2",
                    "z_shift": "0.3",
                }
            },
            2.0,
            0,
            "zero_freq_uid",
            [
                "variable E equal 0.1\n"
                "variable Ex atom (0.5*(1.0+0.1*(x-0.1)+0.01*(x-0.1)^2+0.2*(y-0.2)+0.02*"
                "(y-0.2)^2+0.3*(z-0.3)+0.03*(z-0.3)^2))*cos((2*3.141592653589793)*0.0*step)\n"
                "variable B equal 0.2\n"
                "variable Ey atom (0.5*(1.1+0.11*(x-0.1)+0.011*(x-0.1)^2+0.21*(y-0.2)+0.021*"
                "(y-0.2)^2+0.31*(z-0.3)+0.031*(z-0.3)^2))*cos((2*3.141592653589793)*0.0*step)\n"
                "variable C equal 0.3\n"
                "variable Ez atom (0.5*(1.2+0.12*(x-0.1)+0.012*(x-0.1)^2+0.22*(y-0.2)+0.022*"
                "(y-0.2)^2+0.32*(z-0.3)+0.032*(z-0.3)^2))*cos((2*3.141592653589793)*0.0*step)\n"
                "fix zero_freq_uid all efield v_Ex v_Ey v_Ez"
            ],
        ),
    ],
    ids=["happy_path", "zero_frequency"],
)
def test_create_tickle(
    config_values, current_dt, test_pos, expected_uid, expected_code
):
    # Arrange
    mock_configur = MagicMock()
    mock_configur.get.side_effect = lambda section, key: config_values[section][key]

    # Act
    with patch("src.qlicS.tickle_efield.configur", mock_configur), patch(
        "src.qlicS.tickle_efield.get_current_dt", return_value=current_dt
    ):
        if isinstance(expected_code, list):
            result = create_tickle(test_pos)

            # Assert
            assert result["uid"] == expected_uid
            assert result["code"] == expected_code
        else:
            with expected_code:
                create_tickle(test_pos)


# TODO conservative field test - particle conserves energy as it travels in
# the modulating field
# TODO untrapped particle test - particle moves at the frequency
# of a time-oscillating field
# TODO maybe single particle test - that we can in fact hit resonance
# for a single arbitrary ion in a pseudopotential
