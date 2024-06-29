# For all analysis related tasks, including simply reading the dump file
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
