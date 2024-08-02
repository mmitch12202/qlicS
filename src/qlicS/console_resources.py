from configparser import ConfigParser
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

from . import config_controller, exp_sequence_controller
from .command_mapping import give_command_mapping
from .config_controller import get_ions
from .resources import PathStringValidator

import os

loading_configur = ConfigParser()


def followup_questions_creator():
    return {
        "dumping": None,  # TODO, realistically, dumping doesnt belong with these other functions
        "cloud": [
            inquirer.select(
                message="Species",
                choices=get_ions(),
            ),
            inquirer.number(
                message="Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Count",
                min_allowed=0,
                float_allowed=False,
                validate=EmptyInputValidator(),
            ),
        ],
        "trap": [
            inquirer.number(
                message="Target Ion Position (0 for first ion, 1 for second)",
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Length",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Kappa",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Frequency",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Voltage",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Endcapvoltage",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.select(
                message="Pseudo",
                choices=["True", "False"],
            ),
        ],
        "cooling_laser": [
            inquirer.number(
                message="Target Ion Position (0 for first ion, 1 for second)",
                validate=EmptyInputValidator(),
            ),
            inquirer.select(
                message="Species",
                choices=get_ions(),
            ),
            inquirer.number(
                message="Beam Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Saturation Paramater",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Detunning", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.text(
                message="Laser Direction Vector-List, all negative (ex [-0.5, -0.5, -0.71])",
                validate=EmptyInputValidator(),
            ),
            inquirer.text(
                message="Laser Origin Position Vector-List (ex [0, 0, 0])",
                validate=EmptyInputValidator(),
            ),
        ],
        "evolve": None,
        "tickle": [
            inquirer.number(
                message="uid", float_allowed=False, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="amp", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="frequency", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ex0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ey0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ez0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="x_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="y_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="z_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.text(
                message="Static E-field Vector-List (ex [0, 0, 0])",
                validate=EmptyInputValidator(),
            ),
        ],
    }


def run_from_file(optimize_mode=False, **kwargs):
    # TODO "optimize_mode" is being used in non-optimize cases.  Clean up this notation
    if not optimize_mode:
        config_file = config_file_dialogue()
    elif exp := kwargs.get("exp", None):
        config_file = exp
    else:
        raise ValueError("No experiment given to optimize")

    loading_configur = setup_loading_configur(config_file)
    config_controller.setup_sequence()

    type_poses = count_type_pos(loading_configur)
    print(type_poses)

    # Helper function to update arguments with overrides from kwargs
    def get_overridden_args(defaults, prefix):
        overridden_args = {}
        for k, v in kwargs.items():
            if k.startswith(prefix):
                key_without_prefix = k[len(prefix) + 1:]
                overridden_args[key_without_prefix] = v
        return {**defaults, **overridden_args}


    # Sim skeleton inputs
    s_p, d_p = get_sim_skeleton_inputs()
    s_p = get_overridden_args(s_p, 's_p')
    d_p = get_overridden_args(d_p, 'd_p')
    config_controller.create_sim_skeleton(
        s_p["log_steps"],
        s_p["timesequence"],
        d_p["detection_timestep_seq"],
        d_p["detector_area"],
        d_p["detector_effeciency"],
        d_p["detector_distance"],
        s_p["gpu"],
    )

    # Cloud reset configuration
    for i in range(type_poses["cloud_reset"]):
        cl_reset = get_cloud_reset(i)
        cl_reset = get_overridden_args(cl_reset, f'cloud_reset_{i}')
        config_controller.configur_cloud_reset(
            i,
            cl_reset["initial_atom_id"],
            cl_reset["style"],
            cl_reset["radius"],
            cl_reset["count"],
        )

    # Modulation configuration
    for i in range(type_poses["tickle"]):
        m = get_modulation_inputs(i)
        m = get_overridden_args(m, f'modulation_{i}')
        config_controller.configur_modulation(
            i,
            m["uid"],
            m["amp"],
            m["frequency"],
            m["ex0"],
            m["exx1"],
            m["exx2"],
            m["exy1"],
            m["exy2"],
            m["exz1"],
            m["exz2"],
            m["ey0"],
            m["eyx1"],
            m["eyx2"],
            m["eyy1"],
            m["eyy2"],
            m["eyz1"],
            m["eyz2"],
            m["ez0"],
            m["ezx1"],
            m["ezx2"],
            m["ezy1"],
            m["ezy2"],
            m["ezz1"],
            m["ezz2"],
            m["x_shift"],
            m["y_shift"],
            m["z_shift"],
            m["static"],
        )

    # Ion cloud configuration
    for i in range(type_poses["cloud"]):
        c = get_cloud_inputs(i)
        c = get_overridden_args(c, f'cloud_{i}')
        config_controller.configur_ion_cloud(
            i, c["uid"], c["species"], c["radius"], c["count"]
        )

    # Trap configuration
    for i in range(type_poses["trap"]):
        t = get_trap_inputs(i)
        t = get_overridden_args(t, f'trap_{i}')
        config_controller.configur_trap(
            i,
            t["uid"],
            t["target_ion_pos"],
            t["radius"],
            t["length"],
            t["kappa"],
            t["frequency"],
            t["voltage"],
            t["endcapvoltage"],
            t["pseudo"],
        )

    # Cooling laser configuration
    for i in range(type_poses["cooling_laser"]):
        cl = get_cooling_laser_inputs(i)
        cl = get_overridden_args(cl, f'cooling_laser_{i}')
        config_controller.configur_cooling_laser(
            cl["uid"],
            i,
            cl["target_ion_pos"],
            cl["target_ion_type"],
            cl["beam_radius"],
            cl["saturation_paramater"],
            cl["detunning"],
            cl["laser_direction"],
            cl["laser_origin_position"],
        )

    # Scattering laser configuration
    if loading_configur.has_section("scattering_laser"):
        sl = get_scattering_laser_inputs()
        sl = get_overridden_args(sl, 'scattering_laser')
        config_controller.configur_scattering_laser(
            sl["scattered_ion_indices"],
            sl["target_species"],
            sl["laser_direction"],
            sl["saturation_paramater"],
            sl["frequency"],
        )

    # Experiment sequence configuration
    exp_seq = get_exp_seq()
    if "iter" in exp_seq:
        it = get_iter_inputs()
        it = get_overridden_args(it, 'iter')
        config_controller.configur_iter(
            it["scan_objects"],
            it["scan_var"],
            it["scan_var_seq"],
            it["iter_timesequence"],
            it["iter_detection_seq"],
            it["com_list"],
        )

    config_controller.create_exp_seq(exp_seq)
    # config_controller.commit_changes()
    return exp_sequence_controller.create_and_run_sim_gen()

def run_from_batch(**kwargs):
    # TODO arguments are for the future implementation of an "optimize from batch" mode.  This optimize mode is different from the optimize_mode arg of run_from_file()
    # TODO maybe at some point should make the data naming more helpful
    b_parent = batch_config_dialogue()
    # Get a list of paths to each .ini file in b_parent
    ini_files = [os.path.join(b_parent, file) for file in os.listdir(b_parent) if file.endswith(".ini")]
    for ini_file in ini_files:
        run_from_file(optimize_mode=True, exp=ini_file)


def config_file_dialogue():
    return inquirer.filepath(
        message="Enter a configuration (*.ini) file:",
        validate=PathStringValidator(
            is_file=True,
            message="Input is not a valid filpath.  Make sure input is not a string.",
        ),  # TODO validate that it is also a .ini file
    ).execute()

def batch_config_dialogue():
    return inquirer.filepath(
        message="Enter the parent directory of .ini files to submit as a batch.  Be sure to prime the data folder.",
        validate=PathStringValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
    ).execute()

def mode_dialogue():
    return inquirer.select(
        message="Select a mode",
        choices=[
            "Create New Experiment",
            "Run Experiment From File",
            "Run Experiment Batch From Directory",
            "Optimize Experiment with M-LOOP",
            "Edit Existing Experiment",
            "Analyze Completed Experiment",
            Choice(value=None, name="Quit"),
        ],
        default="Create New Experiment",
    ).execute()


def setup_loading_configur(loading_config_file):
    if not loading_config_file or loading_config_file.strip() == "":
        raise FileNotFoundError("Loading configuration file not provided")
    if not loading_config_file.endswith(".ini"):
        raise ValueError("Invalid file format. Only .ini files are supported.")
    loading_configur.read(loading_config_file)
    return loading_configur


def count_type_pos(loading_configur):
    command_mapping = give_command_mapping()
    type_poses = {key: 0 for key in command_mapping}
    command_string = loading_configur.get("exp_seq", "com_list").split(",")
    # Check if iter is used
    if "iter" in command_string:
        iter_command_string = loading_configur.get("iter", "com_list").split(",")
        for i in iter_command_string:
            if i not in command_string:
                command_string.append(i)
            elif i[:2] != "r_":
                type_poses[i] += 1
    for command in command_string:
        if (
            command[:2] != "r_"
        ):  # this is fine since the removers are a fundamentally different type of command
            type_poses[command] += 1
    return type_poses


def get_sim_skeleton_inputs():
    sim_params = loading_configur.items("sim_parameters")
    if loading_configur.has_section("detection"):
        detection_params = loading_configur.items("detection")
    else:
        detection_params = [
            ["detection_timestep_seq", [[]]],
            ["detector_area", "null"],
            ["detector_effeciency", "null"],
            ["detector_distance", "null"],
        ]
    if "gpu" not in dict(sim_params):
        sim_params.append(["gpu", False])
    return dict(sim_params), dict(detection_params)


def get_cloud_reset(type_pos):
    return dict(loading_configur.items(f"cloud_reset_{type_pos}"))


def get_modulation_inputs(type_pos):
    return dict(loading_configur.items(f"modulation_{type_pos}"))


def get_cloud_inputs(type_pos):
    return dict(loading_configur.items(f"ion_cloud_{type_pos}"))


def get_trap_inputs(type_pos):
    return dict(loading_configur.items(f"trap_{type_pos}"))


def get_cooling_laser_inputs(type_pos):
    return dict(loading_configur.items(f"cooling_laser_{type_pos}"))


def get_scattering_laser_inputs():
    return dict(loading_configur.items("scattering_laser"))


def get_iter_inputs():
    return dict(loading_configur.items("iter"))


def get_exp_seq():
    return loading_configur.get("exp_seq", "com_list")
