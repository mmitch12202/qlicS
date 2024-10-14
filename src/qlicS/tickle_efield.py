from numpy import pi

from .config_controller import configur
from .time_controller import get_current_dt


def create_tickle(type_pos, uid):
    """
    Generates the configuration for a tickle electric field in the simulation.

    This function constructs the necessary parameters and commands for a tickle 
    electric field based on the provided configuration and type position. It calculates 
    the oscillating electric field components and prepares the commands to apply the 
    tickle effect to the specified ions in the simulation.

    Args:
        type_pos (str): The type or position of the tickle electric field being configured.
        uid (str): A unique identifier for the tickle configuration.

    Returns:
        dict: A dictionary containing the UID and generated commands for the tickle 
        electric field.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """

    frequency = eval(configur.get(f"modulation_{type_pos}", "frequency"))
    # uid = eval(configur.get(f"modulation_{type_pos}", "uid"))
    tickleamp = eval(configur.get(f"modulation_{type_pos}", "amp"))
    statics = eval(configur.get(f"modulation_{type_pos}", "static"))
    freq = frequency * get_current_dt()

    # Keep dimensional support? TODO
    f_x = freq
    f_y = freq
    f_z = freq

    e_oscx = (
        f"variable Ex atom ({tickleamp}*"
        f'({eval(configur.get(f"modulation_{type_pos}", "Ex0"))}+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exx1"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exx2"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exy1"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exy2"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exz1"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Exz2"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_x}*step)\n"
    )
    e_oscy = (
        f"variable Ey atom ({tickleamp}*"
        f'({eval(configur.get(f"modulation_{type_pos}", "Ey0"))}+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyx1"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyx2"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyy1"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyy2"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyz1"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Eyz2"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_y}*step)\n"
    )
    e_oscz = (
        f"variable Ez atom ({tickleamp}*"
        f'({eval(configur.get(f"modulation_{type_pos}", "Ez0"))}+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezx1"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezx2"))}*'
        f'(x-{eval(configur.get(f"modulation_{type_pos}", "x_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezy1"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezy2"))}*'
        f'(y-{eval(configur.get(f"modulation_{type_pos}", "y_shift"))})^2+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezz1"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})+'
        f'{eval(configur.get(f"modulation_{type_pos}", "Ezz2"))}*'
        f'(z-{eval(configur.get(f"modulation_{type_pos}", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_z}*step)\n"
    )

    e_field = f"fix {uid} all efield v_Ex v_Ey v_Ez"

    # Uniform field support TODO using statics is confusing because its really 'uniform'

    e_magx = f"variable E equal {statics[0]}\n"
    e_magy = f"variable B equal {statics[1]}\n"
    e_magz = f"variable C equal {statics[2]}\n"

    lines = [e_magx + e_oscx + e_magy + e_oscy + e_magz + e_oscz + e_field]
    return {"uid": uid, "code": lines}
