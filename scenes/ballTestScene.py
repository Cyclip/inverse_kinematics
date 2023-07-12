from typing import *
import numpy as np
from objects.ball import Ball
from objects.block import Block
from scenes.setter import SceneSetter
import constants as const

class BallTestScene(SceneSetter):
    """
    A physics simulation test with tons of balls
    Does not check for collisions with blocks
    """
    num_balls = 100

    def __init__(self) -> None:
        """
        Create a new scene setter

        Args:
        - sim: The simulation
        """
        super().__init__()
    
    def set_scene(self, sim: Any) -> None:
        """
        Create scenee
        """
        print(f"Creating {BallTestScene.num_balls} balls!!!")
        # Create a bunch of balls
        for _ in range(BallTestScene.num_balls):
            ball = Ball(
                    np.random.uniform(0, const.RESOLUTION[0], 2),
                    np.random.uniform(5, 20),
                    np.random.uniform(1, 10),
                    (
                        np.random.randint(0, 255),
                        np.random.randint(0, 255),
                        np.random.randint(0, 255)
                    )
                )
            
            # Give the ball a random velocity
            ball.vel = np.random.uniform(-100, 100, 2)
            sim.objects.add(ball)
    
        # Create a block
        block = Block(
            (0, const.RESOLUTION[1] - 200),
            (const.RESOLUTION[0] // 2, 100),
            0
        )
        sim.objects.add(block)
    
    def update(self, sim: Any, dt: float) -> None:
        """
        Update the scene

        Args:
        - sim: The simulation
        - dt: Delta time
        """
        pass