from typing import *
import pygame

pygame.font.init()

# Gravitational constant
GRAVITY: float = 9.8

# Sim resolution
RESOLUTION: Tuple[int, int] = (1200, 700)
# Ease of use
SCREEN_WIDTH: int = RESOLUTION[0]
SCREEN_HEIGHT: int = RESOLUTION[1]

# Force multiplier
FORCE_MULTIPLIER: float = 10

# Air friction multiplier
DRAG_FRICTION_MULTIPLIER: float = 0.05

# Friction multiplier (when colliding with another ball or a wall)
FRICTION_MULTIPLIER: float = 0.1

# Restitution
WALL_RESTITUTION: float = 0.4

# Grid size
GRID_SIZE: int = 50

# Arm width
ARM_WIDTH: int = 10

# Font
FONT: pygame.font.Font = pygame.font.SysFont("Arial", 20)

# Arm end radius
ARM_END_RADIUS: int = 13