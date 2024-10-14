from .config_controller import configur
from .pylion import functions as pl_func


def pylion_dumping():
    """
    Dumps the current positions and velocities of ions to a file.

    This function retrieves the directory for data dumps from the configuration 
    and writes the positions and velocities of ions to a specified text file. 
    It allows for the logging of simulation data at defined intervals, facilitating 
    analysis and debugging.

    Args:
        None: This function does not take any arguments.

    Returns:
        None: This function does not return a value; it performs a file write operation 
        to save the ion data.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """

    dump_dir = configur.get("directory", "dump_dir")
    return pl_func.dump(
        f"{dump_dir}positions.txt",
        variables=[
            "x",
            "y",
            "z",
            "vx",
            "vy",
            "vz",
        ],
        steps=eval(configur.get("sim_parameters", "log_steps")),
    )
