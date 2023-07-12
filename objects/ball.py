from __future__ import annotations
from typing import *
import pygame
import constants as const
import numpy as np

from objects.obj import Object
from objects.block import Block
from arm.arm import Arm

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
        
        # If the ball is being held
        self.held = False
        # The arm that is holding the ball
        self.holder = None
    
    def set_held(self, held: bool, holder: Optional[Arm] = None) -> None:
        """
        Set if the ball is being held

        Args:
        - held: If the ball is being held
        - holder: The arm that is holding the ball
        """
        self.held = held
        self.holder = holder
    
    def update(self, dt: float, others: Set[Ball]) -> None:
        """
        Update the ball

        Args:
        - dt: Delta time
        - others: The other balls to check collisions with
        """
        # If the ball is being held, update its position
        if self.held:
            self.pos = self.holder.get_end_effector_pos()
            return

        self.apply_gravity()
        self.apply_friction()

        # Check for collisions
        for other in others:
            if other != self:
                self.apply_collision(other)

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
        # If its a Block, apply a collision with the block
        if isinstance(other, Block):
            return self.apply_block_collision(other)

        # Check if the balls are colliding
        dist = np.linalg.norm(self.pos - other.pos)

        if dist < self.radius + other.radius:
            # Calculate the impulse
            n = (self.pos - other.pos) / dist
            v = self.vel - other.vel
            j = -(1 + const.WALL_RESTITUTION) * np.dot(v, n) / (1 / self.mass + 1 / other.mass)

            # Apply the impulse
            self.apply_impulse(j * n)
            other.apply_impulse(-j * n)

            # Move the balls so they don't overlap
            overlap = (self.radius + other.radius) - dist
            self.pos += n * overlap * 0.75
            other.pos -= n * overlap * 0.75

            # Apply friction
            self.apply_force(-self.vel * const.FRICTION_MULTIPLIER)
            other.apply_force(-other.vel * const.FRICTION_MULTIPLIER)
    
    def apply_block_collision(self, block: Block) -> None:
        """
        Apply a collision with a block to the ball

        Args:
        - block: The block to collide with
        """
        nearest = np.clip(self.pos, block.pos, block.pos + block.size)

        dist = np.linalg.norm(self.pos - nearest)

        if dist <= self.radius:
            overlap = self.radius - dist
            
            if (self.pos[0] < block.pos[0] or self.pos[0] > block.pos[0] + block.size[0]) and (self.pos[1] < block.pos[1] or self.pos[1] > block.pos[1] + block.size[1]):
                self.pos += (self.pos - nearest) / dist * overlap
                return
            
            # dont divide by 0
            if dist == 0:
                dist = 1
            if overlap == 0:
                overlap = 1

            # move the ball so it doesn't overlap
            self.pos += (self.pos - nearest) / dist * overlap

            # calculate the impulse
            # we do this by calculating the velocity of the ball
            # at the point of collision
            # then we calculate the impulse using the velocity
            # and the normal of the collision
            v = self.vel
            n = (self.pos - nearest) / dist
            j = -(block.restitution) * np.dot(v, n) / (1 / self.mass + 1 / block.mass)

            # apply the impulse
            self.apply_impulse(j * n)


    def apply_wall_collision(self) -> None:
        """
        Apply a collision with the walls to the ball
        """
        # Check if the ball is colliding with the walls
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.vel[0] *= -const.WALL_RESTITUTION
        elif self.pos[0] + self.radius > const.RESOLUTION[0]:
            self.pos[0] = const.RESOLUTION[0] - self.radius
            self.vel[0] *= -const.WALL_RESTITUTION
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -const.WALL_RESTITUTION
        elif self.pos[1] + self.radius > const.RESOLUTION[1]:
            self.pos[1] = const.RESOLUTION[1] - self.radius
            self.vel[1] *= -const.WALL_RESTITUTION