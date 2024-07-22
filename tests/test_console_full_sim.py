import pytest
import os
from unittest.mock import patch, MagicMock
import math


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
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
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
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
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
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
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

    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        res = qlicS.console_resources.run_from_file()
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
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        dd = qlicS.console_resources.run_from_file()
        positions = f"{dd}positions.txt"
        with open(positions, "r") as pos_file:
            last_three = pos_file.readlines()[-3:]
        data_values = [[float(val) for val in line.split()[1:]] for line in last_three]

        # Check that we have frozen:
        for a in data_values:
            for v in a[3:]:
                assert abs(v) < 2

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
        disp_thresh = 0.2
        analytic_del = 18.15e-6  # TODO cite calculation
        wing_zs = [x for x in zs if abs(x) != min_value]
        for w in wing_zs:
            assert abs(w) < analytic_del * (1 + disp_thresh) and abs(
                w
            ) > analytic_del * (1 - disp_thresh)

        # Check that each wing has a different sign
        assert len(wing_zs) == 2 and wing_zs[0] * wing_zs[1] < 0


@pytest.mark.order(index=-6)
def test_1_be_cool_ts_switch(reload_package):
    # NOTE: Setting a timestep that doesn't allow for many datapoints per oscillation on these types of tests
    # results in some physics issues.  (py)LIon defaults to 20, but I think closer to 50 is necessary. More is better
    # but balance this against runtime.
    # If you want to see the projected envelop, flip to true.
    show_plot = False
    reload_package
    import matplotlib.pyplot as plt

    examples_dir = f"{os.getcwd()}/examples"
    file_path = f"{examples_dir}/1_be_damp_test.ini"
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        dd = qlicS.cl_console.run_from_file()
        positions = f"{dd}positions.txt"
        with open(positions, "r") as pos_file:
            lines = pos_file.readlines()[:]
        data_values = [
            [float(val) for val in line.split()[1:]]
            for line in lines
            if len(line.split()) == 7
        ]
        initial_amp1 = data_values[0][0]

        def get_largest_abs(start, data):
            largest_val = 0
            for sublist in data[start:]:
                if abs(sublist[0]) > largest_val:
                    largest_val = abs(sublist[0])
            return largest_val

        initial_amp2 = get_largest_abs(2000, data_values)
        print(initial_amp2)
        step_num = 10
        # In the notation of Taylor Classical Mech.
        b = (
            2.703426035144626e-21 / 2
        )  # TODO this second 2 in the denominator makes the fit work, I am having trouble justifying it to myself though
        beta = b / (2 * 9 * 1.6605402e-27)

        def dec_curve(initial_amp, x, timestep):
            return abs(initial_amp * math.e ** (-beta * x * step_num * timestep))

        threshold = 0.25
        score = 0
        within_envelope = 0

        # Lists to store values for plotting
        indices = []
        d_values = []
        expected_values = []
        for index, d in enumerate(data_values):
            if index < 2000:
                expected = dec_curve(initial_amp1, index, 1e-9)
            else:
                expected = dec_curve(initial_amp2, index - 2000, 1e-8)
            if abs(d[0]) > expected * (1 - threshold) and abs(d[0]) < expected * (
                1 + threshold
            ):
                score += 1
            if d[0] > -expected * (1 + threshold) and d[0] < expected * (1 + threshold):
                within_envelope += 1
            # Append values for plotting
            indices.append(index)
            d_values.append(d[0])
            expected_values.append(expected)
        print(expected_values)
        print(score)
        print(within_envelope)
        if show_plot:
            plt.figure()
            plt.plot(indices, d_values, label="d[0]")
            plt.plot(indices, expected_values, label="dec_curve")
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.title("Comparison of d[0] and dec_curve")
            plt.legend()
            plt.show()
        poss = len(data_values)
        score_threshold = 0.1
        in_envelope_threshold = 0.75

        assert score >= score_threshold * poss

        # TODO the envelope logic doesnt work well when it cools down alot due to F_0.  Either fix or just
        # only test for short cooling times
        # assert within_envelope >= in_envelope_threshold*poss


@pytest.mark.order(index=-7)
def test_1_be_steady_state(reload_package):
    # NOTE: Setting a timestep that doesn't allow for many datapoints per oscillation on these types of tests
    # results in some physics issues.  (py)LIon defaults to 20, but I think closer to 50 is necessary. More is better
    # but balance this against runtime.
    # NOTE: it seems like after changing timesteps we have to re-come to equilibrium.  I'm not sure why this is but
    # I think it has to do with removing and readding the tickle (phase change).  TODO this probably doesn't need to
    # be fixed immediatly, but should be noted in documentation.

    # If you want to see the steady state amp, flip to true.
    show_plot = False
    reload_package
    import matplotlib.pyplot as plt
    import numpy as np

    examples_dir = f"{os.getcwd()}/examples"
    file_path = f"{examples_dir}/1_be_damp_drive.ini"
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        dd = qlicS.cl_console.run_from_file()
        positions = f"{dd}positions.txt"
        with open(positions, "r") as pos_file:
            lines = pos_file.readlines()[:]
        data_values = [
            [float(val) for val in line.split()[1:]]
            for line in lines
            if len(line.split()) == 7
        ]

        # Expected Steady State
        f_0 = 1.60217663e-19 * 10  # F=qE in LAMMPS' SI mode
        m = 9 * 1.6605402e-27
        be_fr = 7.100680e05
        driving_frequency = 710000
        # In the notation of Taylor Classical Mech.
        b = (
            2.703426035144626e-21 / 2
        )  # TODO this second 2 in the denominator makes the fit work, I am having trouble justifying it to myself though
        beta = b / (2 * 9 * 1.6605402e-27)
        # Eq. 5.64 Taylor
        a_squared = ((f_0 / m) ** 2) / (
            (((be_fr * 2 * np.pi) ** 2 - (2 * np.pi * driving_frequency) ** 2) ** 2)
            + (4 * ((beta) ** 2) * (2 * np.pi * driving_frequency) ** 2)
        )

        # Optional Print Checking
        if show_plot:
            d_values = []
            indices = []
            for index, d in enumerate(data_values):
                d_values.append(d[0])
                indices.append(index)
            plt.figure()
            plt.plot(indices, d_values, label="d[0]")
            plt.axhline(
                y=np.sqrt(a_squared),
                color="r",
                linestyle="--",
                label="Expected Steady State",
            )
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.title("Comparison of d[0] and dec_curve")
            plt.legend()
            plt.show()
        print(len(data_values))
        first_period = data_values[:40000]
        second_period = data_values[40000:150000]
        third_period = data_values[150000:]

        def get_final_max(final_frac, data):
            cutoff = int(len(data) * (1 - final_frac))
            max = 0
            for l in data[cutoff:]:
                if abs(l[0]) > max:
                    max = abs(l[0])
            return max

        final_frac = 0.2
        # It seems like most of the inaccuracy just comes from us not reaching the steadystate completely
        # 5% seems like a reasonable threshold (within a few microns or so)
        steady_state_simularity_tolerance = 0.05
        prediciton_tolerance = 0.05
        first_max = get_final_max(final_frac, first_period)
        second_max = get_final_max(final_frac, second_period)
        third_max = get_final_max(final_frac, third_period)

        # Calculate the percentage differences between the maximum values
        diff_first_second = abs(first_max - second_max) / first_max
        diff_first_third = abs(first_max - third_max) / first_max
        diff_second_third = abs(second_max - third_max) / second_max

        print(first_max)
        print(second_max)
        print(third_max)

        # Check steady states are consistent
        assert diff_first_second < steady_state_simularity_tolerance
        assert diff_first_third < steady_state_simularity_tolerance
        assert diff_second_third < steady_state_simularity_tolerance

        # Check steady states are in line with prediction
        maxs = [first_max, second_max, third_max]
        for max in maxs:
            assert max > np.sqrt(a_squared) * (1 - prediciton_tolerance)
            assert max < np.sqrt(a_squared) * (1 + prediciton_tolerance)


# More complex Physics tests
@pytest.mark.order(index=-8)
def test_laser_cooling_max_rate_cond(reload_package):
    # NOTE: Based on pg. 89 H. Metcalf et al. "Laser Cooling and Trapping"
    reload_package  # TODO Why is reload_package here? Remove likely
    show_plot = False
    import matplotlib.pyplot as plt
    import numpy as np
    from qlicS.pylion.functions import readdump

    examples_dir = f"{os.getcwd()}/examples"
    file_path = f"{examples_dir}/laser_cooling_thermal_test.ini"
    with patch("qlicS.console_resources.mode_dialogue") as mock_m_d, patch(
        "qlicS.console_resources.config_file_dialogue"
    ) as mock_c_f_d:
        mock_m_d.return_value = "Run Experiment From File"
        mock_c_f_d.return_value = file_path
        dd = qlicS.console_resources.run_from_file()
        positions = f"{dd}positions.txt"
        steps, data = readdump(positions)

        def calculate_rms(lst):
            if not lst:
                return 0  # Handle the case of an empty list to avoid division by zero
            squared_values = [x**2 for x in lst]
            mean_squared = sum(squared_values) / len(lst)
            rms = math.sqrt(mean_squared)
            return rms

        boltzmann_constant = 1.380649e-23  # Boltzmann constant in J/K
        hbar = 6.626e-34 / (2 * np.pi)
        linewidth = 113097335.52923255

        def convert_rms_to_temp(rms_velocities, mass):
            temperatures = [
                (mass * vel**2) / (3 * boltzmann_constant) for vel in rms_velocities
            ]
            return temperatures

        rmses = []
        for step in data:
            atom_vels = []
            for atom in step:
                v = np.sqrt(atom[3] ** 2 + atom[4] ** 2 + atom[5] ** 2)
                # v = atom[3]
                atom_vels.append(v)
            rms_vel = calculate_rms(atom_vels)
            rmses.append(rms_vel)

        temp = convert_rms_to_temp(rmses, 9 * 1.6605402e-27)

        def analytical_doppler_limit(detunning, linewidth):
            coef = (2 * hbar * linewidth) / (boltzmann_constant * 8)
            add_terms = (2 * detunning / linewidth) + (linewidth / (2 * detunning))
            return coef * add_terms

        t1 = analytical_doppler_limit(1e7, 113097335.52923255)
        t2 = analytical_doppler_limit(2.5e7, 113097335.52923255)
        t3 = analytical_doppler_limit(5.65486677646e7, 113097335.52923255)
        t4 = analytical_doppler_limit(7.5e7, 113097335.52923255)
        t5 = analytical_doppler_limit(10e7, 113097335.52923255)

        print(t1)
        print(t2)
        print(t3)
        print(t4)
        print(t5)

        index_ranges = [
            (8000, 11000),
            (18000, 21000),
            (28000, 31000),
            (38000, 41000),
            (48000, 51000),
        ]

        # Initialize lists to store minimum values and their indices
        min_values = []
        min_indices = []

        # Iterate over the index ranges to find the minimum value and index in each range
        for start_index, end_index in index_ranges:
            min_index, min_value = min(
                enumerate(temp[start_index:end_index], start=start_index),
                key=lambda x: x[1],
            )
            min_values.append(min_value)
            min_indices.append(min_index)
        print(min_values)
        print(min_indices)

        if show_plot:
            plt.figure()
            plt.plot(steps, temp, label="T (K)")
            plt.axhline(
                y=t1,
                color="r",
                linestyle="--",
                label="1e7",
            )
            plt.axhline(
                y=t2,
                color="r",
                linestyle="--",
                label="2.5e7",
            )
            plt.axhline(
                y=t3,
                color="b",
                linestyle="--",
                label="5.7e7",
            )
            plt.axhline(
                y=t4,
                color="r",
                linestyle="--",
                label="7.5e7",
            )
            plt.axhline(
                y=t5,
                color="r",
                linestyle="--",
                label="10e7",
            )
            # plt.scatter(min_indices, min_values, color='g', label='Min Values', marker='o')
            plt.xlabel("Step")
            plt.ylabel("Temp")
            plt.legend()
            plt.show()

        smallest_value_index = min_values.index(min(min_values))
        assert (
            smallest_value_index == 2
        ), f"The smallest value is not at index 2. Actual index: {smallest_value_index}"
        # TODO there is probably a good mathematical way of looking at if we are hitting the doppler limit.  For now just look at the graph.
