from typing import *
import pygame
import numpy as np

# Base object class
class Object:
    def __init__(self, pos: Tuple[float, float]) -> None:
        """
        Create a new object
        """
        self.pos = np.array(pos, dtype=np.float64)

    def update(self, dt: float) -> None:
        """
        Update the object

        Args:
        - dt: Delta time
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the object on the surface

        Args:
        - surface: The surface to draw on
        """
        pass