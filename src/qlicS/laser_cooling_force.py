import numpy as np

from .config_controller import configur

# TODO CITE where the math here comes from


def get_F_0(k, sat_param, gamma) -> np.float64:
    num = eval(configur.get("constants", "h")) * k * sat_param * gamma
    den = 2 * np.pi * (1 + sat_param) * 2
    return num / den

# H. Metcalf 3.21
def get_beta(k, s_0, gamma, delta) -> np.float64:
    num = -(
        (eval(configur.get("constants", "h")) / (2 * np.pi))
        * (k**2)
        * 4 * s_0
        * (delta/gamma)
    )
    den = (1 + s_0 + (2*delta / gamma)**2) **2
    return num / den

def create_cooling_laser(
    uid, cycle_info, gid, type_pos
):  # gid is for the species we wish to apply the force to
    laser_info = {
        key: eval(value)
        for key, value in configur.items(f"cooling_laser_{type_pos}")
        if key not in ["target_ion_type", "target_ion_pos"]
    }
    # Laser Vars
    frequency = cycle_info["absorption center"] - laser_info["detunning"]
    wave_number = (2 * np.pi) / (eval(configur.get("constants", "c")) / frequency)
    s = (laser_info["saturation_paramater"]) / (
        1 + ((2 * laser_info["detunning"]) / (cycle_info["natural linewidth"])) ** 2
    )
    # TODO CHECK THE LITTLE AND BIG GAMMAS AND THAT NATURAL LINEWIDTH AND DECAY RATE ARE THE SAME
    decay_rate = cycle_info["natural linewidth"]
    mag = np.sqrt(sum(vec**2 for vec in laser_info["laser_direction"]))
    normalized_laser_direction = [i / mag for i in laser_info["laser_direction"]]

    F_0 = get_F_0(wave_number, s, decay_rate)
    beta = get_beta(wave_number, laser_info["saturation_paramater"], decay_rate, laser_info["detunning"])
    print(f"F_o 1:{str(F_0)}")
    print(f"beta 1: {str(beta)}")
    print(normalized_laser_direction[0])

    # TODO: figure out either if we will switch between or just use one of these
    # likely the other will become our check

    # if linear_lasercool_method:
    f_cool_x = (
        f"variable coolx atom ({F_0}-{beta}*vx)*{normalized_laser_direction[0]}\n"
    )
    f_cool_y = (
        f"variable cooly atom ({F_0}-{beta}*vy)*{normalized_laser_direction[1]}\n"
    )
    f_cool_z = (
        f"variable coolz atom ({F_0}-{beta}*vz)*{normalized_laser_direction[2]}\n"
    )
    # TODO switch all to only affect the species we want
    f_cool = f"fix {uid} {gid} addforce v_coolx v_cooly v_coolz"
    lines = [f_cool_x + f_cool_y + f_cool_z + f_cool]
    return {"uid": uid, "code": lines}
