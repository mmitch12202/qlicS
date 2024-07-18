from unittest.mock import patch

import pytest

from qlicS.ion_creation import pylion_cloud, recloud_spherical


# Helpers


def configur_side_kick(s: str, t: str) -> dict:
    if s == "ions":
        if t == "h+":
            return "{'mass': 1, 'charge': 1}"
        elif t == "he++":
            return "{'mass': 4, 'charge': 2}"


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "type_pos, uid, species, ion_data, radius, count, expected",
    [
        (
            0,
            "1",
            "h+",
            "[{'mass': 1, 'charge': 1}]",
            "0.5",
            "100",
            {"mass": 1, "charge": 1, "positions": [None] * 100},
        ),
        (
            0,
            "1",
            "he++",
            "[{'mass': 4, 'charge': 2}]",
            "1",
            "200",
            {"mass": 4, "charge": 2, "positions": [None] * 200},
        ),
    ],
    ids=["hydrogen_ion_cloud", "helium_ion_cloud"],
)
def test_pylion_cloud_happy_path(
    type_pos, uid, species, ion_data, radius, count, expected
):

    # Arrange
    with patch("qlicS.ion_creation.configur.get") as mock_get:
        mock_get.side_effect = [species, ion_data, radius, count, uid]

        # Act
        result = pylion_cloud(type_pos)
        print(result)
        # Assert
        assert result["mass"] == expected["mass"]
        assert result["charge"] == expected["charge"]
        assert len(result["positions"]) == len(expected["positions"])
        mock_get.assert_any_call("ions", species)
        mock_get.assert_any_call(f"ion_cloud_{type_pos}", "radius")
        mock_get.assert_any_call(f"ion_cloud_{type_pos}", "count")

@pytest.mark.parametrize(
    "type_pos, uid, config_values, expected_number, expected_radius, expected_code",
    [
        # Happy path tests
        ("type1", 1, {"count": "5", "radius": "10", "initial_atom_id": "1"}, 5, 10, 5),
        ("type2", 2, {"count": "3", "radius": "20", "initial_atom_id": "1"}, 3, 20, 3),
        
        # Edge cases
        ("type3", 3, {"count": "0", "radius": "5", "initial_atom_id": "100"}, 0, 5, 0),
        ("type4", 4, {"count": "1", "radius": "0", "initial_atom_id": "0"}, 1, 0, 1),
        
        # Error cases
        ("type5", 5, {"count": "invalid", "radius": "10"}, None, None, None),
        ("type6", 6, {"count": "5", "radius": "invalid"}, None, None, None),
    ],
    ids=[
        "happy_path_type1",
        "happy_path_type2",
        "edge_case_zero_count",
        "edge_case_zero_radius",
        "error_invalid_count",
        "error_invalid_radius",
    ]
)
def test_recloud_spherical(type_pos, uid, config_values, expected_number, expected_radius, expected_code):
    
    # Arrange
    def mock_get(section, option):
        return config_values.get(option)
    
    with patch("qlicS.ion_creation.configur.get", side_effect=mock_get):
        
        # Act
        if expected_number is None or expected_radius is None:
            with pytest.raises((SyntaxError, NameError, TypeError)):
                recloud_spherical(uid)
        else:
            result = recloud_spherical(uid)
            
            # Assert
            assert len(result['code']) == expected_code + 1  # +1 for the initial comment line
            assert result['code'][0] == "\n# Reset the position of the ions"
            for line in result['code'][1:]:
                assert line.startswith("set atom")
                assert "x" in line and "y" in line and "z" in line





