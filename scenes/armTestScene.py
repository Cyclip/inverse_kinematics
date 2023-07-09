from typing import *
import numpy as np
from arm.arm import Arm
from scenes.setter import SceneSetter
import constants as const

class ArmTestScene(SceneSetter):
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
        arm = Arm(
            np.array([const.RESOLUTION[0] / 2, const.RESOLUTION[1] / 2]),
            70,
            4,
            (255, 255, 255)
        )

        sim.objects.add(arm)