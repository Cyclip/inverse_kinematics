from typing import *

from arm.controllers.base import Controller

class SceneSetter:
    """
    Base class for scene setters
    """
    def __init__(self) -> None:
        """
        Create a new scene setter

        Args:
        - sim: The simulation
        """
        print(
            f"Loading scene: {self.__class__.__name__}"
        )
    
    def set_scene(self, _: Any) -> None:
        """
        Set the scene
        """
        raise NotImplementedError

    def set_controller(self, controller: Controller) -> None:
        """
        Set the controller
        """
        self.controller = controller
    
    def update(self, sim: Any, dt: float) -> None:
        """
        Update the scene
        """
        raise NotImplementedError