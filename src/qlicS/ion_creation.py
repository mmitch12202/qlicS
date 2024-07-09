from .config_controller import configur
from .pylion import functions as pl_func


# Spherical Cloud
def pylion_cloud(type_pos):
    c = pl_func.createioncloud(
        eval(configur.get("ions", configur.get(f"ion_cloud_{type_pos}", "species")))[0],
        eval(configur.get(f"ion_cloud_{type_pos}", "radius")),
        eval(configur.get(f"ion_cloud_{type_pos}", "count")),
    )
    c['uid'] = eval(configur.get(f"ion_cloud_{type_pos}", "uid"))
    return c
