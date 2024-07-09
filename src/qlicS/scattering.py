# TODO: Clean up the evals and datatypes in this file
import numpy as np

from .analysis import velocities
from .config_controller import configur
from .time_controller import get_dt_given_timestep


def scattering_rate(velocity: list, laser_config: dict, species_info: dict) -> float:
    c = eval(configur.get("constants", "c"))

    this_atom_velocities_dot = (
        velocity[0] * abs(eval(laser_config["laser_direction"])[0])
        + velocity[1] * abs(eval(laser_config["laser_direction"])[1])
        + velocity[2] * abs(eval(laser_config["laser_direction"])[2])
    )  # TODO Figure out what we are doing with these abs()
    return (
        0.5
        * eval(laser_config["saturation_paramater"])
        * species_info["natural linewidth"]
    ) / (
        1
        + eval(laser_config["saturation_paramater"])
        + (
            (
                (
                    species_info["absorption center"]
                    - eval(laser_config["frequency"])
                    * np.sqrt(
                        (1 + (this_atom_velocities_dot / c))
                        / (1 - (this_atom_velocities_dot / c))
                    )
                )
                / (0.5 * species_info["natural linewidth"])
            )
            ** 2
        )
    )


# sum scattering over the time period, return # of photons
def illuminate(start_stop_pairs: list, laser_config: dict) -> float:
    target_species = laser_config["target_species"]
    atom_range = eval(laser_config["scattered_ion_indices"])
    vels = velocities()
    photon_count = 0
    for timestep in range(
        int(start_stop_pairs[0]),
        int(start_stop_pairs[1]),
        eval(configur.get("sim_parameters", "log_steps")),
    ):
        for atom in range(int(atom_range[0]), int(atom_range[1])):
            photon_count += scattering_rate(
                vels[timestep][atom],
                laser_config,
                eval(configur.get("ions", target_species))[1],
            ) * get_dt_given_timestep(
                timestep
            )  # create a data read in module
    return photon_count


# run illuminate in the sequence needed, return a list of lists
# [[timestepstart, timestepstop, # of photons:]]
def get_scattering() -> list:
    detection_seq = eval(configur.get("detection", "detection_timestep_seq"))
    if "iter" in configur.get("exp_seq", "com_list"):
        detection_seq = iter_correction(detection_seq)
    results = []
    for start_stop_pair in detection_seq:
        laser_config = dict(configur.items("scattering_laser"))
        results.append(start_stop_pair + [illuminate(start_stop_pair, laser_config)])
    return results

def iter_correction(detection_seq):
    l_steps_per_iter = [
            i[1] for i in eval(configur.get("iter", "iter_timesequence"))
        ]
    steps_per_iter = sum(l_steps_per_iter)
    iterations = len(eval(configur.get("iter", "scan_var_seq")))
    iter_detection_seq = eval(configur.get("iter", "iter_detection_seq"))
    pre_iter_steps = sum(
        k[1] for k in eval(configur.get("sim_parameters", "timesequence"))
    ) # assuming evolves have been called and iter is last
    for its in range(iterations):
        for iter_detection_event in iter_detection_seq:
            shift = (its*steps_per_iter)+pre_iter_steps
            detection_seq.append([iter_detection_event[0]+shift, iter_detection_event[1]+shift])
    return detection_seq
