# Generating the pylion trap object (LAMMPS code) we want
from .config_controller import configur
from .pylion import functions as pl_func


def gen_trap_lammps(ions):
    trap_params = {i[0]: eval(i[1]) for i in configur.items("trap")}
    return pl_func.linearpaultrap(trap_params, ions=ions)
