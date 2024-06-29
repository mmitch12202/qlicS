from .config_controller import configur
from .ion_creation import pylion_cloud
from .laser_cooling_force import create_cooling_laser
from .pylion import pylion as pl
from .scattering import get_scattering
from .sim_controller import pylion_dumping
from .tickle_efield import create_tickle
from .time_controller import evolve
from .trap import gen_trap_lammps


def create_and_run_sim():
    s = pl.Simulation("test")
    s.append(pylion_dumping())
    be_cloud = pylion_cloud("be+")
    s.append(be_cloud)

    s.append(gen_trap_lammps(be_cloud))

    s.append(
        create_cooling_laser(eval(configur.get("ions", "be+"))[1], be_cloud["uid"])
    )
    s.append(evolve())

    s.append(create_tickle())
    s.append(evolve())

    s.execute()

    # Analysis

    print(get_scattering())
