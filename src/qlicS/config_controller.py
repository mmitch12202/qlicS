# Generates the configuration file
import os
import time
from configparser import ConfigParser

import numpy as np

# Main Configur Object
configur = ConfigParser()


def dump_dir(setup=True):
    dump_dir = f"{os.getcwd()}/data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    if setup:
        os.makedirs(dump_dir)
        return dump_dir
    else:
        return configur.get("directory", "dump_dir")


def create_universe():
    configur["constants"] = {
        "h": 6.626e-34,
        "c": 299792458,
        "amu": 1.6605402e-27,
        "ele_charge": 1.60217663e-19,
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
    detection_timestep_seq,
    detector_area,
    detector_effeciency,
    detector_distance,
):
    configur["sim_parameters"] = {
        "log_steps": log_steps,
        "timesequence": timesequence,
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


def configur_ion_cloud(type_pos, uid, species, radius, count):
    configur[f"ion_cloud_{type_pos}"] = {
        "uid": uid,
        "species": species,
        "radius": radius,
        "count": count,
    }


def configur_trap(
    type_pos,
    target_ion_pos,
    radius,
    length,
    kappa,
    frequency,
    voltage,
    endcapvoltage,
    pseudo,
):
    configur[f"trap_{type_pos}"] = {
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
    configur["scattering_laser"] = {
        "scattered_ion_indices": scattered_ion_indices,
        "target_species": target_species,
        "laser_direction": laser_direction,
        "saturation_paramater": saturation_paramater,
        "frequency": frequency,
    }


def configur_iter(
    scan_objects,
    scan_var,
    scan_var_seq,
    iter_timesequence,
    iter_detection_seq,
    com_list,
):
    configur["iter"] = {
        "scan_objects": scan_objects,
        "scan_var": scan_var,
        "scan_var_seq": scan_var_seq,
        "iter_timesequence": iter_timesequence,
        "iter_detection_seq": iter_detection_seq,
        "com_list": com_list,
    }


def create_exp_seq(exp_seq: str):
    configur["exp_seq"] = {"com_list": exp_seq}


def create_config(dump_dir):
    # sourcery skip: ensure-file-closed, use-fstring-for-concatenation
    # Write configuration
    # Normally Un-changing Content
    configur["directory"] = {"dump_dir": dump_dir}
    configur["live_vars"] = {"current_timesequence_pos": 0}
    create_universe()


def commit_changes():
    with open(f"{direc}gennedconfig.ini", "w") as configfile:
        configur.write(configfile)


def setup_sequence():
    global direc
    direc = dump_dir()
    create_config(direc)
    # TODO this commit changes is not behaving how I expected
    # commit_changes()


# getting


def get_ions():
    return list(dict(configur.items("ions")).keys())


def get_sections():
    return configur.sections()
