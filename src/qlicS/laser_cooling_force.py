import numpy as np

from .config_controller import configur

# TODO CITE where the math here comes from


def get_F_0(k, sat_param, gamma) -> np.float64:
    """
    Calculates the cooling force for laser cooling.

    This function computes the initial cooling force based on the provided 
    wave vector, saturation parameter, and natural linewidth. It uses the 
    constants defined in the configuration to perform the calculation, 
    returning the result as a floating-point number.

    Args:
        k (float): The wave vector associated with the laser.
        sat_param (float): The saturation parameter for the laser.
        gamma (float): The natural linewidth of the transition.

    Returns:
        np.float64: The calculated cooling force.

    Raises:
        KeyError: If the required constants are not found in the configuration.
    """

    num = eval(configur.get("constants", "h")) * k * sat_param * gamma
    den = 2 * np.pi * (1 + sat_param) * 2
    return num / den


# H. Metcalf 3.21
def get_beta(k, s_0, gamma, delta) -> np.float64:
    """
    Calculates the beta parameter for laser cooling.

    This function computes the beta parameter, which is used to describe the 
    effectiveness of laser cooling based on the wave vector, saturation parameter, 
    natural linewidth, and detuning. The calculation utilizes constants defined in 
    the configuration to derive the result, returning it as a floating-point number.

    Args:
        k (float): The wave vector associated with the laser.
        s_0 (float): The saturation parameter for the laser.
        gamma (float): The natural linewidth of the transition.
        delta (float): The detuning of the laser frequency from the atomic transition.

    Returns:
        np.float64: The calculated beta parameter.

    Raises:
        KeyError: If the required constants are not found in the configuration.
    """

    num = -(
        (eval(configur.get("constants", "h")) / (2 * np.pi))
        * (k**2)
        * 4
        * s_0
        * (delta / gamma)
    )
    den = (1 + s_0 + (2 * delta / gamma) ** 2) ** 2
    return num / den


def get_doppler_limit(gamma, delta):
    """
    Calculates the Doppler limit for laser cooling.

    This function computes the Doppler limit, which defines the maximum cooling 
    achievable due to the Doppler effect in laser cooling scenarios. It uses 
    the natural linewidth and detuning to derive the limit, incorporating physical 
    constants defined in the configuration.

    Args:
        gamma (float): The natural linewidth of the transition.
        delta (float): The detuning of the laser frequency from the atomic transition.

    Returns:
        float: The calculated Doppler limit for the cooling process.

    Raises:
        KeyError: If the required constants are not found in the configuration.
    """

    pre_term = hbar = eval(configur.get("constants", "h")) / (2 * np.pi)
    pre_term = (2 * hbar * gamma) / (eval(configur.get("constants", "boltzmann")) * 8)
    plus_term = (2 * abs(delta) / gamma) + (gamma / (2 * abs(delta)))
    return pre_term * plus_term


def create_cooling_laser(
    uid, cycle_info, gid, type_pos
):  # gid is for the species we wish to apply the force to
    """
    Generates the configuration for a cooling laser in the simulation.

    This function constructs the necessary parameters and commands for a cooling 
    laser based on the provided configuration and cycle information. It calculates 
    various properties such as frequency, wave number, and forces, and prepares 
    the commands to apply the cooling effect to the specified target species.

    Args:
        uid (str): A unique identifier for the cooling laser configuration.
        cycle_info (dict): A dictionary containing information about the absorption 
            center and natural linewidth of the target ion.
        gid (int): The group ID for the species to which the cooling force will be applied.
        type_pos (str): The type or position of the cooling laser being configured.

    Returns:
        dict: A dictionary containing the UID, generated commands for the cooling 
        laser, and any additional lines needed for the simulation.

    Raises:
        KeyError: If the required configuration parameters are not found.
    """

    laser_info = {
        key: eval(value)
        for key, value in configur.items(f"cooling_laser_{type_pos}")
        if key not in ["target_ion_type", "target_ion_pos"]
    }
    c = eval(configur.get("constants", "c"))
    # Laser Vars
    frequency = cycle_info["absorption center"] - laser_info["detunning"]
    wave_number = (2 * np.pi) / (c / frequency)
    s = (laser_info["saturation_paramater"]) / (
        1 + ((2 * laser_info["detunning"]) / (cycle_info["natural linewidth"])) ** 2
    )
    # TODO CHECK THE LITTLE AND BIG GAMMAS AND THAT NATURAL LINEWIDTH AND DECAY RATE ARE THE SAME <- I think we are good
    decay_rate = cycle_info["natural linewidth"]
    mag = np.sqrt(sum(vec**2 for vec in laser_info["laser_direction"]))
    normalized_laser_direction = [i / mag for i in laser_info["laser_direction"]]

    F_0 = get_F_0(wave_number, s, decay_rate)
    beta = get_beta(
        wave_number,
        laser_info["saturation_paramater"],
        decay_rate,
        laser_info["detunning"],
    )

    # NOTE: We are assuming low saturation.  For high saturation this heating term is too small
    T_d = get_doppler_limit(cycle_info["natural linewidth"], laser_info["detunning"])
    print(f"F_o 1: {str(F_0)}")
    print(f"beta 1: {str(beta)}")
    print(f"Doppler Limit: {str(T_d)}")
    print(normalized_laser_direction[0])

    h_num = (1 / 2) * laser_info["saturation_paramater"] * decay_rate
    h_den_preterms = 1 + laser_info["saturation_paramater"]
    h_den_sq__den = decay_rate / 2

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
    f_cool = f"fix {uid} {gid} addforce v_coolx v_cooly v_coolz\n\n"
    f_heat_prep = f"variable targetT equal {T_d}\n" f"variable curr_temp equal temp\n"

    # f_heat_add = f"every 1 \"if '${{curr_temp}} < ${{targetT}}' then 'fix hterm {gid} temp/rescale 1 ${{targetT}} ${{targetT}} 0 0' else 'fix hterm {gid} temp/rescale 1 ${{targetT}} ${{targetT}} 0 0'\"\n"  # NOTE some of these values are a bit arbitrary (the doppler correction speed and tolerance), the flipping temperture move rate to 0 is a bit hacky
    f_heat_add = ""  # FIXME this reheating may not be working properly, especially for multi-species systems.  It also slows things a ton.  This should definetly become a toggelable option
    lines = [f_cool_x + f_cool_y + f_cool_z + f_cool + f_heat_prep]
    return {"uid": uid, "code": lines, "additional_lines": f_heat_add}
