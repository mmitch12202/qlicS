from configparser import ConfigParser
from pathlib import Path

import click
import numpy as np
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

from . import __version__, config_controller, exp_sequence_controller
from .analysis import create_analysis, create_scat_graph
from .command_mapping import give_command_mapping
from .console_dialogue import followup_questions_creator
from .resources import PathStringValidator

loading_configur = ConfigParser()


@click.command()
@click.version_option(version=__version__)
def main():  # sourcery skip: use-named-expression
    """qlicS: Quantum Logic Ion Control Simulator"""

    # Whole user dialogue prepping the configuration before the setup sequence.
    # This will also include loading defaults or saved forms

    mode = mode_dialogue()

    if mode == "Create New Experiment":
        # TODO config updates based on UI dialogue
        create_choices = ["Manually Make New Experiment", "Make New Scan Experiment"]
        create_mode = inquirer.select(
            message="Create Manually?",
            choices=create_choices,
        ).execute()
        if create_mode == create_choices[0]:
            config_controller.setup_sequence()
            command_mapping = give_command_mapping()
            type_poses = {key: 0 for key in command_mapping}

            avail_block_types = list(command_mapping.keys())
            blocks_to_prep = []
            command_str = ""
            add_block = ""
            followup_questions = followup_questions_creator()
            try_again_block = True
            while try_again_block:
                while add_block != "Continue":
                    print(blocks_to_prep)
                    add_block = inquirer.select(
                        message="Next Action:",
                        choices=["Add Block", "Edit Existing", "Continue"],
                    ).execute()
                    if add_block == "Add Block":
                        block_type = inquirer.select(
                            message="Select a Block Type:", choices=avail_block_types
                        ).execute()
                        qs = followup_questions[block_type]
                        if qs:
                            answers = [q.execute() for q in qs]
                            command_str += f"{block_type},"
                            blocks_to_prep.append([block_type, answers])
                            click.echo(f"{block_type} added successfully")
                        elif block_type == "dumping":
                            command_str += f"{block_type},"
                            avail_block_types.remove(block_type)
                            click.echo(
                                f"No further information needed, {block_type} added successfully"
                            )
                        else:
                            command_str += f"{block_type},"
                            click.echo(
                                f"No further information needed, {block_type} added successfully"
                            )
                    elif add_block == "Edit Block":
                        click.echo("No support for editing blocks at this time")
                # Remove last ,
                command_str = command_str[:-1]
                # Chance to edit command_str
                command_str = inquirer.text(
                    message="Change command string if need:", default=command_str
                ).execute()
                try_again_block = not (
                    inquirer.confirm(
                        message=f"Current Blocks:\nBlocks: {blocks_to_prep}\nCom String: {command_str}\nConfirm simulation blocks?"
                    ).execute()
                )
            try_again_sim = True
            while try_again_sim:
                log_steps = inquirer.number(
                    message="Log Steps?", validate=EmptyInputValidator()
                ).execute()
                timesequence = []

                for i in range(command_str.count("evolve")):
                    timestep_dur = inquirer.number(
                        message=f"Timestep Duration (s) for evolve # {i}",
                        float_allowed=True,
                        validate=EmptyInputValidator(),
                    ).execute()
                    timeseq_dur = inquirer.number(
                        message=f"Section Length (timesteps) for evolve # {i}",
                        float_allowed=False,
                        validate=EmptyInputValidator(),
                    ).execute()
                    timesequence.append([timestep_dur, timeseq_dur])
                try_again_sim = not (
                    inquirer.confirm(
                        message=f"Current Sim Params:\nSteps between logs: {log_steps}\nTimesequence {timesequence}"
                    ).execute()
                )
            try_again_det = True
            while try_again_det:
                det_ts_seq = inquirer.text(
                    message="Detection timestep sequence.  Of the form [[start_timestep_1, end_timestep_1], [start_timestep_2, end_timestep_2], ...]",
                    validate=EmptyInputValidator(),
                ).execute()
                det_a = inquirer.number(
                    message="Detector Area (m^2)",
                    float_allowed=True,
                    validate=EmptyInputValidator(),
                ).execute()
                det_eff = inquirer.number(
                    message="Detector Efficiency (0-1.00)",
                    float_allowed=True,
                    min_allowed=0,
                    max_allowed=1,
                    validate=EmptyInputValidator(),
                ).execute()
                det_dist = inquirer.number(
                    message="Detector Distance (m)",
                    float_allowed=True,
                    validate=EmptyInputValidator(),
                ).execute()
                try_again_det = not (
                    inquirer.confirm(
                        message=f"Current Detector Params:\nArea: {det_a}\nEfficiency: {det_eff}\nDist: {det_dist}\nDetection timestep sequence: {det_ts_seq}"
                    )
                ).execute()
            try_again_scattering_laser = True
            while try_again_scattering_laser:
                scattered_ion_indices = inquirer.text(
                    message="Scattered Ion Indices ex. [0, 20]: ",
                    validate=EmptyInputValidator(),
                ).execute()
                target_species = inquirer.text(
                    message="Target Species: ", validate=EmptyInputValidator()
                ).execute()
                laser_direction = inquirer.text(
                    message="Laser Direction Vector List ex. [-0.5, -0.5, -0.7]",
                    validate=EmptyInputValidator(),
                ).execute()
                saturation_paramater = inquirer.number(
                    message="Saturation Paramater: ",
                    float_allowed=True,
                    validate=EmptyInputValidator(),
                ).execute()
                frequency = inquirer.number(
                    message="Frequency: ",
                    float_allowed=True,
                    validate=EmptyInputValidator(),
                ).execute()
                try_again_scattering_laser = not (
                    inquirer.confirm(
                        message=f"Current Scattering Laser:\nIon Indices: {scattered_ion_indices}\nTarget Species: {target_species}\nLaser Direction: {laser_direction}\nSaturation Paramater: {saturation_paramater}\nFrequency: {frequency}"
                    )
                ).execute()

            final_confirm = inquirer.confirm(
                message=(
                    f"\n\n\nOne day you will have the choice to make final edits to the simulation here,\n"
                    f"but for now you have no choice but to go forward.  Good luck!\n\n\n"
                    f"Experiment Information:\n\n"
                    f"Blocks:\n {blocks_to_prep}\n\n"
                    f"******************************************************\n"
                    f"Detection\n"
                    f"Detector Information:\n"
                    f"Detector Area: {det_a}  Detector Efficiency: {det_eff}  Detector Distance: {det_dist}\n"
                    f"Detector Timestep Sequence: {det_ts_seq}\n"
                    f"Scattering Laser Information:\n"
                    f"Active Ion Indices: {scattered_ion_indices}\n"
                    f"Target Species: {target_species}\n"
                    f"Laser Direction: {laser_direction}\n"
                    f"Saturation Paramater: {saturation_paramater}\n"
                    f"Frequency: {frequency}\n"
                    f"******************************************************\n"
                    f"Simulation Information:\n\n"
                    f"Experimental Sequence: {command_str}\n"
                    f"Steps between log events: {log_steps}\n"
                    f"Evolution Sequence: {timesequence}\n"
                )
            ).execute()
            # writing to config now...
            config_controller.create_sim_skeleton(
                log_steps, timesequence, det_ts_seq, det_a, det_eff, det_dist
            )
            config_controller.configur_scattering_laser(
                scattered_ion_indices,
                target_species,
                laser_direction,
                saturation_paramater,
                frequency,
            )
            for b in blocks_to_prep:
                print(b)
                if b[0] == "cloud":
                    config_controller.configur_ion_cloud(type_poses[b[0]], *b[1])
                elif b[0] == "trap":
                    config_controller.configur_trap(type_poses[b[0]], *b[1])
                elif b[0] == "cooling_laser":
                    config_controller.configur_cooling_laser(type_poses[b[0]], *b[1])
                elif b[0] == "tickle":
                    config_controller.configur_modulation(type_poses[b[0]], *b[1])

                type_poses[b[0]] += 1

            config_controller.create_exp_seq(
                command_str
            )  # also need to put detection in config
            config_controller.commit_changes()
            # NOTE: IM THINKING WE CHANGE THIS INTO PURE CONFIG FILE GENERATION, NOT
            # RUNNING SIM
            # exp_sequence_controller.create_and_run_sim_gen()

        elif create_mode == create_choices[1]:
            print("TODO")  # TODO

        click.echo("Create New Experiment")
    elif mode == "Run Experiment From File":
        run_from_file()
    elif mode == "Edit Existing Experiment":
        config_file = inquirer.filepath(
            message="Enter a configuration (*.ini) file:",
            validate=PathStringValidator(
                is_file=True,
                message="Input is not a valid filpath.  Make sure input is not a string.",
            ),  # TODO validate that it is also a .ini file
        ).execute()
        setup_loading_configur(config_file)
        click.echo(
            "Editing existing experiments in the app will be supported at some later date."
        )
    elif mode == "Analyze Completed Experiment":
        data_file = inquirer.filepath(
            message="Enter a data (*.txt) file or a scattering (*.csv) file:",
            validate=PathStringValidator(
                is_file=True,
                message="Input is not a valid filpath.  Make sure input is not a string.",
            ),  # TODO validate that it is also a .txt file
        ).execute()
        if data_file[-4:] == '.txt':
            click.echo(
                "### Analysis is Currently only supported for all Atoms### \n### be sure you know which species lines up with which atom index###\n\n"
            )
            # TODO we should also include averaging and by species output here
            # TODO we should also include crystal state at given timestep
            data_vars = inquirer.checkbox(
                message="Select the variables you would like to recieve information for (use [Tab] to select and [Enter] to submit):",
                choices=["Positions", "Velocities"],
                validate=lambda result: len(result) >= 1,
                invalid_message="Select at least 1",
            ).execute()
            analysis_root, raw_txt = create_analysis(data_vars, data_file)
        elif data_file[-4:] == '.csv':
            # Make scattering graph
            create_scat_graph(data_file)
        else:
            raise ValueError("The input file extension should be .txt (ion data) or .csv (scattering data)")




def run_from_file():
    config_file = config_file_dialogue()

    loading_configur = setup_loading_configur(config_file)
    config_controller.setup_sequence()

    type_poses = count_type_pos(loading_configur)

    s_p, d_p = get_sim_skeleton_inputs()
    config_controller.create_sim_skeleton(
        s_p["log_steps"],
        s_p["timesequence"],
        d_p["detection_timestep_seq"],
        d_p["detector_area"],
        d_p["detector_effeciency"],
        d_p["detector_distance"],
    )

    for i in range(type_poses["tickle"]):
        m = get_modulation_inputs(i)
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

    for i in range(type_poses["cloud"]):
        c = get_cloud_inputs(i)
        config_controller.configur_ion_cloud(i, c["uid"], c["species"], c["radius"], c["count"])

    for i in range(type_poses["trap"]):
        t = get_trap_inputs(i)
        config_controller.configur_trap(
            i,
            t["target_ion_pos"],
            t["radius"],
            t["length"],
            t["kappa"],
            t["frequency"],
            t["voltage"],
            t["endcapvoltage"],
            t["pseudo"],
        )

    for i in range(type_poses["cooling_laser"]):
        cl = get_cooling_laser_inputs(i)
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

    sl = get_scattering_laser_inputs()
    config_controller.configur_scattering_laser(
        sl["scattered_ion_indices"],
        sl["target_species"],
        sl["laser_direction"],
        sl["saturation_paramater"],
        sl["frequency"],
    )
    exp_seq = get_exp_seq()
    # TODO we are assuming only one iter object for now - this could be generalized but I'm not sure how useful it would be to
    if 'iter' in exp_seq:
        it = get_iter_inputs()
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
    exp_sequence_controller.create_and_run_sim_gen()



def config_file_dialogue():
    return inquirer.filepath(
        message="Enter a configuration (*.ini) file:",
        validate=PathStringValidator(
            is_file=True,
            message="Input is not a valid filpath.  Make sure input is not a string.",
        ),  # TODO validate that it is also a .ini file
    ).execute()


def mode_dialogue():
    return inquirer.select(
        message="Select a mode",
        choices=[
            "Create New Experiment",
            "Run Experiment From File",
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
    # Check if there are commands from the iter
    if loading_configur.has_option("iter", "com_list"):
        iter_command_string = loading_configur.get("iter", "com_list").split(",")
        for i in iter_command_string: 
            if i not in command_string:
                command_string.append(i)
    for command in command_string:
        if command[:2] != "r_": # this is fine since the removers are a fundamentally different type of command
            type_poses[command] += 1
    return type_poses


def get_sim_skeleton_inputs():
    sim_params = loading_configur.items("sim_parameters")
    detection_params = loading_configur.items("detection")
    return dict(sim_params), dict(detection_params)


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
