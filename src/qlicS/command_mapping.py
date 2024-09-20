from .ion_creation import cloud_reset, pylion_cloud
from .laser_cooling_force import create_cooling_laser
from .sim_controller import pylion_dumping
from .tickle_efield import create_tickle
from .time_controller import evolve
from .trap import gen_trap_lammps
from .arbitrary_static_efield import create_static_field


def give_command_mapping():
    return {
        "dumping": pylion_dumping,
        "cloud": pylion_cloud,
        "trap": gen_trap_lammps,
        "cooling_laser": create_cooling_laser,
        "evolve": evolve,
        "tickle": create_tickle,
        "iter": None,
        "cloud_reset": cloud_reset,
        "static_efield": create_static_field
    }
