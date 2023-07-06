from typing import *
from scenes.setter import SceneSetter

class EmptyScene(SceneSetter):
    """
    An empty scene
    """
    def __init__(self) -> None:
        """
        Create a new scene setter

        Args:
        - sim: The simulation
        """
        super().__init__()
    
    def set_scene(self, _: Any) -> None:
        """Nothing here, its empty!"""
        pass