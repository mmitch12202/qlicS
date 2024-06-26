# For all analysis related tasks, including simply reading the dump file
from .config_controller import configur
from .pylion import functions as pl_func


# As of now, all atoms, all time.  This could be changed and may make sense too TODO
def velocities():
    dump_dir = configur.get("directory", "dump_dir")
    _, data = pl_func.readdump(dump_dir + "positions.txt")
    return dict(
        zip(_, data[:, :, 3:6])
    )  # TODO code fixing here currently hardcoding velocity indices data[0, :, 3:6]
