from qlicS.cl_console import run_from_file

import mloop.controllers as mlc
import numpy as np


def get_run_info(experiment_dir, params) -> dict:

    # Because we are varying the endcap potential, we need to recalculate f_res
    # Formulas copied from pylion source:

    def f_r(mass, ev, charge=1.60217663e-19, kappa=0.17, length=1.5e-3, freq=11.04e6, voltage=66.4, radius=1.25e-3): # defaults based on mass_selective_pruneing.ini
        ar = -4 * charge * kappa * ev / (mass * length**2 * (2 * np.pi * freq) ** 2)
        qr = 2 * charge * voltage / (mass * radius**2 * (2 * np.pi * freq) ** 2)
        wr = 2 * np.pi * freq / 2 * np.sqrt(ar + qr**2 / 2)
        f_xy = wr/2/np.pi
        return f_xy

    amu = 1.6605402e-27

    beh2_res = f_r(11*amu, params[1])

    try:
        scat = run_from_file(
        optimize_mode=True,
        exp=experiment_dir,
        modulation_2_amp=params[0],
        trap_0_endcapvoltage=params[1],
        trap_1_endcapvoltage=params[1],
        modulation_1_frequency=beh2_res,
        modulation_2_frequency=beh2_res,
        modulation_3_frequency=beh2_res,
        )

        offresavg = (scat[0][2] + scat[-1][2])/2
        offressig = np.sqrt(((scat[0][2]-offresavg)**2 + (scat[1][2]-offresavg)**2)/2)
        uncer = offressig

        remove_sig = abs(scat[3][2] - scat[1][2]) / offresavg
        # why diff and not standard deev?
        be_loss = abs(scat[0][2] - scat[4][2]) / offresavg

        # arbitrarily decided weights
        c1 = 1
        c2 = 5000

        cost = c1*(-remove_sig) + c2*be_loss
        bad = False
    except Exception as e:
        bad = True
        cost = 0
        uncer = 0
        print(e)
    return {"cost": cost, "uncer": uncer, "bad": bad}

def return_controller(interface):
    # For now just dont touch interface
    return mlc.create_controller(
        interface,
        "neural_net",
        max_num_runs=70,
        param_names=['Tickle_Amp', 'V_DC'],
        num_params=2,
        min_boundary=[0.1, 0,],
        max_boundary=[500, 2.5],
        no_delay=False,
    )
