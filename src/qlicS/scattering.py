# TODO: Clean up the evals and datatypes in this file
# TODO: I also think a significant amount of time is spent on this calculation - try and improve performance somehow
import numpy as np

from .analysis import velocities
from .config_controller import configur
from .time_controller import get_dt_given_timestep


def scattering_rate(velocity: list, laser_config: dict, species_info: dict) -> float:
    """
    Calculates the scattering rate of an atom based on its velocity and laser parameters.

    This function computes the scattering rate using the atom's velocity, the configuration 
    of the laser, and the properties of the species involved. It takes into account the 
    direction of the laser, saturation parameters, and the natural linewidth of the species 
    to provide an accurate rate of scattering.

    Args:
        velocity (list): A list containing the velocity components of the atom [vx, vy, vz].
        laser_config (dict): A dictionary containing the configuration parameters of the laser, 
            including direction and saturation parameter.
        species_info (dict): A dictionary containing information about the species, such as 
            natural linewidth and absorption center.

    Returns:
        float: The calculated scattering rate for the atom.

    Raises:
        KeyError: If the required keys are not found in the provided dictionaries.
    """

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
    """
    Calculates the total photon count during the illumination of specified atoms.

    This function iterates over a range of timesteps and specified atoms to compute 
    the total number of photons scattered by the target species under the influence 
    of a laser. It utilizes the scattering rate and the velocities of the atoms to 
    accumulate the photon count over the defined time interval.

    Args:
        start_stop_pairs (list): A list containing two elements that define the start 
            and stop timesteps for the illumination process.
        laser_config (dict): A dictionary containing the configuration parameters for 
            the laser, including target species and indices of scattered ions.

    Returns:
        float: The total number of photons counted during the illumination.

    Raises:
        KeyError: If the required keys are not found in the provided laser configuration.
    """

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
    """
    Retrieves the scattering results based on the detection sequence.

    This function collects the detection timesteps from the configuration and 
    computes the scattering results for each defined interval. If the experimental 
    sequence includes iteration commands, it applies corrections to the detection 
    sequence before calculating the scattering results.

    Args:
        None: This function does not take any arguments.

    Returns:
        list: A list of results containing the start and stop times along with 
        the corresponding scattering counts for each detection interval.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """

    detection_seq = eval(configur.get("detection", "detection_timestep_seq"))
    if "iter" in configur.get("exp_seq", "com_list"):
        detection_seq = iter_correction(detection_seq)
    results = []
    for start_stop_f_set in detection_seq:
        if len(start_stop_f_set) >= 2:
            laser_config = dict(configur.items("scattering_laser"))
            results.append(
                start_stop_f_set + [illuminate(start_stop_f_set, laser_config)]
            )
    return results


def iter_correction(detection_seq):
    """
    Adjusts the detection sequence based on iteration parameters.

    This function modifies the provided detection sequence by incorporating 
    iteration information and adjusting the detection events according to the 
    specified time sequences and iteration counts. It ensures that the detection 
    events align correctly with the overall simulation timeline.

    Args:
        detection_seq (list): The original detection sequence to be corrected.

    Returns:
        list: The updated detection sequence with corrected timing for iterations.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """

    l_steps_per_iter = [i[1] for i in eval(configur.get("iter", "iter_timesequence"))]
    steps_per_iter = sum(l_steps_per_iter)
    iterations = eval(configur.get("iter", "scan_var_seq"))
    iter_detection_seq = eval(configur.get("iter", "iter_detection_seq"))
    pre_iter_seq = eval(configur.get("sim_parameters", "timesequence"))
    # Correcting the pre_iter_seq TODO this is copied code from time_controller
    main_com_evolve_count = configur.get("exp_seq", "com_list").count("evolve")
    time_sequence = pre_iter_seq[:main_com_evolve_count]
    pre_iter_steps = 0 if time_sequence == [] else sum(k[1] for k in time_sequence)
    for its in range(len(iterations)):
        for iter_detection_event in iter_detection_seq:
            shift = (its * steps_per_iter) + pre_iter_steps
            shifted = [iter_detection_event[0] + shift, iter_detection_event[1] + shift]
            detection_seq.append(shifted + [iterations[its]])
    return detection_seq
