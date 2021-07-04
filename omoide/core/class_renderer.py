# -*- coding: utf-8 -*-

"""Object that handles image analyzing and conversion.
"""
import os
from typing import TypedDict, Optional, Callable

from PIL import Image

__all__ = [
    'Renderer',
    'MediaInfo',
]


class MediaInfo(TypedDict):
    """Container for media information."""
    width: int
    height: int
    resolution: float
    size: int
    duration: int
    type: str
    signature: str
    signature_type: str


def analyze_static_image(path: str) -> MediaInfo:
    """Get parameters of a static image (not gif)."""
    image = Image.open(path)
    width, height = image.size
    image.close()

    media_info = {
        'width': width,
        'height': height,
        'resolution': round(width * height / 1_000_000, 2),
        'size': os.path.getsize(path),
        'duration': 0,
        'type': 'image',
        'signature': '',  # TODO
        'signature_type': '',  # TODO
    }

    return media_info


def get_analyze_tool(extension: str) -> Optional[Callable[[str], MediaInfo]]:
    """Return callable that can analyze this kind of files.
    """
    return {
        'jpg': analyze_static_image,
        'jpeg': analyze_static_image,
        'bmp': analyze_static_image,
        'png': analyze_static_image,
    }.get(extension.lower())


class Renderer:
    """Object that handles image analyzing and conversion.
    """

    @staticmethod
    def is_known_media(extension: str) -> bool:
        """Return True if we can handle this file."""
        return get_analyze_tool(extension) is not None

    @staticmethod
    def analyze(path: str, extension: str) -> MediaInfo:
        """Gather media information about the file."""
        tool = get_analyze_tool(extension)

        if tool is None:
            print(f'Unable to analyze this kind of file: {path}')

        info = tool(path)
        return info
