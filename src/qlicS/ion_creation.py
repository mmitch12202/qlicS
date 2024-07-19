import numpy as np

from .config_controller import configur
from .pylion import functions as pl_func


# Spherical Cloud
def pylion_cloud(type_pos, uid_override=None):
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
# TODO I am moving away from using this, maybe should remove
def lammps_append_sph_cloud(type_pos, uid):
    positions = []
    species = eval(
        configur.get("ions", configur.get(f"ion_cloud_{type_pos}", "species"))
    )[0]
    number = eval(configur.get(f"ion_cloud_{type_pos}", "count"))
    radius = eval(configur.get(f"ion_cloud_{type_pos}", "radius"))
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
    return {
        "code": lines + species_prep,
        "type": "live ion append",
        "mass": species["mass"],
        "charge": species["charge"],
        "uid": uid,
    }


def recloud_spherical(type_pos):
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
    style = configur.get(f"cloud_reset_{type_pos}", "style")
    if style == "sphere":
        return recloud_spherical(type_pos)
