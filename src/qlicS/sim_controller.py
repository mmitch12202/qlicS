from .config_controller import configur
from .pylion import functions as pl_func


def pylion_dumping():
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
