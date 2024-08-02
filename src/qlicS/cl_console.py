import click
import numpy as np
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from . import __version__, config_controller, exp_sequence_controller
from .analysis import create_analysis, create_scat_graph, gen_rmsv_plot, create_crystal_image_scat
from .command_mapping import give_command_mapping
from .console_resources import (
    config_file_dialogue,
    followup_questions_creator,
    mode_dialogue,
    run_from_file,
    setup_loading_configur,
    run_from_batch,
)
from .mloop_controller import mainmloop
from .resources import PathStringValidator


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
    elif mode == "Run Experiment Batch From Directory":
        # TODO untested!
        run_from_batch()
    elif mode == "Optimize Experiment with M-LOOP":
        config_file = config_file_dialogue()
        mloop_formulae = inquirer.filepath(
            message="Enter a mloop_formulae (.py) file per the docs:",
            validate=PathStringValidator(
                is_file=True,
                message="Input is not a valid filpath.  Make sure input is not a string.",
            ), # TODO validate that it is also a .py file
        ).execute()
        mainmloop(config_file, mloop_formulae)
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
            "Editing existing experiments in the app will be supported at some later date.  For now, just edit the .ini file directly."
        )
    elif mode == "Analyze Completed Experiment":
        data_file = inquirer.filepath(
            message="Enter a data (*.txt) file or a scattering (*.csv) file:",
            validate=PathStringValidator(
                is_file=True,
                message="Input is not a valid filpath.  Make sure input is not a string.",
            ),  # TODO validate that it is also a .txt file
        ).execute()
        if data_file[-4:] == ".txt":
            txt_choice = inquirer.select(
                message="Would you like to generate whole crystal rms velocity data, analyze atoms individually, or take a crystal snapshot? (use arrows)",
                choices=["Whole", "Individual", "Crystal Image"],
                default=None,
            ).execute()
            if txt_choice == "Whole":
                gen_rmsv_plot(data_file)
            elif txt_choice == "Individual":
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
                start = inquirer.number(
                    message="Enter graph start log step (=timestep/log_steps):",
                    min_allowed=0,
                    validate=EmptyInputValidator(),
                ).execute()
                analysis_root, raw_txt = create_analysis(
                    data_vars, data_file, int(start)
                )
            elif txt_choice == "Crystal Image":
                image_index = inquirer.number(
                    message="Enter the index of the crystal image you want to take (target_timestep/log_steps).\n  If you want the crystal at the end of the simulation enter -1.",
                    validate=EmptyInputValidator(),
                ).execute()
                spec_cutoff = inquirer.number(
                    message="Enter the atom index of the species cutoff (for coloring.  Ex: if there are 10 of species 1 and 5 of species 2, enter 9)",
                    validate=EmptyInputValidator(),
                ).execute()
                show = inquirer.select(
                    message="Would you like to show a 3D plot as well as the orthogonal projection?",
                    choices=["Yes", "No"],
                    transformer = lambda input_string: True if input_string == "Yes" else False
                ).execute()
                create_crystal_image_scat(data_file, int(image_index), int(spec_cutoff), show)
        elif data_file[-4:] == ".csv":
            # Make scattering graph
            create_scat_graph(data_file)
        else:
            raise ValueError(
                "The input file extension should be .txt (ion data) or .csv (scattering data)"
            )
