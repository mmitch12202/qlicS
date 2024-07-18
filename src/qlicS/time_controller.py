# Controls Timestep sequence and evolution
from .config_controller import configur, dump_dir
from .pylion import functions as pl_func


def evolve(add=None):

    time_sequence = get_time_seq()
    print(time_sequence)
    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))

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
    time_sequence = get_time_seq()
    if configur.has_option("iter", "iter_timesequence"):
        time_sequence += eval(configur.get("iter", "iter_timesequence"))

    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))
    return time_sequence[current_timeblock_num][0]


def get_time_seq():
    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    if configur.has_option("iter", "iter_timesequence"):
        time_sequence = iter_correction(time_sequence)
    return time_sequence


def get_dt_given_timestep(timestep):
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
    iterations = len(eval(configur.get("iter", "scan_var_seq")))
    time_sequence += eval(configur.get("iter", "iter_timesequence")) * iterations
    return time_sequence
