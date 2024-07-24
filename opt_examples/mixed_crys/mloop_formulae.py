from qlicS.cl_console import run_from_file

import mloop.controllers as mlc


def get_run_info(experiment_dir, params) -> dict:
    scat = run_from_file(
        optimize_mode=True,
        exp=experiment_dir, 
        modulation_0_amp=params[0], 
        cloud_1_count=int(params[1]), 
        cloud_0_count=int(params[2]), 
        scattering_laser_scattered_ion_indices=[0, int(params[2])]
        )
    non_res_list = []
    for s in scat:
        if s[2] == 178000: #FIXME
            res_count = s[3]
        else:
            non_res_list.append(s[3])
    avg_off_res = sum(non_res_list)/len(non_res_list)
    cost = -abs(res_count-avg_off_res)
    uncer = 0
    bad = False
    return {"cost": cost, "uncer": uncer, "bad": bad}

# TODO probably a better way of dealing with this
def return_controller(interface):
    # For now just dont touch interface
    return mlc.create_controller(
        interface,
        "neural_net",
        max_num_runs=12,
        param_names=['Tickle amp', 'Num O2+', 'Num Be+'],
        num_params=3,
        min_boundary=[0, 1, 1],
        max_boundary=[1, 20, 20],
        no_delay=False,
    )
