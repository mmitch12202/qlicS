import os
from configparser import ConfigParser
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

from . import config_controller, exp_sequence_controller
from .command_mapping import give_command_mapping
from .config_controller import get_ions
from .resources import PathStringValidator

loading_configur = ConfigParser()


def followup_questions_creator():
    """
    Creates a mapping of follow-up questions for different simulation components.

    This function generates a dictionary that contains lists of follow-up questions 
    tailored for various components of the Quantum Logic Ion Control Simulator, such 
    as ion clouds, traps, cooling lasers, and modulation settings. Each component has 
    specific questions that guide the user in providing necessary parameters for the 
    simulation setup.

    Returns:
        dict: A dictionary mapping component types (str) to their corresponding 
        lists of follow-up questions (list).
    """

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
    """
    Runs a simulation based on the configuration provided in a file.

    This function initializes the simulation by loading configuration settings 
    from a specified file or user input, setting up the necessary parameters 
    for various components such as ion clouds, traps, and lasers. It also 
    allows for optional optimization of the experiment based on provided 
    arguments.

    Args:
        optimize_mode (bool, optional): A flag indicating whether to run in 
            optimization mode. Defaults to False.
        **kwargs: Additional keyword arguments that can override default 
            parameters for the simulation.

    Returns:
        None: This function does not return a value; it executes the simulation 
        based on the configured parameters.
    
    Raises:
        ValueError: If no experiment is provided for optimization when 
        `optimize_mode` is True.
    """

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

    constants = get_constants()
    config_controller.configur_constants(constants['h'], constants['c'], constants['amu'], constants['ele_charge'], constants['boltzmann'])

    ions = get_ions_inputs()
    config_controller.configur_ions(ions)

    for i in range(type_poses["mass_change"]):
        mass_change = get_mass_change_inputs(i)
        config_controller.configur_mass_change(i, mass_change["target_cloud_id"], mass_change["new_mass"])

    # Helper function to update arguments with overrides from kwargs
    def get_overridden_args(defaults, prefix):
        """
        Combines default arguments with overridden values based on a prefix.

        This function takes a dictionary of default arguments and a prefix, 
        then checks for any keys in the provided keyword arguments that start 
        with the specified prefix. It returns a new dictionary that merges the 
        default arguments with any overridden values, allowing for flexible 
        configuration of parameters.

        Args:
            defaults (dict): A dictionary of default argument values.
            prefix (str): The prefix used to identify which arguments should be 
                overridden.

        Returns:
            dict: A dictionary containing the combined default and overridden 
            argument values.

        Raises:
            None: This function does not raise exceptions.
        """
        overridden_args = {}
        for k, v in kwargs.items():
            if k.startswith(prefix):
                key_without_prefix = k[len(prefix) + 1 :]
                overridden_args[key_without_prefix] = v
        return {**defaults, **overridden_args}

    # Sim skeleton inputs
    s_p, d_p = get_sim_skeleton_inputs()
    s_p = get_overridden_args(s_p, "s_p")
    d_p = get_overridden_args(d_p, "d_p")
    if not s_p["lammps_boundary_style"]:
        s_p["lammps_boundary_style"] = ['m', 'm', 'm']
    if not s_p["lammps_boundary_locations"]:
        s_p["lammps_boundary_locations"] = [[-0.001, 0.001],[-0.001, 0.001],[-0.001, 0.001]]
    if not s_p["lammps_allow_lost"]:
        s_p["lammps_allow_lost"] = False
    config_controller.create_sim_skeleton(
        s_p["log_steps"],
        s_p["timesequence"],
        s_p["lammps_boundary_style"],
        s_p["lammps_boundary_locations"],
        s_p["lammps_allow_lost"],
        d_p["detection_timestep_seq"],
        d_p["detector_area"],
        d_p["detector_effeciency"],
        d_p["detector_distance"],
        s_p["gpu"],
    )

    # Cloud reset configuration
    for i in range(type_poses["cloud_reset"]):
        cl_reset = get_cloud_reset(i)
        cl_reset = get_overridden_args(cl_reset, f"cloud_reset_{i}")
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
        m = get_overridden_args(m, f"modulation_{i}")
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

    # Static efield configuration
    for i in range(type_poses["static_efield"]):
        s = get_static_efield_inputs(i)
        s = get_overridden_args(s, f"static_efield_{i}")
        config_controller.configur_static_efield(
            i,
            s["uid"],
            s["amp"],
            s["x_bound"],
            s["y_bound"],
            s["z_bound"],
            s["ex0"],
            s["exx1"],
            s["exx2"],
            s["exy1"],
            s["exy2"],
            s["exz1"],
            s["exz2"],
            s["ey0"],
            s["eyx1"],
            s["eyx2"],
            s["eyy1"],
            s["eyy2"],
            s["eyz1"],
            s["eyz2"],
            s["ez0"],
            s["ezx1"],
            s["ezx2"],
            s["ezy1"],
            s["ezy2"],
            s["ezz1"],
            s["ezz2"],
            s["x_shift"],
            s["y_shift"],
            s["z_shift"],
        )

    # Ion cloud configuration
    for i in range(type_poses["cloud"]):
        c = get_cloud_inputs(i)
        c = get_overridden_args(c, f"cloud_{i}")
        config_controller.configur_ion_cloud(
            i, c["uid"], c["species"], c["radius"], c["count"]
        )

    # Late Ion Clouds
    for i in range(type_poses["late_cloud"]):
        lc = get_late_cloud_inputs(i)
        lc = get_overridden_args(lc, f"late_cloud_{i}")
        config_controller.configur_late_cloud(
            i, lc["uid"], lc["species"], lc["radius"], lc["count"]
        )

    # Trap configuration
    for i in range(type_poses["trap"]):
        t = get_trap_inputs(i)
        t = get_overridden_args(t, f"trap_{i}")
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
        cl = get_overridden_args(cl, f"cooling_laser_{i}")
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
        sl = get_overridden_args(sl, "scattering_laser")
        config_controller.configur_scattering_laser(
            sl["scattered_ion_indices"],
            sl["target_species"],
            sl["laser_direction"],
            sl["saturation_paramater"],
            sl["frequency"],
        )

    # Experiment sequence configuration FIXME: there should be some way of identifying and throwing error / warning if there is no evolve object
    exp_seq = get_exp_seq()
    if "iter" in exp_seq:
        it = get_iter_inputs()
        it = get_overridden_args(it, "iter")
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
    """
    Executes simulations based on a batch of configuration files.

    This function retrieves a list of `.ini` configuration files from a specified 
    batch directory and runs simulations for each configuration file using the 
    `run_from_file` function in optimization mode. It is designed to facilitate 
    batch processing of experiments in the Quantum Logic Ion Control Simulator.

    Args:
        **kwargs: Additional keyword arguments that may be used for future 
            enhancements related to batch optimization.

    Returns:
        None: This function does not return a value; it executes simulations 
        based on the configurations found in the batch directory.

    Raises:
        ValueError: If the batch directory does not contain any `.ini` files.
    """

    # TODO arguments are for the future implementation of an "optimize from batch" mode.  This optimize mode is different from the optimize_mode arg of run_from_file()
    # TODO maybe at some point should make the data naming more helpful
    b_parent = batch_config_dialogue()
    # Get a list of paths to each .ini file in b_parent
    ini_files = [
        os.path.join(b_parent, file)
        for file in os.listdir(b_parent)
        if file.endswith(".ini")
    ]
    for ini_file in ini_files:
        run_from_file(optimize_mode=True, exp=ini_file)


def config_file_dialogue():
    """
    Prompts the user to enter a configuration file path.

    This function uses an interactive prompt to request the user to provide 
    the path to a configuration file with a `.ini` extension. It validates 
    the input to ensure that it is a valid file path, allowing for proper 
    configuration loading in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        str: The path to the configuration file entered by the user.

    Raises:
        ValueError: If the input is not a valid file path.
    """

    return inquirer.filepath(
        message="Enter a configuration (*.ini) file:",
        validate=PathStringValidator(
            is_file=True,
            message="Input is not a valid filpath.  Make sure input is not a string.",
        ),  # TODO validate that it is also a .ini file
    ).execute()


def batch_config_dialogue():
    """
    Prompts the user to enter a directory containing batch configuration files.

    This function uses an interactive prompt to request the user to provide 
    the path to a parent directory that contains `.ini` files for batch processing. 
    It validates the input to ensure that it is a valid directory, facilitating 
    the setup of batch configurations in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        str: The path to the directory entered by the user.

    Raises:
        ValueError: If the input is not a valid directory.
    """

    return inquirer.filepath(
        message="Enter the parent directory of .ini files to submit as a batch.  Be sure to prime the data folder.",
        validate=PathStringValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
    ).execute()


def mode_dialogue():
    """
    Prompts the user to select an operational mode for the simulator.

    This function presents a list of available modes for the Quantum Logic Ion Control 
    Simulator and allows the user to select one. The selected mode determines the 
    subsequent actions and configurations for the simulation.

    Args:
        None: This function does not take any arguments.

    Returns:
        str: The mode selected by the user from the available options.

    Raises:
        ValueError: If the user input is invalid or not recognized.
    """

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
    """
    Loads the configuration from a specified .ini file.

    This function reads the configuration settings from the provided .ini file 
    and raises errors if the file is not specified or if the format is incorrect. 
    It ensures that the configuration is properly loaded for use in the simulation.

    Args:
        loading_config_file (str): The path to the .ini configuration file to be loaded.

    Returns:
        ConfigParser: The loaded configuration object.

    Raises:
        FileNotFoundError: If the loading configuration file is not provided.
        ValueError: If the provided file format is not .ini.
    """

    if not loading_config_file or loading_config_file.strip() == "":
        raise FileNotFoundError("Loading configuration file not provided")
    if not loading_config_file.endswith(".ini"):
        raise ValueError("Invalid file format. Only .ini files are supported.")
    loading_configur.read(loading_config_file)
    return loading_configur


def count_type_pos(loading_configur):
    """
    Counts the occurrences of command types in the experimental sequence.

    This function analyzes the command sequence defined in the provided 
    configuration and counts how many times each command type appears. 
    It also checks for the presence of iteration commands and updates the 
    counts accordingly, returning a dictionary that reflects the number of 
    each command type used in the experiment.

    Args:
        loading_configur (ConfigParser): The configuration object containing 
            the experimental sequence and iteration commands.

    Returns:
        dict: A dictionary mapping command types (str) to their respective 
        counts (int).

    Raises:
        KeyError: If the expected keys are not found in the configuration.
    """

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
            command[:2] != "r_" and command[:2] != "d_"
        ):  # this is fine since the removers are a fundamentally different type of command
            type_poses[command] += 1
    return type_poses


def get_sim_skeleton_inputs():
    """
    Retrieves simulation and detection parameters from the configuration.

    This function extracts the simulation parameters and detection settings 
    from the provided configuration. If the detection section is not present, 
    it initializes default values, ensuring that all necessary parameters are 
    available for the simulation skeleton.

    Args:
        None: This function does not take any arguments.

    Returns:
        tuple: A tuple containing two dictionaries:
            - sim_params (dict): A dictionary of simulation parameters.
            - detection_params (dict): A dictionary of detection parameters.

    Raises:
        KeyError: If expected keys are not found in the configuration.
    """

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

def get_ions_inputs():
    """
    Retrieves the ion configurations from the loading configuration.

    This function extracts and returns the ion-related parameters defined in 
    the loading configuration as a dictionary. It provides easy access to the 
    properties of the ions used in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        dict: A dictionary containing the ion configurations from the loading 
        configuration.

    Raises:
        KeyError: If the "ions" section is not found in the loading configuration.
    """
    return dict(loading_configur.items("ions"))

def get_mass_change_inputs(type_pos):
    return dict(loading_configur.items(f"mass_change_{type_pos}"))

def get_constants():
    """
    Retrieves the physical constants from the loading configuration.

    This function extracts and returns the constants defined in the loading 
    configuration as a dictionary. It provides easy access to the fundamental 
    physical constants used throughout the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        dict: A dictionary containing the physical constants from the loading 
        configuration.

    Raises:
        KeyError: If the "constants" section is not found in the loading configuration.
    """
    return dict(loading_configur.items("constants"))
    # TODO maybe a check that all the necessary constant values are assigned

def get_cloud_reset(type_pos):
    """
    Retrieves the reset configuration for a specified ion cloud type.

    This function extracts and returns the parameters defined for resetting 
    a specific ion cloud type from the loading configuration. It provides 
    easy access to the reset settings necessary for managing ion clouds in 
    the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the ion cloud for which to 
            retrieve the reset configuration.

    Returns:
        dict: A dictionary containing the reset parameters for the specified 
        ion cloud type.

    Raises:
        KeyError: If the specified cloud reset configuration is not found 
        in the loading configuration.
    """
    return dict(loading_configur.items(f"cloud_reset_{type_pos}"))

def get_modulation_inputs(type_pos):
    """
    Retrieves the modulation configuration for a specified type.

    This function extracts and returns the parameters defined for a specific 
    modulation type from the loading configuration. It provides easy access to 
    the modulation settings necessary for managing the modulation process in 
    the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the modulation for which to 
            retrieve the configuration.

    Returns:
        dict: A dictionary containing the modulation parameters for the specified 
        type.

    Raises:
        KeyError: If the specified modulation configuration is not found 
        in the loading configuration.
    """
    return dict(loading_configur.items(f"modulation_{type_pos}"))

def get_static_efield_inputs(type_pos):
    """
    Retrieves the static electric field configuration for a specified type.

    This function extracts and returns the parameters defined for a specific 
    static electric field type from the loading configuration. It provides easy 
    access to the static electric field settings necessary for managing the 
    electric field in the Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the static electric field for which 
            to retrieve the configuration.

    Returns:
        dict: A dictionary containing the static electric field parameters for the 
        specified type.

    Raises:
        KeyError: If the specified static electric field configuration is not found 
        in the loading configuration.
    """
    return dict(loading_configur.items(f"static_efield_{type_pos}"))

def get_cloud_inputs(type_pos):
    """
    Retrieves the configuration for a specified ion cloud type.

    This function extracts and returns the parameters defined for a specific 
    ion cloud type from the loading configuration. It provides easy access to 
    the ion cloud settings necessary for managing ion clouds in the Quantum 
    Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the ion cloud for which to 
            retrieve the configuration.

    Returns:
        dict: A dictionary containing the ion cloud parameters for the specified 
        type.

    Raises:
        KeyError: If the specified ion cloud configuration is not found in 
        the loading configuration.
    """
    return dict(loading_configur.items(f"ion_cloud_{type_pos}"))

def get_late_cloud_inputs(type_pos):
    return dict(loading_configur.items(f"late_cloud_{type_pos}"))

def get_trap_inputs(type_pos):
    """
    Retrieves the configuration for a specified trap type.

    This function extracts and returns the parameters defined for a specific 
    trap type from the loading configuration. It provides easy access to the 
    trap settings necessary for managing traps in the Quantum Logic Ion Control 
    Simulator.

    Args:
        type_pos (str): The type or position of the trap for which to 
            retrieve the configuration.

    Returns:
        dict: A dictionary containing the trap parameters for the specified 
        type.

    Raises:
        KeyError: If the specified trap configuration is not found in 
        the loading configuration.
    """
    return dict(loading_configur.items(f"trap_{type_pos}"))


def get_cooling_laser_inputs(type_pos):
    """
    Retrieves the configuration for a specified cooling laser type.

    This function extracts and returns the parameters defined for a specific 
    cooling laser type from the loading configuration. It provides easy access 
    to the cooling laser settings necessary for managing cooling lasers in the 
    Quantum Logic Ion Control Simulator.

    Args:
        type_pos (str): The type or position of the cooling laser for which to 
            retrieve the configuration.

    Returns:
        dict: A dictionary containing the cooling laser parameters for the specified 
        type.

    Raises:
        KeyError: If the specified cooling laser configuration is not found in 
        the loading configuration.
    """
    return dict(loading_configur.items(f"cooling_laser_{type_pos}"))


def get_scattering_laser_inputs():
    """
    Retrieves the configuration for the scattering laser.

    This function extracts and returns the parameters defined for the scattering 
    laser from the loading configuration. It provides easy access to the scattering 
    laser settings necessary for managing the laser in the Quantum Logic Ion Control 
    Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        dict: A dictionary containing the scattering laser parameters from the 
        loading configuration.

    Raises:
        KeyError: If the "scattering_laser" section is not found in the loading configuration.
    """
    return dict(loading_configur.items("scattering_laser"))


def get_iter_inputs():
    """
    Retrieves the configuration for iteration parameters.

    This function extracts and returns the parameters defined for iterations 
    from the loading configuration. It provides easy access to the settings 
    necessary for managing iteration behavior in the Quantum Logic Ion Control 
    Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        dict: A dictionary containing the iteration parameters from the loading 
        configuration.

    Raises:
        KeyError: If the "iter" section is not found in the loading configuration.
    """
    return dict(loading_configur.items("iter"))


def get_exp_seq():
    """
    Retrieves the experimental sequence from the loading configuration.

    This function accesses the loading configuration to obtain the list of 
    commands that define the experimental sequence for the simulation. It 
    provides a straightforward way to access the sequence of operations to be 
    executed in the Quantum Logic Ion Control Simulator.

    Args:
        None: This function does not take any arguments.

    Returns:
        str: The experimental sequence command list retrieved from the loading configuration.

    Raises:
        KeyError: If the "exp_seq" section is not found in the loading configuration.
    """
    return loading_configur.get("exp_seq", "com_list")
