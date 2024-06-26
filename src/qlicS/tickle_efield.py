from numpy import pi

from .config_controller import configur
from .time_controller import get_current_dt


def create_tickle():
    frequency = eval(configur.get("modulation", "frequency"))
    uid = eval(configur.get("modulation", "uid"))
    tickleamp = eval(configur.get("modulation", "amp"))
    statics = eval(configur.get("modulation", "static"))
    freq = frequency * get_current_dt()

    # Keep dimensional support?
    f_x = freq
    f_y = freq
    f_z = freq

    e_oscx = (
        f"variable Ex atom ({tickleamp}*"
        f'({eval(configur.get("modulation", "Ex0"))}+'
        f'{eval(configur.get("modulation", "Exx1"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})+'
        f'{eval(configur.get("modulation", "Exx2"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})^2+'
        f'{eval(configur.get("modulation", "Exy1"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})+'
        f'{eval(configur.get("modulation", "Exy2"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})^2+'
        f'{eval(configur.get("modulation", "Exz1"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})+'
        f'{eval(configur.get("modulation", "Exz2"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_x}*step)\n"
    )
    e_oscy = (
        f"variable Ey atom ({tickleamp}*"
        f'({eval(configur.get("modulation", "Ey0"))}+'
        f'{eval(configur.get("modulation", "Eyx1"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})+'
        f'{eval(configur.get("modulation", "Eyx2"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})^2+'
        f'{eval(configur.get("modulation", "Eyy1"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})+'
        f'{eval(configur.get("modulation", "Eyy2"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})^2+'
        f'{eval(configur.get("modulation", "Eyz1"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})+'
        f'{eval(configur.get("modulation", "Eyz2"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_y}*step)\n"
    )
    e_oscz = (
        f"variable Ez atom ({tickleamp}*"
        f'({eval(configur.get("modulation", "Ez0"))}+'
        f'{eval(configur.get("modulation", "Ezx1"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})+'
        f'{eval(configur.get("modulation", "Ezx2"))}*'
        f'(x-{eval(configur.get("modulation", "x_shift"))})^2+'
        f'{eval(configur.get("modulation", "Ezy1"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})+'
        f'{eval(configur.get("modulation", "Ezy2"))}*'
        f'(y-{eval(configur.get("modulation", "y_shift"))})^2+'
        f'{eval(configur.get("modulation", "Ezz1"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})+'
        f'{eval(configur.get("modulation", "Ezz2"))}*'
        f'(z-{eval(configur.get("modulation", "z_shift"))})^2))*'
        f"cos((2*{pi})*{f_z}*step)\n"
    )

    e_field = f"fix {uid} all efield v_Ex v_Ey v_Ez"

    # Static field support

    e_magx = f"variable E equal {statics[0]}\n"
    e_magy = f"variable B equal {statics[1]}\n"
    e_magz = f"variable C equal {statics[2]}\n"

    lines = [e_magx + e_oscx + e_magy + e_oscy + e_magz + e_oscz + e_field]
    field = {"uid": uid, "code": lines}
    return field
