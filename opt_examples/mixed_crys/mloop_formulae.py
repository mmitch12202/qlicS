from qlicS.cl_console import run_from_file

import mloop.controllers as mlc


def get_run_info(experiment_dir, params) -> dict:
    scat = run_from_file(
        optimize_mode=True,
        exp=experiment_dir, 
        cloud_0_count=int(round(params[0])), 
        trap_0_endcapvoltage=params[1], 
        trap_1_endcapvoltage=params[1],
        scattering_laser_scattered_ion_indices=[0, int(round(params[0]))]
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
        param_names=['Num Be+', 'V_DC'],
        num_params=2,
        min_boundary=[1, 0],
        max_boundary=[20, 2.5],
        no_delay=False,
    )
