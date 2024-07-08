# For all analysis related tasks, including simply reading the dump file
import os
import shutil
import time

import matplotlib.pyplot as plt

from .config_controller import configur
from .pylion import functions as pl_func


def velocities(atom_range=None, step_range=None, velocity_indices=None):
    """
    Retrieves the velocities of atoms from a dump file and
    returns a dictionary mapping atom names to their velocity components.

    Args:
        atom_range (tuple, optional): A tuple specifying the range of atoms to consider.
        Defaults to None.
        step_range (tuple, optional): A tuple specifying the range of steps to consider.
        Defaults to None.
        velocity_indices (list, optional): A list specifying the indices of velocity
        components to extract. Defaults to [3, 6].
    """
    if atom_range is None:
        atom_range = [None, None]
    if step_range is None:
        step_range = [None, None]
    if velocity_indices is None:
        velocity_indices = [3, 6]

    dump_dir = configur.get("directory", "dump_dir")
    _, data = pl_func.readdump(f"{dump_dir}positions.txt")
    return dict(
        zip(
            _,
            data[
                step_range[0] : step_range[1],
                atom_range[0] : atom_range[1],
                velocity_indices[0] : velocity_indices[1],
            ],
        )
    )


def get_number_atoms(raw_data_copy):
    _, data = pl_func.readdump(raw_data_copy)
    return len(data[1])


def create_analysis(var_list, raw_data_file):
    analysis_root = (
        f"{os.getcwd()}/data/analysis" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    )
    os.makedirs(analysis_root)
    raw_copy = f"{analysis_root}raw.txt"
    shutil.copy(raw_data_file, raw_copy)
    num_atoms = get_number_atoms(raw_copy)
    for a_i in range(num_atoms):
        for vartype in var_list:
            graph_dir = f"{analysis_root}atom_{a_i}/{vartype}"
            os.makedirs(graph_dir)
            create_lammps_vars_graphs(graph_dir, raw_copy, vartype, a_i)
    return analysis_root, raw_copy


def create_lammps_vars_graphs(directory, raw_data, vartype, atom_num):
    if vartype == "Positions":
        var_indices = [0, 3]
    elif vartype == "Velocities":
        var_indices = [3, 6]
    steps, data = pl_func.readdump(raw_data)
    sel_d = data[:, atom_num, var_indices[0] : var_indices[1]]
    x = []
    y = []
    z = []
    for i in sel_d:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])
    _extracted_from_create_lammps_vars_graphs_15(steps, x, directory, "/x.png")
    _extracted_from_create_lammps_vars_graphs_15(steps, y, directory, "/y.png")
    _extracted_from_create_lammps_vars_graphs_15(steps, z, directory, "/z.png")
    return


# TODO Rename this here and in `create_lammps_vars_graphs`
def _extracted_from_create_lammps_vars_graphs_15(steps, arg1, directory, arg3):
    plt.scatter(steps, arg1)
    plt.savefig(f"{directory}{arg3}")
    plt.clf()
