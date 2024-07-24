# Imports for python 2 compatibility

from __future__ import absolute_import, division, print_function

__metaclass__ = type


# Imports for M-LOOP

import time
import signal

import mloop.controllers as mlc
import mloop.interfaces as mli
import mloop.visualizations as mlv
import mloop.learners as mlr
import numpy as np

from .cl_console import run_from_file


class CustomInterface(mli.Interface):
    def __init__(self, experiment_dir):
        super(CustomInterface, self).__init__()
        self.experiment_dir = experiment_dir

    def get_next_cost_dict(self, params_dict):
        params = params_dict["params"]

        scat = run_from_file(
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
        bad = False
        return {"cost": cost, "uncer": uncer, "bad": bad}



def mainmloop(experiment_dir):

    # M-LOOP can be run with three commands

    # First create your interface

    interface = CustomInterface(experiment_dir=experiment_dir)

    # Next create the controller. Provide it with your interface and any options you want to set
    # NOTE:
    controller = mlc.create_controller(
        interface,
        "neural_net",
        max_num_runs=50,
        param_names=['Num of Be', 'V_DC'],
        num_params=2,
        min_boundary=[1, 0],
        max_boundary=[20, 2.5],
        no_delay=False,
    )

    # To run M-LOOP and find the optimal parameters just use the controller method optimize

    controller.optimize()

    # The results of the optimization will be saved to files and can also be accessed as attributes of the controller.

    print("Best parameters found:")

    print(controller.best_params)

    # You can also run the default sets of visualizations for the controller with one command

    #mlv.show_all_default_visualizations(controller)
    #mlv.NeuralNetVisualizer()
    c_arch = controller.total_archive_filename
    def swap_controller_to_archive(input_string):
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
            return input_string  # Return the original string if "controller" is not found

    l_arch = swap_controller_to_archive(c_arch)
    print(c_arch + '\n' + l_arch)
    # TODO check here that l_arch dir exists for safety
    best_vis = False
    try:
        mlv.show_all_default_visualizations(controller)
        best_vis = True
    except Exception as e:
        print(e)
        print("A possible problem I have had in the past is using # or other special characters in param names.")
    if not best_vis:
        print('trying')
        mlv.create_controller_visualizations(c_arch) # TODO this is not working
    