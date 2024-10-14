from qlicS.cl_console import run_from_file

import mloop.controllers as mlc
import numpy as np


def get_run_info(experiment_dir, params) -> dict:
<<<<<<< HEAD

    def f_r(mass, ev, charge=1.60217663e-19, kappa=0.17, length=1.5e-3, freq=11.04e6, voltage=66.4, radius=1.25e-3): # defaults based on mass_selective_pruneing.ini
        ar = -4 * charge * kappa * ev / (mass * length**2 * (2 * np.pi * freq) ** 2)
        qr = 2 * charge * voltage / (mass * radius**2 * (2 * np.pi * freq) ** 2)
        wr = 2 * np.pi * freq / 2 * np.sqrt(ar + qr**2 / 2)
        f_xy = wr/2/np.pi
        return f_xy

    amu = 1.6605402e-27

    o2_res = f_r(32*amu, params[2])
    scan_seq = [78000, 100000, 125000, o2_res, 225000, 250000, 278000]

    try:
        scat = run_from_file(
=======
    """
    Retrieves run information and calculates the cost based on simulation results.

    This function executes a simulation using the specified experiment directory and 
    parameters, then analyzes the results to compute a cost value based on the 
    differences between reference and non-reference counts. It returns a dictionary 
    containing the calculated cost, uncertainty, and a flag indicating if the run 
    was successful.

    Args:
        experiment_dir (str): The directory where the experiment data is located.
        params (list): A list of parameters used for the run, where the first two 
            elements represent cloud counts and endcap voltages.

    Returns:
        dict: A dictionary containing the following keys:
            - cost (float): The calculated cost based on the run results.
            - uncer (int): The uncertainty value, currently set to 0.
            - bad (bool): A flag indicating if an error occurred during execution.

    Raises:
        KeyError: If the required parameters are not found in the configuration.
    """
    if scat := run_from_file(
>>>>>>> 114d41d (docstrings)
        optimize_mode=True,
        exp=experiment_dir,
        cloud_0_count=int(round(params[0])),
        cloud_1_count=int(round(params[1])),
        iter_scan_var_seq=scan_seq,
        trap_0_endcapvoltage=params[2],
        trap_1_endcapvoltage=params[2],
        scattering_laser_scattered_ion_indices=[0, int(round(params[0]))]
        )
        non_res_list = []
        res_count = scat[4][3]
        for s in scat:
            if s[3] != res_count: 
                non_res_list.append(s[3])
        res_diffs = [(res_count-i) for i in non_res_list] # Optimizing Peaks
        avg_diff = sum(res_diffs)/len(res_diffs)
        cost = -(avg_diff)
        bad = False
        uncer = np.std(non_res_list)
    except Exception as e:
        bad = True
        cost = 0
        uncer = 0
        print(e)
    return {"cost": cost, "uncer": uncer, "bad": bad}

# TODO probably a better way of dealing with this
def return_controller(interface):
    """
    Creates and returns a controller object for the simulation.

    This function initializes a controller using the specified interface and 
    predefined parameters for a neural network. It sets various configuration 
    options such as the maximum number of runs, parameter names, and boundaries 
    for the parameters, facilitating the control of the simulation process.

    Args:
        interface: The interface to be used for creating the controller.

    Returns:
        Controller: The created controller object configured with the specified parameters.

    Raises:
        ValueError: If the provided interface is invalid or if required parameters are missing.
    """
    # For now just dont touch interface
    return mlc.create_controller(
        interface,
        "neural_net",
        max_num_runs=100,
        param_names=['Num_Be', 'Num_O2', 'V_DC'],
        num_params=3,
        min_boundary=[1, 1, 0,],
        max_boundary=[20, 20, 2.5],
        no_delay=False,
    )
