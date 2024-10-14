import numpy as np

from .config_controller import configur
from .pylion import functions as pl_func


# Spherical Cloud
def pylion_cloud(type_pos, uid_override=None):
    """
    Creates an ion cloud based on the specified type and configuration.

    This function generates an ion cloud using parameters defined in the 
    configuration, such as species, radius, and count. It allows for an optional 
    override of the unique identifier (UID) for the created ion cloud, enabling 
    flexibility in managing multiple ion clouds within the simulation.

    Args:
        type_pos (str): The type or position of the ion cloud being created.
        uid_override (str, optional): An optional UID to override the default UID 
            from the configuration. Defaults to None.

    Returns:
        dict: A dictionary representing the created ion cloud, including its 
        properties and UID.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """
    c = pl_func.createioncloud(
        eval(configur.get("ions", configur.get(f"ion_cloud_{type_pos}", "species")))[0],
        eval(configur.get(f"ion_cloud_{type_pos}", "radius")),
        eval(configur.get(f"ion_cloud_{type_pos}", "count")),
    )
    if uid_override is not None:
        c["uid"] = uid_override
    else:
        c["uid"] = eval(configur.get(f"ion_cloud_{type_pos}", "uid"))
    return c


# Pulling heavily from the pylion cloud func, but not tied to the jinja template (so we have control over when they are added)
def lammps_append_sph_cloud(type_pos, uid):
    """
    Generates a spherical distribution of ion positions and prepares LAMMPS commands.

    This function creates a specified number of ion positions distributed 
    uniformly within a sphere of a given radius and prepares the corresponding 
    LAMMPS commands for adding these ions to a simulation. It retrieves the 
    necessary parameters from the configuration and constructs the commands 
    needed to append the ions to the simulation.

    Args:
        type_pos (str): The type or position of the ion cloud being created.
        uid (int): A unique identifier for the ions being created.

    Returns:
        dict: A dictionary containing the generated LAMMPS commands, the type of 
        operation, and the mass and charge of the ions.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """

    positions = []
    species = eval(
        configur.get("ions", configur.get(f"late_cloud_{type_pos}", "species"))
    )[0]
    number = eval(configur.get(f"late_cloud_{type_pos}", "count"))
    radius = eval(configur.get(f"late_cloud_{type_pos}", "radius"))
    for _ind in range(number):
        d = np.random.random() * radius
        a = np.pi * np.random.random()
        b = 2 * np.pi * np.random.random()

        positions.append(
            [d * np.sin(a) * np.cos(b), d * np.sin(a) * np.sin(b), d * np.cos(a)]
        )
    lines = ["\n# Variable ion creation (sphere)\n"]
    lines.extend(
        f"create_atoms {uid} single {' '.join(str(d) for d in position)} units box\n"
        for position in positions
    )
    species_prep = [
        "\n # Species...\n",
        f"mass {uid} {eval(configur.get('constants', 'amu')) * species['mass']}\n",
        f"set type {uid} charge {eval(configur.get('constants', 'ele_charge')) * species['charge']}\n",
        f"group {uid} type {uid}\n",
    ]
    t_int = ["\nfix timeIntegrator nonRigidBody nve\n"]

    return {
        "code": lines+t_int,
        "type": "live ion append",
        "mass": species["mass"],
        "charge": species["charge"],
    }


def recloud_spherical(type_pos):
    """
    Generates new positions for ions in a spherical distribution.

    This function calculates new positions for a specified number of ions 
    within a sphere of a given radius, based on the configuration settings 
    for the specified ion cloud type. It constructs the necessary commands 
    to reset the positions of these ions in the simulation.

    Args:
        type_pos (str): The type or position of the ion cloud being reset.

    Returns:
        dict: A dictionary containing the generated commands to reset the 
        positions of the ions.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """

    number = eval(configur.get(f"cloud_reset_{type_pos}", "count"))
    radius = eval(configur.get(f"cloud_reset_{type_pos}", "radius"))
    initial_atom_id = eval(configur.get(f"cloud_reset_{type_pos}", "initial_atom_id"))

    positions = []
    for _ind in range(number):
        d = np.random.random() * radius
        a = np.pi * np.random.random()
        b = 2 * np.pi * np.random.random()

        positions.append(
            [d * np.sin(a) * np.cos(b), d * np.sin(a) * np.sin(b), d * np.cos(a)]
        )
    lines = ["\n# Reset the position of the ions"]
    lines.extend(
        f"set atom {i+initial_atom_id} x {position[0]} y {position[1]} z {position[2]}\n"
        for i, position in enumerate(positions)
    )
    return {"code": lines}


def cloud_reset(type_pos):
    """
    Resets the configuration of an ion cloud based on its type.

    This function retrieves the reset style for a specified ion cloud type 
    from the configuration and calls the appropriate function to reset the 
    cloud's positions. Currently, it supports resetting clouds in a spherical 
    distribution.

    Args:
        type_pos (str): The type or position of the ion cloud to be reset.

    Returns:
        dict: The result of the reset operation, which may include commands 
        for repositioning the ions.

    Raises:
        KeyError: If the specified cloud type does not exist in the configuration.
    """

    style = configur.get(f"cloud_reset_{type_pos}", "style")
    if style == "sphere":
        return recloud_spherical(type_pos)

# For chemical reaction modeling, probably doesn't belong in ion_creation
def mass_change(uid, new_mass):
    lines = [f"\nmass {uid} {new_mass}\n"]
    return {"code": lines}

