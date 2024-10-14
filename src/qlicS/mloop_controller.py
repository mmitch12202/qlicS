# Imports for python 2 compatibility

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import signal
import time

import mloop.controllers as mlc
import mloop.interfaces as mli
import mloop.learners as mlr
import mloop.visualizations as mlv
import numpy as np

from .cl_console import run_from_file


def get_function_from_file(file_path, function_name):
    """
    Loads a function from a specified file and returns it.

    This function dynamically imports a module from a given file path and retrieves 
    a specified function by name. It allows for the execution of functions defined 
    in external Python files, facilitating modular programming and code reuse.

    Args:
        file_path (str): The path to the Python file from which to load the function.
        function_name (str): The name of the function to retrieve from the module.

    Returns:
        function: The function object retrieved from the specified module.

    Raises:
        AttributeError: If the specified function is not found in the module.
    """

    # Load the module from the file path
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Access the function from the module
    if hasattr(module, function_name):
        return getattr(module, function_name)
    else:
        raise AttributeError(f"Function '{function_name}' not found in the module")


class CustomInterface(mli.Interface):
    """
    Custom interface for managing experiments in the M-LOOP framework.

    This class extends the base interface to provide functionality for 
    managing and executing experiments. It initializes with a specified 
    experiment directory and a file path for formulae, allowing for 
    dynamic retrieval of run information.

    Args:
        experiment_dir (str): The directory where the experiment data is stored.
        formulae_filepath (str): The file path to the formulae used for run information.

    Methods:
        get_next_cost_dict(params_dict): Retrieves the next cost dictionary based on 
        the provided parameters, utilizing the run information function.
    """

    def __init__(self, experiment_dir, formulae_filepath):
        super(CustomInterface, self).__init__()
        self.experiment_dir = experiment_dir
        self.get_run_info = get_function_from_file(formulae_filepath, "get_run_info")

    def get_next_cost_dict(self, params_dict):
        """
        Calculates the next cost dictionary based on provided parameters.

        This method retrieves the parameters from the given dictionary and uses 
        them to obtain the next cost for the simulation. It interacts with the 
        run information function to gather necessary data for cost calculation.

        Args:
            params_dict (dict): A dictionary containing parameters for the simulation, 
                specifically under the key "params".

        Returns:
            dict: The next cost dictionary based on the current parameters.

        Raises:
            KeyError: If the "params" key is not found in the provided dictionary.
        """

        params = params_dict["params"]

        """ scat = run_from_file(
            optimize_mode=True, 
            exp=self.experiment_dir,
            scattering_laser_scattered_ion_indices=[0, int(round(params[0]))],
            cloud_0_count=int(round(params[0])), 
            trap_0_endcapvoltage=params[1], 
            trap_1_endcapvoltage=params[1]
            )
        non_res_list = []
        for s in scat:
            if s[2] == 178000:
                res_count = s[3]
            else:
                non_res_list.append(s[3])
        avg_off_res = sum(non_res_list)/len(non_res_list)
        cost = -abs(res_count-avg_off_res)

        #cost = -np.sum(np.sinc(params[0] - 10)+np.sinc(params[1] + 15))

        # For now
        uncer = 0
        bad = False """

        return self.get_run_info(self.experiment_dir, params)


def mainmloop(experiment_dir, mloop_formulae_file):
    """
    Runs the M-LOOP optimization process for the specified experiment.

    This function initializes the M-LOOP framework by creating a custom interface 
    and a controller based on the provided experiment directory and formulae file. 
    It executes the optimization process to find the best parameters and handles 
    visualization of the results.

    Args:
        experiment_dir (str): The directory where the experiment data is stored.
        mloop_formulae_file (str): The file path to the M-LOOP formulae used for optimization.

    Returns:
        None: This function does not return a value; it performs the optimization 
        and visualizations directly.

    Raises:
        FileNotFoundError: If the specified formulae file does not exist.
        ValueError: If the controller cannot be created or if there are issues 
        during the optimization process.
    """


    # M-LOOP can be run with three commands

    # First create your interface

    interface = CustomInterface(
        experiment_dir=experiment_dir, formulae_filepath=mloop_formulae_file
    )

    # Next create the controller. Provide it with your interface and any options you want to set
    # NOTE:
    """ controller = mlc.create_controller(
        interface,
        "neural_net",
        max_num_runs=50,
        param_names=['Num of Be', 'V_DC'],
        num_params=2,
        min_boundary=[1, 0],
        max_boundary=[20, 2.5],
        no_delay=False,
    ) """
    return_controller = get_function_from_file(mloop_formulae_file, "return_controller")
    controller = return_controller(interface)

    # To run M-LOOP and find the optimal parameters just use the controller method optimize

    controller.optimize()

    # The results of the optimization will be saved to files and can also be accessed as attributes of the controller.

    print("Best parameters found:")

    print(controller.best_params)

    # You can also run the default sets of visualizations for the controller with one command

    # mlv.show_all_default_visualizations(controller)
    # mlv.NeuralNetVisualizer()
    c_arch = controller.total_archive_filename

    def swap_controller_to_archive(input_string):
        """
        Replaces the last occurrence of 'controller' with 'learner' in a string.

        This function searches for the last instance of the word "controller" in the 
        provided input string and replaces it with "learner". If "controller" is not 
        found, the original string is returned unchanged.

        Args:
            input_string (str): The string in which to replace the word.

        Returns:
            str: The modified string with the last occurrence of "controller" replaced 
            by "learner", or the original string if "controller" is not found.
        """

        # Find the last index of "controller" in the string
        last_index = input_string.rfind("controller")

        if last_index != -1:
            # Replace the last instance of "controller" with "learner"
            modified_string = (
                f"{input_string[:last_index]}learner"
                + input_string[last_index + len("controller") :]
            )
            return modified_string
        else:
            return (
                input_string  # Return the original string if "controller" is not found
            )

    l_arch = swap_controller_to_archive(c_arch)
    print(c_arch + "\n" + l_arch)
    # TODO check here that l_arch dir exists for safety
    best_vis = False
    try:
        mlv.show_all_default_visualizations(controller)
        best_vis = True
    except Exception as e:
        print(e)
        print(
            "A possible problem I have had in the past is using # or other special characters in param names."
        )
    if not best_vis:
        print("trying")
        mlv.create_controller_visualizations(c_arch)  # TODO this is not working
