# -*- coding: utf-8 -*-

"""Abstraction of printing.
"""
from colorama import init, Fore

init(autoreset=True)

__all__ = [
    'STDOut',
]


class STDOut:
    """Abstraction of printing.
    """

    @classmethod
    def print(cls, text: str, *args, **kwargs) -> None:
        """Print green."""
        return cls.prefix_print('', text, *args, **kwargs)

    @classmethod
    def green(cls, text: str, *args, **kwargs) -> None:
        """Print green."""
        return cls.prefix_print(Fore.GREEN, text, *args, **kwargs)

    @classmethod
    def yellow(cls, text: str, *args, **kwargs) -> None:
        """Print yellow."""
        return cls.prefix_print(Fore.YELLOW, text, *args, **kwargs)

    @classmethod
    def red(cls, text: str, *args, **kwargs) -> None:
        """Print red."""
        return cls.prefix_print(Fore.RED, text, *args, **kwargs)

    @classmethod
    def gray(cls, text: str, *args, **kwargs) -> None:
        """Print gray."""
        return cls.prefix_print(Fore.LIGHTBLACK_EX, text, *args, **kwargs)

    @classmethod
    def magenta(cls, text: str, *args, **kwargs) -> None:
        """Print magenta."""
        return cls.prefix_print(Fore.MAGENTA, text, *args, **kwargs)

    @classmethod
    def cyan(cls, text: str, *args, **kwargs) -> None:
        """Print cyan."""
        return cls.prefix_print(Fore.CYAN, text, *args, **kwargs)

    @classmethod
    def prefix_print(cls, prefix: str, text: str, *args, **kwargs) -> None:
        """Print with prefix (usually color)."""
        return print(prefix + text, *args, **kwargs)