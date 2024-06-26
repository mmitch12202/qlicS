# Generates the configuration file
import os
import time
from configparser import ConfigParser

import numpy as np

# Configur Object
configur = ConfigParser()


def dump_dir(setup=True):
    dump_dir = str(os.getcwd()) + "/data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    if setup:
        os.makedirs(dump_dir)
    return dump_dir


def create_config(dump_dir):
    # Write configuration
    # Normally Un-changing Content
    configur["directory"] = {"dump_dir": dump_dir}
    configur["constants"] = {
        "h": 6.626e-34,
        "c": 299792458,
        "amu": 1.6605402e-27,
        "ele_charge": 1.60217663e-19,
    }
    configur["live_vars"] = {"current_timesequence_pos": 0}
    configur["sim_parameters"] = {
        "log_steps": 10,
        # [[dt1, Δt1], [dt2, Δt2] etc...], Δt (timesteps) is just the number of dt's
        "timesequence": [[1e-8, 1e4], [1e-9, 1e4]],
    }
    configur["modulation"] = {
        "uid": 569202603907006,
        "amp": 3e-3,
        "frequency": 717000,  # hz
        "Ex0": 0.319039e3,
        "Exx1": -0.320779e6,
        "Exx2": 0.16384e9,
        "Exy1": 0.00318837e6,
        "Exy2": -0.158115e9,
        "Exz1": -4.83258e-1,
        "Exz2": 0.0000162061e9,
        "Ey0": -0.00362944e3,
        "Eyx1": 0.00352719e6,
        "Eyx2": 0.000660075e9,
        "Eyy1": 0.320888e6,
        "Eyy2": -0.001252e9,
        "Eyz1": 1.91814,
        "Eyz2": 0.0000135735e9,
        "Ez0": 1.11849e-3,
        "Ezx1": -5.82074e-1,
        "Ezx2": -7.895e2,
        "Ezy1": 2.08274,
        "Ezy2": 1.40833e3,
        "Ezz1": -0.0000575482e6,
        "Ezz2": 1.53512e2,
        "x_shift": 0,
        "y_shift": 0,
        "z_shift": 0,
        "static": [0, 0, 0],
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
    configur["ion_cloud"] = {"radius": 1e-3, "count": 50}
    configur["trap"] = {
        "radius": 3.75e-3,
        "length": 2.75e-3,
        "kappa": 0.244,
        "frequency": 3.85e6,
        "voltage": 500,
        "endcapvoltage": 15,
        "pseudo": True,
    }
    # Note: - I am trying to use more useful variables here
    # that can be scaled against the species,
    # hence 'saturation_paramater' and 'detunning'
    # as opposed to 'saturation' and 'frequency'.
    # Detunning is assumed to be red.
    configur["cooling_laser"] = {
        "beam_radius": 0.1e-3,
        "saturation_paramater": 100,
        "detunning": 3e8,
        "laser_direction": [
            -1 / 2,
            -1 / 2,
            -1 / np.sqrt(2),
        ],  # TODO as of now this needs to be normalized manually - fix
        "laser_origin_position": [0, 0, 0],
    }
    configur["scattering_laser"] = {
        "scattered_ion_indices": [
            0,
            50,
        ],  # TODO I think we should eventually move this into the "ions" section
        "target_species": "be+",
        "laser_direction": [
            -1 / 2,
            -1 / 2,
            -1 / np.sqrt(2),
        ],  # TODO as of now this needs to be normalized manually - fix
        "saturation_paramater": 100,
        "frequency": 9.578e14,
    }
    configur["detection"] = {
        "detection_timestep_seq": [[15000, 16000], [17000, 19000]],
        "detector_area": 0.0001,
        "detector_effeciency": 0.01,
        "detector_distance": 0.2,
    }
    configfile = open(dump_dir + "config.ini", "w")
    configur.write(configfile)
    configfile.close()


def setup_sequence():
    # Using a global variable - there is a more pythonic way of doing this...
    # I think the above is resolved, try removing
    global dir
    dir = dump_dir()
    create_config(dir)
