from mock import patch

import pytest

from qlicS.trap import gen_trap_lammps

from .resources import check_string_format

# Objects

test_trap = {
    "radius": str(3.75e-3),
    "length": str(2.75e-3),
    "kappa": str(0.244),
    "frequency": str(3.850000e6),
    "voltage": str(500),
    "endcapvoltage": str(15),
    "pseudo": str(True),
}
float_pattern = r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
int_pattern = r"\d+"
expected_pattern = (
    rf"\n# Pseudopotential approximation for Linear Paul trap\.\.\. \(fixID={int_pattern}\)"
    rf"\n# SHO"
    rf"variable k_x{int_pattern}\t\tequal {float_pattern}"
    rf"variable k_y{int_pattern}\t\tequal {float_pattern}"
    rf"variable k_z{int_pattern}\t\tequal {float_pattern}"
    rf"variable fX{int_pattern} atom \"-v_k_x{int_pattern} \* x\""
    rf"variable fY{int_pattern} atom \"-v_k_y{int_pattern} \* y\""
    rf"variable fZ{int_pattern} atom \"-v_k_z{int_pattern} \* z\""
    rf"variable E{int_pattern} atom "
    rf"\"v_k_x{int_pattern} \* x \* x /\s+"
    rf"2 \+ v_k_y{int_pattern} \* y \* y / 2 \+"
    rf" v_k_z{int_pattern} \* z \* z / 2\""
    rf"fix {int_pattern} all addforce\s+v_fX{int_pattern}"
    rf" v_fY{int_pattern} v_fZ{int_pattern} energy v_E{int_pattern}\n"
)

# Basic Test


# Happy path tests with test values
@pytest.mark.parametrize(
    "ions, trap_pos, trap_config, expected_result",
    [
        ({"mass": 9, "charge": 1}, 0, test_trap.items(), expected_pattern),
    ],
    ids=["single_ion"],
)
def test_gen_trap_lammps_happy_path(ions, trap_pos, trap_config, expected_result):
    # Arrange
    with patch("qlicS.trap.configur.items", return_value=trap_config):
        # Act
        result = gen_trap_lammps(ions, trap_pos)
        # print(''.join(result['code'][0]))
        # print(expected_result)
        # assert check_string_format(''.join(result['code'][0]), expected_result)
        print(type(result["code"][0]))
        print(expected_result)
        assert check_string_format("".join(result["code"]), expected_result) is True


# TODO Various conservation of energy, secular motion type tests
