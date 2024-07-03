from .ion_creation import pylion_cloud
from .laser_cooling_force import create_cooling_laser
from .sim_controller import pylion_dumping
from .tickle_efield import create_tickle
from .time_controller import evolve
from .trap import gen_trap_lammps

command_mapping = {
    "dumping": pylion_dumping,
    "cloud": pylion_cloud,
    "trap": gen_trap_lammps,
    "cooling_laser": create_cooling_laser,
    "evolve": evolve,
    "tickle": create_tickle,
}
