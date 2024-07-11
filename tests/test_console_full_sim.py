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

# Basic, check that sim doesn't throw error type tests:

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


@pytest.mark.order(index=-4)
def test_trap(reload_package):
    examples_dir = f"{os.getcwd()}/examples"
    # sourcery skip: no-loop-in-tests

    file_path = f"{examples_dir}/iteration_example.ini"
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

# Simple Physics tests

@pytest.mark.order(index=-5)
def test_be_chirp(reload_package):
    examples_dir = f"{os.getcwd()}/examples"
    reload_package

    file_path = f"{examples_dir}/pure_be_chirp.ini"

    with patch("qlicS.cl_console.mode_dialogue") as mock_m_d, patch(
        "qlicS.cl_console.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        res = qlicS.cl_console.run_from_file()
        smallest_scat_v = res[0][3]
        smallest_scat_f = res[0][2]
        for r in res:
            if r[3] < smallest_scat_v:
                smallest_scat_v = r[3]
                smallest_scat_f = r[2]
        assert smallest_scat_f == 710000

        


# More complex Physics tests
