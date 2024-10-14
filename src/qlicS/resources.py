import re
from pathlib import Path
from typing import Optional

from prompt_toolkit.validation import ValidationError, Validator


class PathStringValidator(Validator):
    """
    Validator to check if input is a valid file or directory path.

    This class extends the `Validator` from the `prompt_toolkit` to provide 
    functionality for validating file and directory paths. It can be configured 
    to check whether the input corresponds to an existing file or directory, 
    and it provides an error message when validation fails.

    Args:
        message (str, optional): The error message to display when validation fails. 
            Defaults to "Input is not a valid path".
        is_file (bool, optional): If set to True, the validator checks if the input 
            is a valid file path. Defaults to False.
        is_dir (bool, optional): If set to True, the validator checks if the input 
            is a valid directory path. Defaults to False.

    Raises:
        ValidationError: If the input does not meet the specified validation criteria.
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
        """Validates the input document to check if it corresponds to a valid file or directory path.

        This method processes the text from the input document, removing any surrounding 
        quotes, and checks if the resulting path is a valid file or directory based on 
        the configuration settings. If the validation fails, it raises a `ValidationError` 
        with an appropriate error message.

        Args:
            document (Document): The input document containing the text to be validated.

        Returns:
            None: This function does not return a value; it raises an exception if validation fails.

        Raises:
            ValidationError: If the input path is not a valid file or directory.
        """


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
