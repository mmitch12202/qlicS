import pytest
import os
from unittest.mock import patch, MagicMock

# TODO we are only checking the most primative, sim doesnt throw error case - make this better

# Did some hacky things to prevent cross-talk between tests, this may just be inherint of full
# Sim testing though
@pytest.fixture()
def reload_package():
    global qlicS  # reach the global scope
    import sys

    loaded_package_modules = [
        key for key, value in sys.modules.items() if "qlicS" in str(value)
    ]
    for key in loaded_package_modules:
        del sys.modules[key]
    from qlicS.exp_sequence_controller import create_and_run_sim_gen
    import qlicS.cl_console

    yield  # run test

    # delete all modules from package
    loaded_package_modules = [
        key for key, value in sys.modules.items() if "qlicS" in str(value)
    ]
    for key in loaded_package_modules:
        del sys.modules[key]


# TODO set this up so it checks for more specific things - right now all it checks is that the simulations
# dont throw an error.


@pytest.mark.order(index=-1)
def test_cotrap(reload_package):
    examples_dir = f"{os.getcwd()}/examples"
    # sourcery skip: no-loop-in-tests
    reload_package
    file_path = f"{examples_dir}/cotrap_symp_cool.ini"
    with patch("qlicS.cl_console.mode_dialogue") as mock_m_d, patch(
        "qlicS.cl_console.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        print(file_path)
        try:
            qlicS.cl_console.run_from_file()
        except Exception as e:
            assert False, f"An error occurred: {e}"
        else:
            assert True, "No errors were thrown"


@pytest.mark.order(index=-2)
def test_cool_tickle(reload_package):
    examples_dir = f"{os.getcwd()}/examples"
    # sourcery skip: no-loop-in-tests

    file_path = f"{examples_dir}/cotrap_symp_cool.ini"
    with patch("qlicS.cl_console.mode_dialogue") as mock_m_d, patch(
        "qlicS.cl_console.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        print(file_path)
        try:
            qlicS.cl_console.run_from_file()
        except Exception as e:
            assert False, f"An error occurred: {e}"
        else:
            assert True, "No errors were thrown"


@pytest.mark.order(index=-3)
def test_trap(reload_package):
    examples_dir = f"{os.getcwd()}/examples"
    # sourcery skip: no-loop-in-tests

    file_path = f"{examples_dir}/cotrap_symp_cool.ini"
    with patch("qlicS.cl_console.mode_dialogue") as mock_m_d, patch(
        "qlicS.cl_console.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        print(file_path)
        try:
            qlicS.cl_console.run_from_file()
        except Exception as e:
            assert False, f"An error occurred: {e}"
        else:
            assert True, "No errors were thrown"
