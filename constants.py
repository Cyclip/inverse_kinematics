from typing import *

# Gravitational constant
GRAVITY: float = 9.8

# Sim resolution
RESOLUTION: Tuple[int, int] = (1200, 700)

# Force multiplier
FORCE_MULTIPLIER: float = 10

# Air friction multiplier
DRAG_FRICTION_MULTIPLIER: float = 0.05

# Friction multiplier (when colliding with another ball or a wall)
FRICTION_MULTIPLIER: float = 0.1

# Restitution
WALL_RESTITUTION: float = 0.4

# Grid size
GRID_SIZE: int = 100