from __future__ import annotations
from typing import *
import pygame
import constants as const
import numpy as np

from objects.obj import Object

"""
The Block class is a simple object that can be moved by the user or arm.
It does not collide with other blocks for simplicity, nor does it have any
physics properties (i.e. gravity, friction, etc.)

Methods:
- __init__(
    self,
    pos: Tuple[float, float],
    size: Tuple[float, float],
    color: Tuple[int, int, int],
    mass: float = 1,
    restitution: float = 0.4,
    friction: float = 0.1
) -> None
- update(self, dt: float) -> None
- draw(self, surface: pygame.Surface) -> None
"""

class Block(Object):
    def __init__(
        self,
        pos: Tuple[float, float],
        size: Tuple[float, float],
        color: Tuple[int, int, int],
        mass: float = 1,
        restitution: float = 0.8,
        friction: float = 0.1
    ) -> None:
        """
        Create a new block
        """
        super().__init__(pos)
        self.pos = np.array(pos, dtype=np.float64)
        self.size = np.array(size, dtype=np.float64)
        self.color = color
        self.mass = mass
        self.restitution = restitution
        self.friction = friction
    
    def update(self, dt: float) -> None:
        """
        Update the block

        Args:
        - dt: Delta time
        """
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the block

        Args:
        - surface: The surface to draw on
        """
        # Draw an outline
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (
                self.pos[0] - self.size[0] // 2,
                self.pos[1] - self.size[1] // 2,
                self.size[0],
                self.size[1]
            ),
            1
        )