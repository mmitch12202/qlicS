# Generating the pylion trap object (LAMMPS code) we want
from .config_controller import configur
from .pylion import functions as pl_func


def gen_trap_lammps(uid, ions, type_pos):
    trap_params = {i[0]: eval(i[1]) for i in configur.items(f"trap_{type_pos}")}
    a = not trap_params["pseudo"]
    return pl_func.linearpaultrap(uid=uid, trap=trap_params, ions=ions, all=a)
