"""
This file contains all the exceptions for message sdk.
"""


class MessageException(Exception):
    """
    Exception raised whenever there an error occurs in message sdk
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
