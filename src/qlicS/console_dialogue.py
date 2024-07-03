from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from .config_controller import get_ions


def followup_questions_creator():
    return {
        "dumping": None,  # TODO, realistically, dumping doesnt belong with these other functions
        "cloud": [
            inquirer.select(
                message="Species",
                choices=get_ions(),
            ),
            inquirer.number(
                message="Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Count",
                min_allowed=0,
                float_allowed=False,
                validate=EmptyInputValidator(),
            ),
        ],
        "trap": [
            inquirer.number(
                message="Target Ion Position (0 for first ion, 1 for second)",
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Length",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Kappa",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Frequency",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Voltage",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Endcapvoltage",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.select(
                message="Pseudo",
                choices=["True", "False"],
            ),
        ],
        "cooling_laser": [
            inquirer.number(
                message="Target Ion Position (0 for first ion, 1 for second)",
                validate=EmptyInputValidator(),
            ),
            inquirer.select(
                message="Species",
                choices=get_ions(),
            ),
            inquirer.number(
                message="Beam Radius",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Saturation Paramater",
                float_allowed=True,
                validate=EmptyInputValidator(),
            ),
            inquirer.number(
                message="Detunning", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.text(
                message="Laser Direction Vector-List, all negative (ex [-0.5, -0.5, -0.71])",
                validate=EmptyInputValidator(),
            ),
            inquirer.text(
                message="Laser Origin Position Vector-List (ex [0, 0, 0])",
                validate=EmptyInputValidator(),
            ),
        ],
        "evolve": None,
        "tickle": [
            inquirer.number(
                message="uid", float_allowed=False, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="amp", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="frequency", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ex0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Exz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ey0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Eyz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ez0", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezx1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezx2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezy1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezy2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezz1", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="Ezz2", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="x_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="y_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.number(
                message="z_shift", float_allowed=True, validate=EmptyInputValidator()
            ),
            inquirer.text(
                message="Static E-field Vector-List (ex [0, 0, 0])",
                validate=EmptyInputValidator(),
            ),
        ],
    }
