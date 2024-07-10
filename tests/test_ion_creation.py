from unittest.mock import patch

import pytest

from qlicS.ion_creation import pylion_cloud


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
