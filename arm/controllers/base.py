from typing import *

class Controller:
    """
    Base controller class
    """
    def __init__(self, alpha: float = 0.001) -> None:
        pass
    
    def update(self, arm: Any, dt: float) -> None:
        pass