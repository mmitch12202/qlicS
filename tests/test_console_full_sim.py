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

@pytest.mark.order(index=-6)
def test_3_be_freeze_pos(reload_package):
    reload_package
    examples_dir = f"{os.getcwd()}/examples"
    file_path = f"{examples_dir}/3_be_freeze_positions.ini"
    with patch("qlicS.cl_console.mode_dialogue") as mock_m_d, patch(
            "qlicS.cl_console.config_file_dialogue") as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        dd = qlicS.cl_console.run_from_file()
        positions = f"{dd}positions.txt"
        with open(positions, 'r') as pos_file:
            last_three = pos_file.readlines()[-3:]
        data_values = [[float(val) for val in line.split()[1:]] for line in last_three]

        # Check that we have frozen:
        for a in data_values:
            for v in a[3:]:
                assert abs(v) < 1e-9

        # Get z's
        zs = [a[2] for a in data_values]
        abs_zs = [abs(i) for i in zs]

        # Check that there is one central z
        threshold = 0.2
        min_value = min(abs_zs)
        for val in abs_zs:
            if val != min_value:
                assert min_value / val < threshold

        # Check wing distance
        disp_thresh = .2
        analytic_del = 18.15e-6 # TODO cite calculation
        wing_zs = [x for x in zs if abs(x) != min_value]
        for w in wing_zs:
            assert abs(w) < analytic_del*(1+disp_thresh) and abs(w) > analytic_del*(1-disp_thresh)

        # Check that each wing has a different sign
        assert len(wing_zs) == 2 and wing_zs[0] * wing_zs[1] < 0




# More complex Physics tests
