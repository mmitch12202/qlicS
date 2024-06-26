from .config_controller import configur
from .pylion import functions as pl_func


# Spherical Cloud
def pylion_cloud(species):
    return pl_func.createioncloud(
        eval(configur.get("ions", species))[0],
        eval(configur.get("ion_cloud", "radius")),
        eval(configur.get("ion_cloud", "count")),
    )
