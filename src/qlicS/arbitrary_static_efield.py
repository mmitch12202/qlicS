from numpy import pi

from .config_controller import configur
# TODO make tests of this
def create_static_field(type_pos, uid):
    """Generates the configuration for a static electric field in the simulation.

    This function constructs the necessary parameters and commands for a static 
    electric field based on the provided configuration and type position. It calculates 
    the electric field components and prepares the commands to apply the static 
    field effect to the specified region in the simulation.

    Args:
        type_pos (str): The type or position of the static electric field being configured.
        uid (str): A unique identifier for the static field configuration.

    Returns:
        dict: A dictionary containing the UID and generated commands for the static 
        electric field.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """
    # uid = eval(configur.get(f"static_efield_{type_pos}", "uid"))
    amp_coeff = eval(configur.get(f"static_efield_{type_pos}", "amp"))

    x_bound = eval(configur.get(f"static_efield_{type_pos}", "x_bound"))
    y_bound = eval(configur.get(f"static_efield_{type_pos}", "y_bound"))
    z_bound = eval(configur.get(f"static_efield_{type_pos}", "z_bound"))

    # TODO maybe an option for all space
    bound = (
        f"region {uid}r block {x_bound[0]} {x_bound[1]} {y_bound[0]} {y_bound[1]} {z_bound[0]} {z_bound[1]}\n"
    )

    e_oscx = (
        f"variable sEx atom ({amp_coeff}*"
        f'({eval(configur.get(f"static_efield_{type_pos}", "Ex0"))}+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exx1"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exx2"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exy1"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exy2"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exz1"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Exz2"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})^2))\n'
    )
    e_oscy = (
        f"variable sEy atom ({amp_coeff}*"
        f'({eval(configur.get(f"static_efield_{type_pos}", "Ey0"))}+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyx1"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyx2"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyy1"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyy2"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyz1"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Eyz2"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})^2))\n'
    )
    e_oscz = (
        f"variable sEz atom ({amp_coeff}*"
        f'({eval(configur.get(f"static_efield_{type_pos}", "Ez0"))}+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezx1"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezx2"))}*'
        f'(x-{eval(configur.get(f"static_efield_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezy1"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezy2"))}*'
        f'(y-{eval(configur.get(f"static_efield_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezz1"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"static_efield_{type_pos}", "Ezz2"))}*'
        f'(z-{eval(configur.get(f"static_efield_{type_pos}", "z_shift"))})^2))\n'
    )

    e_field = f"fix {uid} all efield v_sEx v_sEy v_sEz region {uid}r"

    lines = [bound + e_oscx + e_oscy + e_oscz + e_field]
    return {"uid": uid, "code": lines}
