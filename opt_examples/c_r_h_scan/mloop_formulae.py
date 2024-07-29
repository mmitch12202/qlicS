from qlicS.cl_console import run_from_file

import mloop.controllers as mlc
import numpy as np


def get_run_info(experiment_dir, params) -> dict:
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
