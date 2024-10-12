from qlicS.cl_console import run_from_file

import mloop.controllers as mlc
import numpy as np


def get_run_info(experiment_dir, params) -> dict:

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
