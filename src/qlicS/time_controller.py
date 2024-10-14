# Controls Timestep sequence and evolution
from .config_controller import configur, dump_dir
from .pylion import functions as pl_func


def evolve(add=None):
    """
    Advances the simulation by one timestep based on the current time sequence.

    This function retrieves the current time sequence and updates the simulation 
    state by evolving it for the specified duration. It also updates the current 
    timestep position in the configuration and writes the updated configuration to a file.

    Args:
        add (optional): Additional parameters to be passed to the evolution function.

    Returns:
        dict: A dictionary containing the commands for the updated timestep and 
        the evolution code.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """


    time_sequence = get_time_seq()
    print(time_sequence)
    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))
    print(current_timeblock_num)
    dt = time_sequence[current_timeblock_num][0]
    Deltat = time_sequence[current_timeblock_num][1]
    set_timestep = [f"timestep {dt}"]
    evolve = pl_func.evolve(Deltat, add)
    current_timeblock_num += 1
    configur.set("live_vars", "current_timesequence_pos", str(current_timeblock_num))
    with open(f"{dump_dir(setup=False)}config.ini", "w") as configfile:
        configur.write(configfile)
    return {"code": set_timestep + evolve["code"]}


def get_current_dt():  # Make it clear that this is only for simulation generation,
    # for analysis use get_dt_given_timestep()
    """
    Retrieves the current timestep duration for the simulation.

    This function calculates the current timestep based on the simulation's time 
    sequence and the current position in that sequence. It also incorporates any 
    additional iteration timesteps if they are defined in the configuration.

    Args:
        None: This function does not take any arguments.

    Returns:
        float: The duration of the current timestep for the simulation.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """

    time_sequence = get_time_seq()
    if configur.has_option("iter", "iter_timesequence"):
        time_sequence += eval(configur.get("iter", "iter_timesequence"))

    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))
    return time_sequence[current_timeblock_num][0]


def get_time_seq():
    """
    Retrieves and processes the simulation time sequence.

    This function extracts the time sequence from the configuration and limits it 
    based on the number of evolution commands present in the experimental sequence. 
    It also applies any necessary corrections for iteration timesteps if defined in 
    the configuration.

    Args:
        None: This function does not take any arguments.

    Returns:
        list: A list representing the processed time sequence for the simulation.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """

    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    main_com_evolve_count = configur.get("exp_seq", "com_list").count("evolve")
    time_sequence = time_sequence[:main_com_evolve_count]
    if configur.has_option("iter", "iter_timesequence"):
        time_sequence = iter_correction(time_sequence)
    return time_sequence


def get_dt_given_timestep(timestep):
    """
    Retrieves the duration associated with a specific timestep in the simulation.

    This function calculates the duration of the specified timestep by iterating 
    through the time sequence defined in the configuration. It accounts for any 
    corrections related to iteration timesteps and returns the corresponding duration 
    if the timestep falls within the valid range.

    Args:
        timestep (float): The timestep for which to retrieve the corresponding duration.

    Returns:
        float: The duration associated with the specified timestep.

    Raises:
        Exception: If the specified timestep is beyond the simulation duration.
    """

    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    if configur.has_option("iter", "iter_timesequence"):
        time_sequence = iter_correction(time_sequence)
    prev_Delt, nex_Delt = (0,) * 2
    for idx, time_chunk in enumerate(time_sequence):
        if idx != 0:
            prev_Delt += float(time_sequence[idx - 1][1])
        nex_Delt += float(time_chunk[1])
        if timestep < nex_Delt and timestep >= prev_Delt:
            return time_chunk[0]
    # sourcery skip: raise-specific-error
    raise Exception(f"Timestep {timestep} is beyond simulation duration {nex_Delt}")


def iter_correction(time_sequence):
    """
    Adjusts the time sequence by appending iteration timesteps.

    This function modifies the provided time sequence by adding a specified number 
    of iteration timesteps based on the configuration settings. It ensures that the 
    time sequence accurately reflects the total duration of the simulation, including 
    any iterations defined in the configuration.

    Args:
        time_sequence (list): The original time sequence to be corrected.

    Returns:
        list: The updated time sequence with appended iteration timesteps.

    Raises:
        KeyError: If the required keys are not found in the configuration.
    """

    iterations = len(eval(configur.get("iter", "scan_var_seq")))
    time_sequence += eval(configur.get("iter", "iter_timesequence")) * iterations
    return time_sequence
