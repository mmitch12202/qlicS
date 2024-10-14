"""For all analysis related tasks, including simply reading the dump file """

import math
import os
import shutil
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config_controller import configur
from .pylion import functions as pl_func

# TODO make it so we can color many species in images if we want
def velocities(atom_range=None, step_range=None, velocity_indices=None):
    """
    Retrieves the velocities of atoms from a dump file and returns a dictionary 
    mapping atom names to their corresponding velocity components.

    This function reads atom velocity data from a specified dump file, allowing 
    the user to define ranges for atoms and steps, as well as which velocity 
    components to extract. The resulting dictionary contains atom names as keys 
    and their velocity components as values.

    Args:
        atom_range (tuple, optional): A tuple specifying the range of atoms to consider.
            Defaults to (None, None).
        step_range (tuple, optional): A tuple specifying the range of steps to consider.
            Defaults to (None, None).
        velocity_indices (list, optional): A list specifying the indices of velocity 
            components to extract. Defaults to [3, 6].

    Returns:
        dict: A dictionary mapping atom names to their velocity components.
    """

    if atom_range is None:
        atom_range = [None, None]
    if step_range is None:
        step_range = [None, None]
    if velocity_indices is None:
        velocity_indices = [3, 6]

    dump_dir = configur.get("directory", "dump_dir")
    _, data = pl_func.readdump_inhomogenous(f"{dump_dir}positions.txt")
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
    """Retrieve the number of atoms from the provided raw data.

    This function reads the raw data from a specified source and returns the count of atoms present in the data. It utilizes a helper function to process the raw data and extract the relevant information.

    Args:
        raw_data_copy: The source of the raw data to be analyzed.

    Returns:
        int: The number of atoms found in the raw data.

    Examples:
        >>> count = get_number_atoms("path/to/raw_data.txt")
        >>> int(count)
        True
    """
    _, data = pl_func.readdump_inhomogenous(raw_data_copy)
    return len(data[1])


def create_analysis(var_list, raw_data_file, start):
    """
    Creates an analysis directory and generates graphs for specified variables from raw data.

    This function sets up a structured directory for analysis, copies the provided raw data file, 
    and generates graphs for each atom based on the specified variable types. The resulting 
    directory structure is organized by atom and variable type.

    Args:
        var_list (list): A list of variable types for which graphs will be generated.
        raw_data_file (str): The path to the raw data file to be analyzed.
        start (int): The starting index or parameter for graph generation.

    Returns:
        tuple: A tuple containing the path to the analysis root directory and the path to the 
               copied raw data file.
    """

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
            create_lammps_vars_graphs(graph_dir, raw_copy, vartype, a_i, start)
    return analysis_root, raw_copy


def gen_rmsv_plot(raw_data_file):
    """Generates a plot of the root mean square velocity (RMS V) from raw data.

    This function creates a directory for analysis, copies the provided raw data file, 
    and calculates the RMS velocity for each step in the data. It then generates a plot 
    of the RMS velocity over time and saves it as a PNG file.

    Args:
        raw_data_file (str): The path to the raw data file to be analyzed.

    Returns:
        None: The function saves the RMS velocity plot to the analysis directory.
    """

    analysis_root = (
        f"{os.getcwd()}/data/rms_v" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    )
    os.makedirs(analysis_root)
    raw_copy = f"{analysis_root}raw.txt"
    shutil.copy(raw_data_file, raw_copy)
    steps, data = pl_func.readdump_inhomogenous(raw_copy)

    def calculate_rms(lst):
        """Calculates the root mean square (RMS) of a list of numbers.

        This function takes a list of numerical values and computes the RMS, which is a measure 
        of the magnitude of a varying quantity. If the list is empty, it returns 0 to avoid 
        division by zero errors.

        Args:
            lst (list): A list of numerical values for which to calculate the RMS.

        Returns:
            float: The calculated RMS value, or 0 if the input list is empty.
        """

        if not lst:
            return 0  # Handle the case of an empty list to avoid division by zero
        squared_values = [x**2 for x in lst]
        mean_squared = sum(squared_values) / len(lst)
        rms = math.sqrt(mean_squared)
        return rms

    rmses = []
    for step in data:
        atom_vels = []
        for atom in step:
            v = np.sqrt(atom[3] ** 2 + atom[4] ** 2 + atom[5] ** 2)
            # v = atom[3]
            atom_vels.append(v)
        rms_vel = calculate_rms(atom_vels)
        rmses.append(rms_vel)
    plt.figure()
    plt.plot(steps, rmses, label="RMS V (m/s)")
    plt.xlabel("Step")
    plt.ylabel("RMS V")
    plt.savefig(analysis_root + "RMS_vel_plot.png")


def create_scat_graph(raw_data_file):
    """Generates a scatter plot of photon counts from raw data.

    This function creates a directory for analysis, copies the provided raw data file, 
    and generates a scatter plot of photon counts against a specified variable. The plot 
    is saved as a PNG file in the analysis directory.

    Args:
        raw_data_file (str): The path to the raw data file in CSV format to be analyzed.

    Returns:
        None: The function saves the scatter plot to the analysis directory.
    """

    analysis_root = (
        f"{os.getcwd()}/data/ph_count" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    )
    os.makedirs(analysis_root)
    raw_copy = f"{analysis_root}raw.csv"
    shutil.copy(raw_data_file, raw_copy)
    data = pd.read_csv(raw_copy)
    filtered_data = data[data.iloc[:, 2].notnull()]
    plt.plot(
        filtered_data.iloc[:, 2],
        filtered_data.iloc[:, 3],
        marker="|",
        markersize=10,
        color="lightblue",
        linestyle="-",
        markerfacecolor="black",
        markeredgecolor="black",
    )
    plt.xlabel("scan_var")
    plt.ylabel("# of Photons")
    plt.title("Photon Count vs Iter Var")
    plt.savefig(analysis_root + "count_plot.png")
    return


def create_lammps_vars_graphs(directory, raw_data, vartype, atom_num, start=0):
    """Generates graphs for specified variable types of a given atom from LAMMPS data.

    This function reads raw data from a LAMMPS dump file and extracts the specified 
    variable type (either positions or velocities) for a particular atom. It then 
    generates separate graphs for each component (x, y, z) and saves them in the 
    specified directory.

    Args:
        directory (str): The path to the directory where the graphs will be saved.
        raw_data (str): The path to the raw data file to be analyzed.
        vartype (str): The type of variable to graph, either "Positions" or "Velocities".
        atom_num (int): The index of the atom for which to generate the graphs.
        start (int, optional): The starting index for data extraction. Defaults to 0.

    Returns:
        None: The function saves the generated graphs to the specified directory.
    """

    if vartype == "Positions":
        var_indices = [0, 3]
    elif vartype == "Velocities":
        var_indices = [3, 6]
    steps, data = pl_func.readdump_inhomogenous(raw_data)
    sel_d = data[start:, atom_num, var_indices[0] : var_indices[1]]
    x = []
    y = []
    z = []
    for i in sel_d:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    _extracted_from_create_lammps_vars_graphs_15(steps[start:], x, directory, "/x.png")
    _extracted_from_create_lammps_vars_graphs_15(steps[start:], y, directory, "/y.png")
    _extracted_from_create_lammps_vars_graphs_15(steps[start:], z, directory, "/z.png")
    return


def create_crystal_image_scat(raw_data_file, index, species_cutoff, show):
    """Generates scatter plots of crystal structures from raw data.

    This function creates a directory for analysis, copies the provided raw data file, 
    and generates 2D scatter plots of crystal positions based on specified species. 
    Optionally, it can also display a 3D scatter plot of the crystal structure.

    Args:
        raw_data_file (str): The path to the raw data file to be analyzed.
        index (int): The index of the time step to visualize.
        species_cutoff (int): The cutoff index to separate different species in the data.
        show (bool): A flag indicating whether to display the 3D plot.

    Returns:
        None: The function saves the generated plots and displays them if requested.
    """

    analysis_root = (
        f"{os.getcwd()}/data/crystal_snap" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
    )
    os.makedirs(analysis_root)
    raw_copy = f"{analysis_root}raw.txt"
    shutil.copy(raw_data_file, raw_copy)
    steps, data = pl_func.readdump_inhomogenous(raw_copy)

    x_1 = list(data[index, :species_cutoff, 0])
    x_2 = list(data[index, species_cutoff:, 0])
    y_1 = list(data[index, :species_cutoff, 1])
    y_2 = list(data[index, species_cutoff:, 1])
    z_1 = list(data[index, :species_cutoff, 2])
    z_2 = list(data[index, species_cutoff:, 2])

    fig_flat = plt.figure()
    ax1 = fig_flat.add_subplot(122)
    ax1.scatter(x_1, z_1)
    ax1.scatter(x_2, z_2, c="r")
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("z (m)")

    ax2 = fig_flat.add_subplot(121)
    ax2.scatter(x_1, y_1)
    ax2.scatter(x_2, y_2, c="r")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")

    ratio = 1
    x_left, x_right = ax1.get_xlim()
    y_low, y_high = ax1.get_ylim()
    ax2.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)
    x_left, x_right = ax2.get_xlim()
    y_low, y_high = ax2.get_ylim()
    ax2.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    if show:
        fig3d = plt.figure()
        ax = fig3d.add_subplot(111, projection="3d")
        p1 = ax.scatter(
            data[index, :species_cutoff, 0],
            data[index, :species_cutoff, 1],
            data[index, :species_cutoff, 2],
        )
        p2 = ax.scatter(
            data[index, species_cutoff:, 0],
            data[index, species_cutoff:, 1],
            data[index, species_cutoff:, 2],
            c="r",
        )
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_zlabel("z (m)")

    plt.show()


# TODO Rename this here and in `create_lammps_vars_graphs`
def _extracted_from_create_lammps_vars_graphs_15(steps, arg1, directory, arg3):
    """Generates and saves a scatter plot of data against steps.

    This function creates a scatter plot using the provided steps and data values, 
    saves the plot as a PNG file in the specified directory, and clears the current 
    figure to prepare for future plots.

    Args:
        steps (list): A list of step values to be used as the x-axis of the plot.
        arg1 (list): A list of data values to be plotted against the steps on the y-axis.
        directory (str): The path to the directory where the plot will be saved.
        arg3 (str): The filename for the saved plot, including the file extension.

    Returns:
        None: The function saves the generated plot to the specified directory.
    """

    plt.scatter(steps, arg1)
    plt.savefig(f"{directory}{arg3}")
    plt.clf()
