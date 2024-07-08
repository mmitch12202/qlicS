import re
from pathlib import Path
from typing import Optional

from prompt_toolkit.validation import ValidationError, Validator


class PathStringValidator(Validator):
    """:class:`~prompt_toolkit.validation.Validator` to validate if input is a valid filepath on the system.

    # A copy of the class from the InquirePy toolkit but with the modification that it can handle string inputs

    Args:
        message: Error message to display in the validatation toolbar when validation failed.
        is_file: Explicitly check if the input is a valid file on the system.
        is_dir: Explicitly check if the input is a valid directory/folder on the system.
    """

    def __init__(
        self,
        message: str = "Input is not a valid path",
        is_file: bool = False,
        is_dir: bool = False,
    ) -> None:
        self._message = message
        self._is_file = is_file
        self._is_dir = is_dir

    def validate(self, document) -> None:

        if document.text[0] in ["'", '"']:
            document.text = document.text[1:-1]

        path = Path(document.text).expanduser()
        if self._is_file and not path.is_file():
            raise ValidationError(
                message=self._message,
                cursor_position=document.cursor_position,
            )
        elif self._is_dir and not path.is_dir():
            raise ValidationError(
                message=self._message,
                cursor_position=document.cursor_position,
            )
        elif not path.exists():
            raise ValidationError(
                message=self._message,
                cursor_position=document.cursor_position,
            )
