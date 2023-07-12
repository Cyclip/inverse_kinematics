from typing import *
import numpy as np
from arm.arm import Arm
from arm.controllers.base import Controller
from scenes.setter import SceneSetter
import constants as const
import pygame

class FollowMouseScene(SceneSetter):
    """
    A test for the arm's rotation mechanics
    """
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
        # Create an arm
        self.arm = Arm(
            np.array([
                const.RESOLUTION[0] // 2,
                const.RESOLUTION[1] // 2
            ]),
            75,
            5,
            (255, 255, 255)
        )

        sim.objects.add(self.arm)
    
    def set_controller(self, controller: Controller) -> None:
        """
        Set the controller
        """
        self.controller = controller
        
    def update(self, sim: Any, dt: float) -> None:
        """
        Update the scene
        """

        # Update the arm
        target = np.array(pygame.mouse.get_pos())
        self.controller.update(self.arm, target)

        # draw target
        pygame.draw.circle(sim.surface, (214, 119, 30), target, 5)
