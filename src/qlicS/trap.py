# Generating the pylion trap object (LAMMPS code) we want
from .config_controller import configur
from .pylion import functions as pl_func


def gen_trap_lammps(ions):

    # Getting trap code
    trap_params = {}
    for i in configur.items("trap"):
        trap_params[i[0]] = eval(i[1])
    return pl_func.linearpaultrap(trap_params, ions=ions)
