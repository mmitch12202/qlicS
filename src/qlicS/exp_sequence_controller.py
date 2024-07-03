from .command_mapping import command_mapping
from .config_controller import configur
from .ion_creation import pylion_cloud
from .laser_cooling_force import create_cooling_laser
from .pylion import pylion as pl
from .scattering import get_scattering
from .sim_controller import pylion_dumping
from .tickle_efield import create_tickle
from .time_controller import evolve
from .trap import gen_trap_lammps


# TODO at some point want evolve to follow the pattern of the rest and the if statement to not exist. But
# doesn't limit us functionally now.
def create_and_run_sim_gen():
    s = pl.Simulation("test")
    commands = configur.get("exp_seq", "com_list").split(
        ","
    )  # Assuming commands are separated by commas

    type_poses = {key: 0 for key in command_mapping}
    ion_groups = []
    for command in commands:
        if command not in command_mapping:
            raise ValueError(f"Command {command} is not recognized")
        func = command_mapping[command]
        if func == pylion_cloud:
            pl_cloud = func(type_poses[command])
            ion_groups.append(pl_cloud)
            s.append(pl_cloud)
        elif func == gen_trap_lammps:
            if not ion_groups:
                raise SyntaxError("Trap must come after ion creation")
            type_pos = eval(
                configur.get(f"trap_{type_poses[command]}", "target_ion_pos")
            )
            s.append(func(ion_groups[type_pos], type_poses[command]))
        elif func == create_cooling_laser:
            if not ion_groups:
                raise SyntaxError("Laser cooling must come after ion creation")
            type_pos = eval(
                configur.get(f"cooling_laser_{type_poses[command]}", "target_ion_pos")
            )
            cooling_ion_name = configur.get(
                f"cooling_laser_{type_poses[command]}", "target_ion_type"
            )
            ion_cooling_data = eval(configur.get("ions", cooling_ion_name))[1]
            s.append(func(ion_cooling_data, ion_groups[0]["uid"], type_poses[command]))
        elif func in [evolve, pylion_dumping]:
            s.append(func())
        else:
            s.append(func(type_poses[command]))
        type_poses[command] += 1
    s.execute()

    # Analysis
    print(get_scattering())
