from __future__ import annotations
from typing import *
import pygame
import constants as const
import numpy as np

from objects.obj import Object

"""
This module contains the Ball class.
A ball is a simple object that is affected by gravity,
can collide with other balls, and can be moved by the user or arm.

Methods:
- __init__(self, pos: Tuple[float, float], radius: float, mass: float, color: Tuple[int, int, int]) -> None
- update(self, dt: float) -> None
- draw(self, surface: pygame.Surface) -> None
- apply_force(self, force: np.ndarray) -> None
- apply_impulse(self, impulse: np.ndarray) -> None
- apply_gravity(self) -> None
- apply_friction(self) -> None
- apply_drag(self) -> None
- apply_collision(self, other: Ball) -> None
- apply_wall_collision(self) -> None
"""

class Ball(Object):
    def __init__(self, pos: Tuple[float, float], radius: float, mass: float, color: Tuple[int, int, int]) -> None:
        """
        Create a new ball
        """
        super().__init__(pos)
        self.pos = np.array(pos, dtype=np.float64)
        self.vel = np.zeros(2, dtype=np.float64)
        self.acc = np.zeros(2, dtype=np.float64)
        self.radius = radius
        self.mass = mass
        self.color = color
    
    def update(self, dt: float) -> None:
        """
        Update the ball

        Args:
        - dt: Delta time
        """
        self.apply_gravity()
        self.apply_friction()
        # self.apply_drag()
        self.apply_wall_collision()
        self.pos += self.vel * dt
        self.vel += self.acc * dt
        self.acc = np.zeros(2, dtype=np.float64)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the ball on the surface

        Args:
        - surface: The surface to draw on
        """
        pygame.draw.circle(surface, self.color, self.pos.astype(int), self.radius)
    
    def apply_force(self, force: np.ndarray) -> None:
        """
        Apply a force to the ball

        Args:
        - force: The force to apply
        """
        self.acc += force / self.mass

    def apply_impulse(self, impulse: np.ndarray) -> None:
        """
        Apply an impulse to the ball
        An impulse is a force applied over a single frame:
            Δp = F * Δt

        Args:
        - impulse: The impulse to apply
        """
        self.vel += impulse / self.mass

    def apply_gravity(self) -> None:
        """
        Apply gravity to the ball:
            F = m * g
        """
        self.apply_force(np.array([0, const.GRAVITY]) * self.mass)

    def apply_friction(self) -> None:
        """
        Apply friction to the ball:
            F = -μ * v
        """
        self.apply_force(-self.vel * const.DRAG_FRICTION_MULTIPLIER)

    def apply_collision(self, other: Ball) -> None:
        """
        Apply a collision to the ball

        Args:
        - other: The other ball
        """
        raise NotImplementedError

    def apply_wall_collision(self) -> None:
        """
        Apply a collision with the walls to the ball
        """
        # Check if the ball is colliding with the walls
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.vel[0] *= -const.RESTITUTION
        elif self.pos[0] + self.radius > const.RESOLUTION[0]:
            self.pos[0] = const.RESOLUTION[0] - self.radius
            self.vel[0] *= -const.RESTITUTION
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -const.RESTITUTION
        elif self.pos[1] + self.radius > const.RESOLUTION[1]:
            self.pos[1] = const.RESOLUTION[1] - self.radius
            self.vel[1] *= -const.RESTITUTION