# Imports for python 2 compatibility

from __future__ import absolute_import, division, print_function

__metaclass__ = type


# Imports for M-LOOP

import time

import mloop.controllers as mlc
import mloop.interfaces as mli
import mloop.visualizations as mlv
import numpy as np

from .cl_console import run_from_file


class CustomInterface(mli.Interface):
    def __init__(self, experiment_dir):
        super(CustomInterface, self).__init__()
        self.minimum_params = np.array([0, 0.1, -0.1])
        self.experiment_dir = experiment_dir

    def get_next_cost_dict(self, params_dict):
        params = params_dict["params"]

        # Here you can include the code to run your experiment given a particular set of parameters

        # Cost calculation (based on scattering info, hardcoded for now) TODO generalize this at some point

        # TODO figure out how to take input parameters

        scat = run_from_file(optimize_mode=True, exp=self.experiment_dir)
        non_res_list = []
        for s in scat:
            if s[2] == 710000:
                res_count = s[3]
            else:
                non_res_list.append(s[3])
        avg_off_res = sum(non_res_list)/len(non_res_list)

        cost = res_count/avg_off_res

        # There is no uncertainty in our result

        uncer = 0

        # The evaluation will always be a success

        bad = False

        # Add a small time delay to mimic a real experiment

        time.sleep(1)

        # The cost, uncertainty and bad boolean must all be returned as a dictionary

        # You can include other variables you want to record as well if you want

        cost_dict = {"cost": cost, "uncer": uncer, "bad": bad}

        return cost_dict


def mainmloop(experiment_dir):

    # M-LOOP can be run with three commands

    # First create your interface

    interface = CustomInterface(experiment_dir=experiment_dir)

    # Next create the controller. Provide it with your interface and any options you want to set

    controller = mlc.create_controller(
        interface,
        max_num_runs=1000,
        target_cost=-2.99,
        num_params=3,
        min_boundary=[-2, -2, -2],
        max_boundary=[2, 2, 2],
    )

    # To run M-LOOP and find the optimal parameters just use the controller method optimize

    controller.optimize()

    # The results of the optimization will be saved to files and can also be accessed as attributes of the controller.

    print("Best parameters found:")

    print(controller.best_params)

    # You can also run the default sets of visualizations for the controller with one command

    mlv.show_all_default_visualizations(controller)
