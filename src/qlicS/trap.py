# Generating the pylion trap object (LAMMPS code) we want
from .config_controller import configur
from .pylion import functions as pl_func


def gen_trap_lammps(uid, ions, type_pos):
    """
    Generates a LAMMPS command for a linear Paul trap.

    This function retrieves the parameters for a specified trap type from the 
    configuration and constructs a command to create a linear Paul trap in 
    the LAMMPS simulation. It allows for the specification of the trap's 
    characteristics and the ions that will be affected by the trap.

    Args:
        uid (str): A unique identifier for the trap being created.
        ions (list): A list of ions that will be affected by the trap.
        type_pos (str): The type or position of the trap being configured.

    Returns:
        object: The result of the LAMMPS command for the linear Paul trap.

    Raises:
        KeyError: If the required trap parameters are not found in the configuration.
    """

    trap_params = {i[0]: eval(i[1]) for i in configur.items(f"trap_{type_pos}")}
    a = not trap_params["pseudo"]
    return pl_func.linearpaultrap(uid=uid, trap=trap_params, ions=ions, all=a)
