import ast
import csv
import os
import re
import sys

from .command_mapping import give_command_mapping
from .config_controller import configur
from .ion_creation import cloud_reset, pylion_cloud, mass_change, lammps_append_sph_cloud
from .laser_cooling_force import create_cooling_laser
from .pylion import pylion as pl
from .remover import delete_atoms_by_uid, remove_by_uid
from .scattering import get_scattering
from .sim_controller import pylion_dumping
from .tickle_efield import create_tickle
from .time_controller import evolve
from .trap import gen_trap_lammps
from .arbitrary_static_efield import create_static_field


# TODO at some point want evolve to follow the pattern of the rest and the if statement to not exist. But
# doesn't limit us functionally now.
def create_and_run_sim_gen():
    s = pl.Simulation("test")
    if configur.has_option("sim_parameters", "gpu") and eval(
        configur.get("sim_parameters", "gpu")
    ):
        s.attrs["gpu"] = True

    if configur.has_option("sim_parameters", "lammps_boundary_style"):
        boundary_style_input = eval(configur.get("sim_parameters", "lammps_boundary_style"))
        s.attrs["domain_type"] = [boundary_style_input[0], boundary_style_input[1], boundary_style_input[2]]

    if configur.has_option("sim_parameters", "lammps_boundary_locations"):
        boundary_loc_input = eval(configur.get("sim_parameters", "lammps_boundary_locations"))
        s.attrs["domain"] = [boundary_loc_input[0][1], boundary_loc_input[1][1], boundary_loc_input[2][1]] # TODO we can clean this up for non-centered boxes (or at least don't pretend like we support them)

    if configur.has_option("sim_parameters", "lammps_allow_lost"):
        s.attrs["allow_lost"] = eval(configur.get("sim_parameters", "lammps_allow_lost"))

    commands = configur.get("exp_seq", "com_list").split(
        ","
    )  # Assuming commands are separated by commas
    command_mapping = give_command_mapping()
    type_poses = {key: [0] for key in command_mapping}
    ion_groups = []
    com_appending(s, commands, command_mapping, type_poses, ion_groups, False)

    # sys.stdout = open(os.devnull, 'w')
    # sys.stderr = open(os.devnull, 'w')
    s.execute()
    # sys.stdout = sys.__stdout__
    # sys.stderr = sys.__stderr__

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


def append_iter(s, ion_groups):
    config_dict = dict(configur.items("iter"))
    scan_objects = ast.literal_eval(config_dict["scan_objects"])
    scan_var = ast.literal_eval(config_dict["scan_var"])
    scan_var_seq = ast.literal_eval(config_dict["scan_var_seq"])
    iter_timesequence = ast.literal_eval(config_dict["iter_timesequence"])
    iter_detection_seq = ast.literal_eval(config_dict["iter_detection_seq"])
    com_list_str = config_dict["com_list"]
    com_list = com_list_str.split(",")
    command_mapping = give_command_mapping()
    stat_type_poses = {key: [None] for key in command_mapping}
    original_uids = {}
    for scan_object in scan_objects:
        w, i = separate_word_and_int(scan_object)
        if i is not None:
            if w not in stat_type_poses or stat_type_poses[w] == [None]:
                stat_type_poses[w] = [
                    i
                ]  # FIXME We currently overwrite and dont account for iter objects of the same type
            else:
                stat_type_poses[w].append(i)
            original_uids[scan_object] = eval(configur.get(scan_object, "uid"))
    for key, value in stat_type_poses.items():
        if value == [None]:
            stat_type_poses[key] = [0]
    for i, scan_var_val in enumerate(scan_var_seq):
        i_steps = i  # + 1 by getting rid of the plus one this means the same object in an exp_seq and a iter needs to be two different objects
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
                if k[:9] == "ion_cloud":
                    delete_atoms_by_uid(s, original_uids[k] + i_steps)
                else:
                    remove_by_uid(s, original_uids[k] + i_steps)
            if k[:12] == "cooling_laser":
                remove_by_uid(s, "hterm")
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
    evolve_add = [None]
    i_object_num_record = {key: 0 for key in type_poses}
    for command in commands:
        if command == "iter":
            append_iter(s, ion_groups)
            continue
        elif command[:2] == "r_":
            r_uid = int(command[2:])
            if is_iter:
                r_uid += iter_step
            remove_by_uid(s, str(r_uid))
            continue
        elif command[:2] == "d_":
            d_uid = int(command[2:])
            if is_iter:
                d_uid += iter_step
            delete_atoms_by_uid(s, str(d_uid))
            continue
        elif command not in command_mapping:
            raise ValueError(f"Command {command} is not recognized")
        func = command_mapping[command]
        if func == pylion_cloud:
            cloud_self_uid = eval(
                configur.get(
                    f"ion_cloud_{type_poses[command][i_object_num_record[command]]}",
                    "uid",
                )
            )
            if is_iter:
                cloud_self_uid += iter_step
            pl_cloud = func(
                type_poses[command][i_object_num_record[command]], cloud_self_uid
            )
            ion_groups.append(pl_cloud)
            s.append(pl_cloud)
            if is_iter:
                i_object_num_record[command] += 1
        elif func == lammps_append_sph_cloud:
            late_cloud_self_uid = eval(
                configur.get(
                    f"late_cloud_{type_poses[command][i_object_num_record[command]]}",
                    "uid",
                )
            )
            if is_iter:
                late_cloud_self_uid += iter_step
            l_cloud = func(
                type_poses[command][i_object_num_record[command]], late_cloud_self_uid
            )
            s.append(l_cloud)
            if is_iter:
                i_object_num_record[command] += 1
        elif func == gen_trap_lammps:
            if not ion_groups and not is_iter:
                raise SyntaxError("Trap must come after ion creation")
            type_pos = eval(
                configur.get(
                    f"trap_{type_poses[command][i_object_num_record[command]]}",
                    "target_ion_pos",
                )
            )
            self_uid = eval(
                configur.get(
                    f"trap_{type_poses[command][i_object_num_record[command]]}", "uid"
                )
            )
            if is_iter:
                self_uid += iter_step
            s.append(
                func(
                    self_uid,
                    ion_groups[type_pos],
                    type_poses[command][i_object_num_record[command]],
                )
            )
            if is_iter:
                i_object_num_record[command] += 1
        elif func == create_cooling_laser:
            if not ion_groups and not is_iter:
                raise SyntaxError("Laser cooling must come after ion creation")
            type_pos = eval(
                configur.get(
                    f"cooling_laser_{type_poses[command][i_object_num_record[command]]}",
                    "target_ion_pos",
                )
            )
            cooling_ion_name = configur.get(
                f"cooling_laser_{type_poses[command][i_object_num_record[command]]}",
                "target_ion_type",
            )
            self_uid = eval(
                configur.get(
                    f"cooling_laser_{type_poses[command][i_object_num_record[command]]}",
                    "uid",
                )
            )
            ion_cooling_data = eval(configur.get("ions", cooling_ion_name))[1]
            target_uid = eval(configur.get(f"ion_cloud_{type_pos}", "uid"))
            if is_iter:
                self_uid += iter_step
            l = func(
                self_uid,
                ion_cooling_data,
                target_uid,
                type_poses[command][i_object_num_record[command]],
            )
            s.append(
                l
            )  # TODO I think there may be a bug here where if an ion cloud is never created and cooling is only done in iter, it tries to run the sim (and obviously failes)
            evolve_add.append(l["additional_lines"])
            if is_iter:
                i_object_num_record[command] += 1
        elif func == pylion_dumping:
            s.append(func())
        elif func == evolve:
            s.append(func(evolve_add[-1]))
        elif (
            func == create_tickle
        ):  # TODO this is a little sketchy how it has both a 'tickle' and 'modulation' key
            if is_iter:
                self_uid = eval(
                    configur.get(
                        f"modulation_{type_poses['modulation'][i_object_num_record['modulation']]}",
                        "uid",
                    )
                )
                self_uid += iter_step
                s.append(
                    func(
                        type_poses["modulation"][i_object_num_record["modulation"]],
                        self_uid,
                    )
                )
                i_object_num_record["modulation"] += 1
            else:
                self_uid = eval(
                    configur.get(f"modulation_{type_poses[command][0]}", "uid")
                )
                s.append(func(type_poses[command][0], self_uid))
        elif func == create_static_field: # NOTE I blindly copied much of the logic from the modulation block, if errors check here
            if is_iter:
                self_uid = eval(
                    configur.get(
                        f"static_efield_{type_poses['static_efield'][i_object_num_record['static_efield']]}",
                        "uid",
                    )
                )
                self_uid += iter_step
                s.append(
                    func(
                        type_poses["static_efield"][i_object_num_record["static_efield"]],
                        self_uid,
                    )
                )
                i_object_num_record["static_efield"] += 1
            else:
                self_uid = eval(
                    configur.get(f"static_efield_{type_poses[command][0]}", "uid")
                )
                s.append(func(type_poses[command][0], self_uid))
        elif func == cloud_reset:
            s.append(
                func(type_poses[command][i_object_num_record[command]])
            )  # TODO can prolly merge with below
            if is_iter:
                i_object_num_record[command] += 1
        else:
            s.append(func(type_poses[command][i_object_num_record[command]]))
            if is_iter:
                i_object_num_record[command] += 1
        if not is_iter:
            type_poses[command][0] += 1
