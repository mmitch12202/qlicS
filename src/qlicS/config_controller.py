# Generates the configuration file
import os
import time
from configparser import ConfigParser

import numpy as np

# Main Configur Object
configur = ConfigParser()


def dump_dir(setup=True):
    """
    Generates or retrieves the directory for dumping data.

    This function creates a timestamped directory for storing data dumps based on 
    the current working directory. If the `setup` parameter is set to True, it 
    creates the directory; otherwise, it retrieves the existing dump directory 
    from the configuration.

    Args:
        setup (bool, optional): A flag indicating whether to create a new dump 
            directory. Defaults to True.

    Returns:
        str: The path to the dump directory.
    """

    dump_dir = f"{os.getcwd()}/data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    if setup:
        os.makedirs(dump_dir)
        return dump_dir
    else:
        return configur.get("directory", "dump_dir")


# TODO this is hardcoded rn - fix eventually
def create_universe():
    """
    Initializes the physical constants and ion configurations for the simulation.

    This function sets up the necessary physical constants and defines the properties 
    of ions used in the Quantum Logic Ion Control Simulator. It populates the configuration 
    with constants such as Planck's constant, speed of light, and properties for Beryllium 
    and O2 ions, which are essential for the simulation's calculations.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur["constants"] = {
        "h": 6.626e-34,
        "c": 299792458,
        "amu": 1.6605402e-27,
        "ele_charge": 1.60217663e-19,
        "boltzmann": 1.380649e-23,
    }
    # Beryllium as the coolant ion,
    # O2 is cooled sympathetically in our system
    # so leaving its transition info blank
    configur["ions"] = {
        "be+": [
            {"mass": 9, "charge": 1},
            {
                "natural linewidth": 2 * np.pi * 18e6,
                "absorption center": 9.578e14,
                "saturation": 765,
            },
        ],
        "o2+": [
            {"mass": 32, "charge": 1},
            {"natural linewidth": None, "absorption center": None, "saturation": None},
        ],
    }


def create_sim_skeleton(
    log_steps,
    timesequence,
    lammps_boundary_style,
    lammps_boundary_locations,
    lammps_allow_lost,
    detection_timestep_seq,
    detector_area,
    detector_effeciency,
    detector_distance,
    GPU=False,
):
    """
    Sets up the simulation parameters and detection configuration.

    This function initializes the simulation parameters and detection settings 
    by populating the global configuration dictionary with the provided values. 
    It includes parameters such as logging steps, time sequences, and detector 
    specifications, which are essential for running the simulation.

    Args:
        log_steps (int): The number of steps between log events in the simulation.
        timesequence (list): A list defining the duration and sequence of timesteps.
        detection_timestep_seq (list): A sequence of timesteps for detection events.
        detector_area (float): The area of the detector in square meters.
        detector_effeciency (float): The efficiency of the detector (0 to 1).
        detector_distance (float): The distance of the detector from the source in meters.
        GPU (bool, optional): A flag indicating whether to use GPU for the simulation. Defaults to False.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur["sim_parameters"] = {
        "log_steps": log_steps,
        "timesequence": timesequence,
        "lammps_boundary_style": lammps_boundary_style,
        "lammps_boundary_locations": lammps_boundary_locations,
        "lammps_allow_lost": lammps_allow_lost,
        "gpu": GPU,
    }
    configur["detection"] = {
        "detection_timestep_seq": detection_timestep_seq,
        "detector_area": detector_area,
        "detector_effeciency": detector_effeciency,
        "detector_distance": detector_distance,
    }


def configur_modulation(
    type_pos,
    uid,
    amp,
    frequency,
    Ex0,
    Exx1,
    Exx2,
    Exy1,
    Exy2,
    Exz1,
    Exz2,
    Ey0,
    Eyx1,
    Eyx2,
    Eyy1,
    Eyy2,
    Eyz1,
    Eyz2,
    Ez0,
    Ezx1,
    Ezx2,
    Ezy1,
    Ezy2,
    Ezz1,
    Ezz2,
    x_shift,
    y_shift,
    z_shift,
    static,
):
    """
    Configures the modulation parameters for a specified type of modulation.

    This function updates the global configuration dictionary with modulation parameters 
    based on the provided values. It includes settings for electric field components, 
    shifts, and other modulation characteristics, allowing for detailed control over the 
    modulation process in the simulation.

    Args:
        type_pos (str): The type of modulation being configured.
        uid (str): A unique identifier for the modulation configuration.
        amp (float): The amplitude of the modulation.
        frequency (float): The frequency of the modulation.
        Ex0, Exx1, Exx2, Exy1, Exy2, Exz1, Exz2 (float): Electric field components in the x-direction.
        Ey0, Eyx1, Eyx2, Eyy1, Eyy2, Eyz1, Eyz2 (float): Electric field components in the y-direction.
        Ez0, Ezx1, Ezx2, Ezy1, Ezy2, Ezz1, Ezz2 (float): Electric field components in the z-direction.
        x_shift (float): The shift in the x-direction.
        y_shift (float): The shift in the y-direction.
        z_shift (float): The shift in the z-direction.
        static (bool): A flag indicating whether the modulation is static.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur[f"modulation_{type_pos}"] = {
        "uid": uid,
        "amp": amp,
        "frequency": frequency,
        "Ex0": Ex0,
        "Exx1": Exx1,
        "Exx2": Exx2,
        "Exy1": Exy1,
        "Exy2": Exy2,
        "Exz1": Exz1,
        "Exz2": Exz2,
        "Ey0": Ey0,
        "Eyx1": Eyx1,
        "Eyx2": Eyx2,
        "Eyy1": Eyy1,
        "Eyy2": Eyy2,
        "Eyz1": Eyz1,
        "Eyz2": Eyz2,
        "Ez0": Ez0,
        "Ezx1": Ezx1,
        "Ezx2": Ezx2,
        "Ezy1": Ezy1,
        "Ezy2": Ezy2,
        "Ezz1": Ezz1,
        "Ezz2": Ezz2,
        "x_shift": x_shift,
        "y_shift": y_shift,
        "z_shift": z_shift,
        "static": static,
    }

def configur_static_efield(
    type_pos,
    uid,
    amp,
    x_bound,
    y_bound,
    z_bound,
    Ex0,
    Exx1,
    Exx2,
    Exy1,
    Exy2,
    Exz1,
    Exz2,
    Ey0,
    Eyx1,
    Eyx2,
    Eyy1,
    Eyy2,
    Eyz1,
    Eyz2,
    Ez0,
    Ezx1,
    Ezx2,
    Ezy1,
    Ezy2,
    Ezz1,
    Ezz2,
    x_shift,
    y_shift,
    z_shift,
):
    """
    Configures the parameters for a static electric field in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining a static electric field, including its unique identifier, amplitude, 
    bounds, and electric field components. This allows for detailed specification 
    of static electric fields used in the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the static electric field being configured.
        uid (str): A unique identifier for the static electric field configuration.
        amp (float): The amplitude of the electric field.
        x_bound (list): The bounds for the electric field in the x-direction.
        y_bound (list): The bounds for the electric field in the y-direction.
        z_bound (list): The bounds for the electric field in the z-direction.
        Ex0, Exx1, Exx2, Exy1, Exy2, Exz1, Exz2 (float): Electric field components in the x-direction.
        Ey0, Eyx1, Eyx2, Eyy1, Eyy2, Eyz1, Eyz2 (float): Electric field components in the y-direction.
        Ez0, Ezx1, Ezx2, Ezy1, Ezy2, Ezz1, Ezz2 (float): Electric field components in the z-direction.
        x_shift (float): The shift in the x-direction.
        y_shift (float): The shift in the y-direction.
        z_shift (float): The shift in the z-direction.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """
    configur[f"static_efield_{type_pos}"] = {
        "uid": uid,
        "amp": amp,
        "x_bound": x_bound,
        "y_bound": y_bound,
        "z_bound": z_bound,
        "Ex0": Ex0,
        "Exx1": Exx1,
        "Exx2": Exx2,
        "Exy1": Exy1,
        "Exy2": Exy2,
        "Exz1": Exz1,
        "Exz2": Exz2,
        "Ey0": Ey0,
        "Eyx1": Eyx1,
        "Eyx2": Eyx2,
        "Eyy1": Eyy1,
        "Eyy2": Eyy2,
        "Eyz1": Eyz1,
        "Eyz2": Eyz2,
        "Ez0": Ez0,
        "Ezx1": Ezx1,
        "Ezx2": Ezx2,
        "Ezy1": Ezy1,
        "Ezy2": Ezy2,
        "Ezz1": Ezz1,
        "Ezz2": Ezz2,
        "x_shift": x_shift,
        "y_shift": y_shift,
        "z_shift": z_shift,
    }

def configur_constants(h, c, amu, ele_charge, kb):
    """
    Sets the physical constants in the configuration.

    This function updates the global configuration dictionary with fundamental 
    physical constants such as Planck's constant, the speed of light, atomic mass 
    unit, elementary charge, and Boltzmann's constant. This allows for easy access 
    to these constants throughout the Quantum Logic Ion Control Simulator.

    Args:
        h (float): Planck's constant.
        c (float): The speed of light in vacuum.
        amu (float): Atomic mass unit.
        ele_charge (float): Elementary charge.
        kb (float): Boltzmann's constant.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """
    configur["constants"] = {
        "h": h,
        "c": c,
        "amu": amu,
        "ele_charge": ele_charge,
        "boltzmann": kb,
    }

def configur_ions(ions):
    """
    Sets the ion configurations in the global configuration.

    This function updates the global configuration dictionary with the provided 
    ion definitions, allowing the simulation to utilize the specified ions. 
    This facilitates the management of ion properties within the Quantum Logic 
    Ion Control Simulator.

    Args:
        ions (dict): A dictionary containing the definitions and properties of the ions.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """
    configur["ions"] = ions

def configur_ion_cloud(type_pos, uid, species, radius, count):
    """
    Configures the properties of an ion cloud in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining an ion cloud, including its unique identifier, species, radius, and 
    the number of ions. This allows for detailed specification of ion clouds used 
    in the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the ion cloud being configured.
        uid (str): A unique identifier for the ion cloud configuration.
        species (str): The species of the ions in the cloud.
        radius (float): The radius of the ion cloud.
        count (int): The number of ions in the cloud.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur[f"ion_cloud_{type_pos}"] = {
        "uid": uid,
        "species": species,
        "radius": radius,
        "count": count,
    }

def configur_late_cloud(type_pos, uid, species, radius, count):
    configur[f"late_cloud_{type_pos}"] = {
        "uid": uid,
        "species": species,
        "radius": radius,
        "count": count,
    }

def configur_trap(
    type_pos,
    uid,
    target_ion_pos,
    radius,
    length,
    kappa,
    frequency,
    voltage,
    endcapvoltage,
    pseudo,
):
    """
    Configures the properties of a trap in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining a trap, including its unique identifier, target ion position, dimensions, 
    and operational characteristics. This allows for detailed specification of traps 
    used in the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the trap being configured.
        uid (str): A unique identifier for the trap configuration.
        target_ion_pos (tuple): The position of the target ion in the trap.
        radius (float): The radius of the trap.
        length (float): The length of the trap.
        kappa (float): The parameter related to the trap's field configuration.
        frequency (float): The operating frequency of the trap.
        voltage (float): The voltage applied to the trap.
        endcapvoltage (float): The voltage applied to the endcaps of the trap.
        pseudo (bool): A flag indicating whether the trap is a pseudo trap.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur[f"trap_{type_pos}"] = {
        "uid": uid,
        "target_ion_pos": target_ion_pos,
        "radius": radius,
        "length": length,
        "kappa": kappa,
        "frequency": frequency,
        "voltage": voltage,
        "endcapvoltage": endcapvoltage,
        "pseudo": pseudo,
    }


def configur_cooling_laser(
    uid,
    type_pos,
    target_ion_pos,
    target_ion_type,
    beam_radius,
    saturation_paramater,
    detunning,
    laser_direction,
    laser_origin_position,
):
    """
    Configures the properties of a cooling laser in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining a cooling laser, including its unique identifier, target ion position, 
    and various operational characteristics. This allows for detailed specification 
    of cooling lasers used in the Quantum Logic Ion Control Simulator.

    Args:
        uid (str): A unique identifier for the cooling laser configuration.
        type_pos (str): The type or position of the cooling laser being configured.
        target_ion_pos (tuple): The position of the target ion for the cooling laser.
        target_ion_type (str): The type of the target ion being cooled.
        beam_radius (float): The radius of the cooling laser beam.
        saturation_paramater (float): The saturation parameter for the laser.
        detunning (float): The detuning of the laser frequency from the target ion transition.
        laser_direction (tuple): The direction vector of the laser beam.
        laser_origin_position (tuple): The origin position of the laser in the simulation.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur[f"cooling_laser_{type_pos}"] = {
        "uid": uid,
        "target_ion_pos": target_ion_pos,
        "target_ion_type": target_ion_type,
        "beam_radius": beam_radius,
        "saturation_paramater": saturation_paramater,
        "detunning": detunning,
        "laser_direction": laser_direction,
        "laser_origin_position": laser_origin_position,
    }


def configur_scattering_laser(
    scattered_ion_indices,
    target_species,
    laser_direction,
    saturation_paramater,
    frequency,
):
    """
    Configures the properties of a scattering laser in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining a scattering laser, including the indices of scattered ions, the target 
    species, and various operational characteristics. This allows for detailed 
    specification of scattering lasers used in the Quantum Logic Ion Control Simulator.

    Args:
        scattered_ion_indices (list): A list of indices for the ions that will be scattered.
        target_species (str): The species of the target ions for the scattering process.
        laser_direction (tuple): The direction vector of the scattering laser.
        saturation_paramater (float): The saturation parameter for the laser.
        frequency (float): The frequency of the scattering laser.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur["scattering_laser"] = {
        "scattered_ion_indices": scattered_ion_indices,
        "target_species": target_species,
        "laser_direction": laser_direction,
        "saturation_paramater": saturation_paramater,
        "frequency": frequency,
    }


def configur_cloud_reset(
    type_pos,
    initial_atom_id,
    style,
    radius,
    count,
):
    """
    Configures the reset parameters for an ion cloud in the simulation.

    This function updates the global configuration dictionary with the parameters 
    defining how an ion cloud should be reset, including the initial atom ID, 
    style of the reset, radius, and the number of atoms in the cloud. This allows 
    for detailed specification of cloud reset behavior in the Quantum Logic Ion 
    Control Simulator.

    Args:
        type_pos (str): The type or position of the ion cloud being reset.
        initial_atom_id (int): The ID of the atom from which the reset will start.
        style (str): The style of the reset operation.
        radius (float): The radius of the ion cloud.
        count (int): The number of ions in the cloud after the reset.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur[f"cloud_reset_{type_pos}"] = {
        "initial_atom_id": initial_atom_id,
        "style": style,
        "radius": radius,
        "count": count,
    }

def configur_mass_change(type_pos, uid, new_mass):
    configur[f"mass_change_{type_pos}"] = {
        "target_cloud_id": uid,
        "new_mass": new_mass,
    }

def configur_iter(
    scan_objects,
    scan_var,
    scan_var_seq,
    iter_timesequence,
    iter_detection_seq,
    com_list,
):
    """
    Configures the iteration parameters for the simulation.

    This function updates the global configuration dictionary with the parameters 
    related to the iteration process, including scan objects, scan variables, 
    time sequences, and command lists. This allows for detailed specification of 
    iteration behavior in the Quantum Logic Ion Control Simulator.

    Args:
        scan_objects (list): A list of objects to be scanned during the iteration.
        scan_var (str): The variable that will be scanned.
        scan_var_seq (list): The sequence of values for the scan variable.
        iter_timesequence (list): The time sequence for the iteration.
        iter_detection_seq (list): The sequence of detection events during the iteration.
        com_list (list): A list of commands to be executed during the iteration.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur["iter"] = {
        "scan_objects": scan_objects,
        "scan_var": scan_var,
        "scan_var_seq": scan_var_seq,
        "iter_timesequence": iter_timesequence,
        "iter_detection_seq": iter_detection_seq,
        "com_list": com_list,
    }


def create_exp_seq(exp_seq: str):
    """
    Creates and stores the experimental sequence in the configuration.

    This function updates the global configuration dictionary with the experimental 
    sequence provided as a string. This allows for the storage and retrieval of 
    the command list used in the Quantum Logic Ion Control Simulator.

    Args:
        exp_seq (str): A string representing the experimental sequence of commands.

    Returns:
        None: This function does not return a value; it modifies the global configuration 
        dictionary directly.
    """

    configur["exp_seq"] = {"com_list": exp_seq}


def create_config(dump_dir):
    """
    Initializes the configuration settings for the simulation.

    This function sets up the initial configuration parameters, including the 
    directory for data dumps and the current position in the time sequence. 
    It also calls the `create_universe` function to establish the necessary 
    physical constants and ion configurations for the simulation.

    Args:
        dump_dir (str): The directory path where data dumps will be stored.

    Returns:
        None: This function does not return a value; it modifies the global 
        configuration dictionary directly.
    """

    # sourcery skip: ensure-file-closed, use-fstring-for-concatenation
    # Write configuration
    # Normally Un-changing Content
    configur["directory"] = {"dump_dir": dump_dir}
    configur["live_vars"] = {"current_timesequence_pos": 0}
    #create_universe() No longer using this hardcode crutch


def commit_changes():
    """
    Writes the current configuration to a file.

    This function saves the global configuration dictionary to a specified 
    INI file, ensuring that all changes made to the configuration are 
    persisted. It opens the file in write mode and uses the `configur` 
    object to write the current settings.

    Args:
        None: This function does not take any arguments.

    Returns:
        None: This function does not return a value; it performs a file 
        write operation to save the configuration.
    """

    with open(f"{direc}gennedconfig.ini", "w") as configfile:
        configur.write(configfile)


def setup_sequence():
    """
    Initializes the directory and configuration for the simulation.

    This function sets up the necessary directory for data dumps and initializes 
    the configuration settings by calling the `create_config` function. It also 
    prepares the environment for the simulation by defining the global directory 
    variable.

    Args:
        None: This function does not take any arguments.

    Returns:
        None: This function does not return a value; it modifies the global 
        variable and configuration directly.
    """

    global direc
    direc = dump_dir()
    create_config(direc)
    # TODO this commit changes is not behaving how I expected
    # commit_changes()


# getting


def get_ions():
    """
    Retrieves a list of ion types from the configuration.

    This function extracts the keys representing different ion types from the 
    configuration dictionary and returns them as a list. It allows for easy 
    access to the defined ions in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        list: A list of strings representing the ion types defined in the configuration.
    """

    return list(dict(configur.items("ions")).keys())


def get_sections():
    """
    Retrieves a list of sections from the configuration.

    This function accesses the configuration dictionary and returns a list of 
    all defined sections. It provides a convenient way to obtain the structure 
    of the configuration used in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        list: A list of strings representing the names of the sections in the configuration.
    """

    return configur.sections()
