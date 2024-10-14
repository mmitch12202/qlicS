from qlicS.cl_console import run_from_file

import mloop.controllers as mlc
import numpy as np


def get_run_info(experiment_dir, params) -> dict:
    def get_run_info(experiment_dir, params) -> dict:
        """
        Retrieves run information for a given experiment directory and parameters.

        This function executes a run using specified parameters and calculates a cost based 
        on the differences between a reference count and non-reference counts. It returns a 
        dictionary containing the cost, uncertainty, and a flag indicating if an error occurred.

        Args:
            experiment_dir: The directory where the experiment data is located.
            params: A list of parameters used for the run, where the first two elements 
                    represent cloud counts.

        Returns:
            A dictionary with the following keys:
                - cost: The calculated cost based on the run results.
                - uncer: The uncertainty value, currently set to 0.
                - bad: A boolean flag indicating if an error occurred during execution.
        """

    try:
        scat = run_from_file(
        optimize_mode=True,
        exp=experiment_dir,
        cloud_0_count=int(round(params[0])),
        cloud_1_count=int(round(params[1])),
        scattering_laser_scattered_ion_indices=[0, int(round(params[0]))]
    )
        non_res_list = []
        for s in scat:
            if s[2] == 204000: 
                res_count = s[3]
            else:
                non_res_list.append(s[3])
        res_diffs = [abs(res_count-i) for i in non_res_list]
        avg_diff = sum(res_diffs)/len(res_diffs)
        cost = -(avg_diff)
        bad = False
    except Exception as e:
        print(e)
        cost = 0
        bad = True
    uncer = 0
    return {"cost": cost, "uncer": uncer, "bad": bad}

# TODO probably a better way of dealing with this
def return_controller(interface):
    """
    Creates and returns a controller object for the simulation.

    This function initializes a controller using the specified interface and 
    predefined parameters for a neural network. It sets various configuration 
    options such as maximum duration, parameter names, and boundaries for the 
    parameters, facilitating the control of the simulation process.

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
        max_duration=50400,
        param_names=['Num Be+', 'Num O2+'],
        num_params=2,
        min_boundary=[1, 1,],
        max_boundary=[20, 20],
        no_delay=False,
    )
