import pytest
from unittest.mock import MagicMock, patch

# Import the function to be tested
from qlicS.cl_console import setup_loading_configur
from qlicS.cl_console import get_sim_skeleton_inputs


@pytest.mark.parametrize(
    "loading_config_file, mock_read_call, expected_exception",
    [
        # Happy path tests
        ("config1.ini", True, None),
        ("config2.ini", True, None),
        # Edge cases
        ("", False, FileNotFoundError),
        (None, False, FileNotFoundError),
        # Error cases
        ("invalid_format_file.txt", False, ValueError),
    ],
    ids=[
        "happy_path_config1",
        "happy_path_config2",
        "edge_case_empty_string",
        "edge_case_none",
        "error_case_invalid_format",
    ],
)
def test_setup_loading_configur(
    loading_config_file, mock_read_call, expected_exception
):

    # Arrange
    with patch("qlicS.cl_console.loading_configur.read") as mock_read:
        mock_read.return_value = mock_read_call

        # Act
        if expected_exception:
            with pytest.raises(expected_exception):
                setup_loading_configur(loading_config_file)
        else:
            setup_loading_configur(loading_config_file)

        # Assert
        if not expected_exception:
            mock_read.assert_called_once_with(loading_config_file)
        else:
            mock_read.assert_not_called()


# Mock data for testing
mock_sim_params = [("param1", "value1"), ("param2", "value2")]
mock_detection_params = [("detect1", "value1"), ("detect2", "value2")]


@pytest.mark.parametrize(
    "sim_params, detection_params, expected_sim_params, expected_detection_params",
    [
        pytest.param(
            mock_sim_params,
            mock_detection_params,
            mock_sim_params,
            mock_detection_params,
            id="happy_path",
        ),
        pytest.param([], [], [], [], id="empty_params"),
        pytest.param(
            [("param1", "value1")],
            [("detect1", "value1")],
            [("param1", "value1")],
            [("detect1", "value1")],
            id="single_param",
        ),
    ],
)
def test_get_sim_skeleton_inputs(
    sim_params, detection_params, expected_sim_params, expected_detection_params
):

    # Arrange
    with patch(
        "qlicS.cl_console.loading_configur.items",
        side_effect=[sim_params, detection_params],
    ):

        # Act
        result_sim_params, result_detection_params = get_sim_skeleton_inputs()

        # Assert
        assert result_sim_params == dict(expected_sim_params)
        assert result_detection_params == dict(expected_detection_params)


@pytest.mark.parametrize(
    "side_effect, expected_exception",
    [
        pytest.param(Exception("Config error"), Exception, id="config_error"),
        pytest.param(KeyError("Missing key"), KeyError, id="missing_key"),
    ],
)
def test_get_sim_skeleton_inputs_errors(side_effect, expected_exception):

    # Arrange
    with patch("qlicS.cl_console.loading_configur.items", side_effect=side_effect):

        # Act / Assert
        with pytest.raises(expected_exception):
            get_sim_skeleton_inputs()
