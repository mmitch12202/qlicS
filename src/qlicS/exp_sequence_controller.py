import ast
import csv
import re

from .command_mapping import give_command_mapping
from .config_controller import configur
from .ion_creation import pylion_cloud
from .laser_cooling_force import create_cooling_laser
from .pylion import pylion as pl
from .remover import remove_by_uid
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
    command_mapping = give_command_mapping()
    type_poses = {key: 0 for key in command_mapping}
    ion_groups = []
    com_appending(s, commands, command_mapping, type_poses, ion_groups, False)
    s.execute()

    if configur.get("detection", "detector_area") == "null":
        return configur.get("directory", "dump_dir")
    scat = get_scattering()
    print(scat)
    with open(
        configur.get("directory", "dump_dir") + "ph_scattering.csv", "w", newline=""
    ) as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header row
        if configur.has_option("iter", "scan_var"):
            scan_var = eval(configur.get("iter", "scan_var"))
            csvwriter.writerow(
                ["det_start", "det_stop", " - ".join(scan_var), "photon count"]
            )
        else:
            csvwriter.writerow(["det_start", "det_stop", "no_scan_var", "photon count"])

        # Write the data rows
        for sublist in scat:
            if len(sublist) == 3:
                csvwriter.writerow([sublist[0], sublist[1], "", sublist[2]])
            elif len(sublist) == 4:
                csvwriter.writerow([sublist[0], sublist[1], sublist[2], sublist[3]])
    return scat


# For expanding select simulation blocks - should most commonly be used for scanning modulation frequency but is completely general
# For now we are just supporting sweeping one variable at a time

# TODO basically a function that takes s as input and appends appropriatly based on the [iter] information


def append_iter(s):
    config_dict = dict(configur.items("iter"))
    scan_objects = ast.literal_eval(config_dict["scan_objects"])
    scan_var = ast.literal_eval(config_dict["scan_var"])
    scan_var_seq = ast.literal_eval(config_dict["scan_var_seq"])
    iter_timesequence = ast.literal_eval(config_dict["iter_timesequence"])
    iter_detection_seq = ast.literal_eval(config_dict["iter_detection_seq"])
    com_list_str = config_dict["com_list"]
    com_list = com_list_str.split(",")
    command_mapping = give_command_mapping()
    stat_type_poses = {key: 0 for key in command_mapping}
    original_uids = {}
    for scan_object in scan_objects:
        w, i = separate_word_and_int(scan_object)
        if i is not None:
            stat_type_poses[w] = i
            original_uids[scan_object] = eval(configur.get(scan_object, "uid"))
    for i, scan_var_val in enumerate(scan_var_seq):  # TODO use scan_var_val
        ion_groups = []  # Not sure if this is the best way of handling this
        i_steps = i + 1
        configur.set(scan_var[0], scan_var[1], str(scan_var_val))
        com_appending(
            s,
            com_list,
            command_mapping,
            stat_type_poses,
            ion_groups,
            True,
            iter_step=i_steps,
        )
        for k in list(original_uids.keys()):
            if str(original_uids[k]) not in com_list_str:
                remove_by_uid(s, original_uids[k] + i_steps)
    return


def separate_word_and_int(input_string):
    if match := re.match(r"^(.*?)(_\d+)?$", input_string):
        word_part = match[1]
        int_part = match[2][1:] if match[2] else None
        return word_part, int_part
    return None, None


def com_appending(
    s, commands, command_mapping, type_poses, ion_groups, is_iter, iter_step=0
):
    for command in commands:
        if command == "iter":
            append_iter(s)
            continue
        elif command[:2] == "r_":
            r_uid = int(command[2:])
            if is_iter:
                r_uid += iter_step
            remove_by_uid(s, str(r_uid))
            continue
        elif command not in command_mapping:
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
            if not ion_groups and not is_iter:
                raise SyntaxError("Laser cooling must come after ion creation")
            type_pos = eval(
                configur.get(f"cooling_laser_{type_poses[command]}", "target_ion_pos")
            )
            cooling_ion_name = configur.get(
                f"cooling_laser_{type_poses[command]}", "target_ion_type"
            )
            self_uid = eval(configur.get(f"cooling_laser_{type_poses[command]}", "uid"))
            ion_cooling_data = eval(configur.get("ions", cooling_ion_name))[1]
            target_uid = eval(configur.get(f"ion_cloud_{type_pos}", "uid"))
            if is_iter:
                self_uid += iter_step
            s.append(
                func(self_uid, ion_cooling_data, target_uid, type_poses[command])
            )  # TODO I think there may be a bug here where if an ion cloud is never created and cooling is only done in iter, it tries to run the sim (and obviously failes)
        elif func in [evolve, pylion_dumping]:
            s.append(func())
        elif func == create_tickle:
            self_uid = eval(configur.get(f"modulation_{type_poses[command]}", "uid"))
            if is_iter:
                self_uid += iter_step
            s.append(func(type_poses[command], self_uid))
        else:
            s.append(func(type_poses[command]))
        if not is_iter:
            type_poses[command] += 1
