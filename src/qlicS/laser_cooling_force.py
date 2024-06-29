import numpy as np

from .config_controller import configur

# TODO CITE where the math here comes from


def get_F_0(k, sat_param, gamma) -> np.float64:
    num = eval(configur.get("constants", "h")) * k * sat_param * gamma
    den = 2 * np.pi * (1 + sat_param) * 2
    return num / den


def get_beta(k, sat_param, gamma, delta) -> np.float64:
    num = (
        -(eval(configur.get("constants", "h")) / (2 * np.pi))
        * (k**2)
        * sat_param
        * delta
        * gamma
    )
    den = (1 + sat_param) ** 2 * (delta**2 + gamma**2 / 4)
    return num / den


def create_cooling_laser(
    cycle_info, gid
):  # gid is for the species we wish to apply the force to
    laser_info = {i[0]: eval(i[1]) for i in configur.items("cooling_laser")}
    # Laser Vars
    frequency = cycle_info["absorption center"] - laser_info["detunning"]
    wave_number = (2 * np.pi) / (eval(configur.get("constants", "c")) / frequency)
    intensity = cycle_info["saturation"] * laser_info["saturation_paramater"]
    s = (intensity / cycle_info["saturation"]) / (
        1 + ((2 * laser_info["detunning"]) / (cycle_info["natural linewidth"])) ** 2
    )
    # TODO CHECK THE LITTLE AND BIG GAMMAS AND THAT NATURAL LINEWIDTH AND DECAY RATE ARE THE SAME
    decay_rate = cycle_info["natural linewidth"]
    mag = np.sqrt(sum(vec**2 for vec in laser_info["laser_direction"]))
    normalized_laser_direction = [i / mag for i in laser_info["laser_direction"]]
    # id stuff
    uid = 569202603907002  # TODO: work out this explicit id stuff

    F_0 = get_F_0(wave_number, s, decay_rate)
    beta = get_beta(wave_number, s, decay_rate, laser_info["detunning"])
    print(f"F_o 1:{str(F_0)}")
    print(f"beta 1: {str(beta)}")
    print(normalized_laser_direction[0])

    # TODO: figure out either if we will switch between or just use one of these
    # likely the other will become our check

    # if linear_lasercool_method:
    f_cool_x = (
        f"variable coolx atom ({F_0}+({beta}*vx))*{normalized_laser_direction[0]}\n"
    )
    f_cool_y = (
        f"variable cooly atom ({F_0}+{beta}*vy)*{normalized_laser_direction[1]}\n"
    )
    f_cool_z = (
        f"variable coolz atom ({F_0}+{beta}*vz)*{normalized_laser_direction[2]}\n"
    )
    # TODO switch all to only affect the species we want
    f_cool = f"fix {uid} {gid} addforce v_coolx v_cooly v_coolz"
    lines = [f_cool_x + f_cool_y + f_cool_z + f_cool]
    return {"uid": uid, "code": lines}


# TODO Deleat this when no longer needed
def create_cooling_laser_old(
    cycle_info, gid
):  # gid is for the species we wish to apply the force to
    laser_info = {}
    for i in configur.items("cooling_laser"):
        laser_info[i[0]] = eval(i[1])

    # Transition and Laser - dependent values
    frequency = (
        cycle_info["absorption center"] - laser_info["detunning"]
    )  # Assuming red detunning
    intensity = cycle_info["saturation"] * laser_info["saturation_paramater"]
    mag = np.sqrt(sum(vec**2 for vec in laser_info["laser_direction"]))
    normalized_laser_direction = [i / mag for i in laser_info["laser_direction"]]
    # TODO smaller scattering beam then crystal size
    """ beam_area = np.pi * (laser_info["beam_radius"] ** 2)
    e_ph = eval(configur.get("constants", "h")) * frequency
    p_ph = eval(configur.get("constants", "h")) * (
        eval(configur.get("constants", "c")) / frequency
    ) """
    s = (intensity / cycle_info["saturation"]) / (
        1 + ((2 * laser_info["detunning"]) / (cycle_info["natural linewidth"])) ** 2
    )

    # find laser's centerline (line from origin position in direction of laser_direction)
    def laser_centerline(t):
        return [
            laser_info["laser_origin_position"][dim]
            + t * normalized_laser_direction[dim]
            for dim in range(3)
        ]

    # for determining if atom is in laser beam, defunct for now
    """ def shortest_distance_to_centerline(atom_pos, centerline):
        point_1 = centerline(0)
        point_2 = centerline(4)
        # 4 is arbitrarily large so that the closest point on the line is between
        # the two selected points:
        # https://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
        def vector_subtraction_3d(first, second):
            return [first[q]-second[q] for q in range(3)]
        numerator = abs(np.cross(vector_subtraction_3d(atom_pos,point_1),
        vector_subtraction_3d(atom_pos, point_2)))
        numerator_mag = sqrt(sum(num_val**2 for num_val in numerator))
        denominator = sqrt(sum(
        [(point_2[l]-point_1[l])**2 for l in range(len(point_2))]
        ))
        return numerator_mag/denominator """

    # id stuff
    uid = 569202603907002  # TODO: work out this explicit id stuff
    # rewriting the cool functions:

    detAng = laser_info["detunning"] * 2 * np.pi
    wave_number = (2 * np.pi) / (
        eval(configur.get("constants", "c")) / frequency
    )  # not sure if there should be an extra factor of 2pi here, but fits better wout.
    numerator = (
        -(eval(configur.get("constants", "h")) / (2 * np.pi))
        * (wave_number**2)
        * 4
        * laser_info["saturation_paramater"]
        * (-detAng / cycle_info["natural linewidth"])
    )
    denominator = (
        1
        + laser_info["saturation_paramater"]
        + ((-2 * detAng) / cycle_info["natural linewidth"]) ** 2
    ) ** 2
    beta = numerator / denominator

    s = laser_info["saturation_paramater"] / (
        1 + (2 * laser_info["detunning"] / cycle_info["natural linewidth"])
    )
    F_o = (
        (eval(configur.get("constants", "h")) / (2 * np.pi))
        * wave_number
        * s
        * (cycle_info["natural linewidth"] / 2)
        / (1 + s)
    )
    # F_o = 0
    print("F_o 1:" + str(F_o))
    print("beta 1: " + str(beta))
    print(normalized_laser_direction[0])

    # TODO: figure out either if we will switch between or just use one of these
    # likely the other will become our check

    # if linear_lasercool_method:
    f_cool_x = (
        f"variable coolx atom ({F_o}+({beta}*vx))*{normalized_laser_direction[0]}\n"
    )
    f_cool_y = (
        f"variable cooly atom ({F_o}+{beta}*vy)*{normalized_laser_direction[1]}\n"
    )
    f_cool_z = (
        f"variable coolz atom ({F_o}+{beta}*vz)*{normalized_laser_direction[2]}\n"
    )
    # else:
    #    f_cool_x = f'variable coolx atom ({h}*{frequency}* \
    #    (((1+(vx/{speed_of_light}))/(1-(vx/{speed_of_light})))^(1/2))/ \
    #    {speed_of_light})*({s}*{ions_info[1][1]["natural linewidth"]}/2)/ \
    #    (1+{s}+(({ions_info[1][1]["absorption center"]}-{frequency}* \
    #    (((1+(vx/{speed_of_light}))/(1-(vx/{speed_of_light})))^(1/2)))/ \
    #    ({ions_info[1][1]["natural linewidth"]}/{4*np.pi}))^(2))* \
    #    {normalized_laser_direction[0]}\n'
    #    f_cool_y = f'variable cooly atom ({h}*{frequency}* \
    #    (((1+(vy/{speed_of_light}))/(1-(vy/{speed_of_light})))^(1/2))/ \
    #    {speed_of_light})*({s}*{ions_info[1][1]["natural linewidth"]}/2)/ \
    #    (1+{s}+(({ions_info[1][1]["absorption center"]}-{frequency}* \
    #    (((1+(vy/{speed_of_light}))/(1-(vy/{speed_of_light})))^(1/2)))/ \
    #    ({ions_info[1][1]["natural linewidth"]}/{4*np.pi}))^(2))* \
    #    {normalized_laser_direction[1]}\n'
    #    f_cool_z = f'variable coolz atom ({h}*{frequency}* \
    #    (((1+(vx/{speed_of_light}))/(1-(vx/{speed_of_light})))^(1/2))/ \
    #    {speed_of_light})*({s}*{ions_info[1][1]["natural linewidth"]}/2)/ \
    #    (1+{s}+(({ions_info[1][1]["absorption center"]}-{frequency}* \
    #    (((1+(vx/{speed_of_light}))/(1-(vx/{speed_of_light})))^(1/2)))/ \
    #    ({ions_info[1][1]["natural linewidth"]}/{4*np.pi}))^(2))* \
    #    {normalized_laser_direction[2]}\n'

    f_cool = f"fix {uid} {gid} addforce v_coolx v_cooly v_coolz"
    lines = [f_cool_x + f_cool_y + f_cool_z + f_cool]
    field = {"uid": uid, "code": lines}
    return field
