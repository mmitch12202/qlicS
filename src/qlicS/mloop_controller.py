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

        scat = run_from_file(optimize_mode=True, exp=self.experiment_dir, modulation_0_amp=params[0], cloud_0_count=int(params[1]), scattering_laser_=[0, int(params[1])])
        non_res_list = []
        for s in scat:
            if s[2] == 178000:
                res_count = s[3]
            else:
                non_res_list.append(s[3])
        avg_off_res = sum(non_res_list)/len(non_res_list)
        cost = -abs(res_count-avg_off_res)

        # For now
        uncer = 0
        bad = False
        return {"cost": cost, "uncer": uncer, "bad": bad}



def mainmloop(experiment_dir):

    # M-LOOP can be run with three commands

    # First create your interface

    interface = CustomInterface(experiment_dir=experiment_dir)

    # Next create the controller. Provide it with your interface and any options you want to set

    controller = mlc.create_controller(
        interface,
        max_num_runs=10,
        num_params=2,
        min_boundary=[0, 1],
        max_boundary=[2, 20],
        controller_type='neural_net',
    )

    # To run M-LOOP and find the optimal parameters just use the controller method optimize

    controller.optimize()

    # The results of the optimization will be saved to files and can also be accessed as attributes of the controller.

    print("Best parameters found:")

    print(controller.best_params)

    # You can also run the default sets of visualizations for the controller with one command

    mlv.show_all_default_visualizations(controller)
