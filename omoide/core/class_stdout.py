# -*- coding: utf-8 -*-

"""Special class that handles printing.
"""
from colorama import init, Fore

init(autoreset=True)

__all__ = [
    'STDOut',
]


class STDOut:
    """Special class that handles printing.
    """

    @classmethod
    def print(cls, text: str, *args, **kwargs) -> None:
        """Print green."""
        return print(text, *args, **kwargs)

    @classmethod
    def green(cls, text: str, *args, **kwargs) -> None:
        """Print green."""
        return print(Fore.GREEN + text, *args, **kwargs)

    @classmethod
    def yellow(cls, text: str, *args, **kwargs) -> None:
        """Print yellow."""
        return print(Fore.YELLOW + text, *args, **kwargs)

    @classmethod
    def red(cls, text: str, *args, **kwargs) -> None:
        """Print red."""
        return print(Fore.RED + text, *args, **kwargs)
