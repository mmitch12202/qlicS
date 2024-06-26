# Controls Timestep sequence and evolution
from .config_controller import configur, dump_dir
from .pylion import functions as pl_func


def evolve():

    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))

    dt = time_sequence[current_timeblock_num][0]
    Deltat = time_sequence[current_timeblock_num][1]
    set_timestep = [f"timestep {dt}"]
    evolve = pl_func.evolve(Deltat)
    current_timeblock_num += 1
    configur.set("live_vars", "current_timesequence_pos", str(current_timeblock_num))
    configfile = open(dump_dir(setup=False) + "config.ini", "w")
    configur.write(configfile)
    configfile.close()
    return {"code": set_timestep + evolve["code"]}


def get_current_dt():  # Make it clear that this is only for simulation generation,
    # for analysis use get_dt_given_timestep()
    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    current_timeblock_num = eval(configur.get("live_vars", "current_timesequence_pos"))
    return time_sequence[current_timeblock_num][0]


def get_dt_given_timestep(timestep):
    time_sequence = eval(configur.get("sim_parameters", "timesequence"))
    prev_Delt, nex_Delt = (0,) * 2
    for idx, time_chunk in enumerate(time_sequence):
        if not idx == 0:
            prev_Delt += time_sequence[idx - 1][1]
        nex_Delt += time_chunk[1]
        if timestep < nex_Delt and timestep >= prev_Delt:
            return time_chunk[0]
    raise Exception(f"Timestep {timestep} is beyond simulation duration {nex_Delt}")
