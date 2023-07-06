from typing import *
from objects.obj import Object
import pygame
import constants as const

"""
This module contains the ObjectManager class
which is responsible for managing all the objects in the simulation
"""

class ObjectManager:
    def __init__(self) -> None:
        """
        Create a new object manager
        """
        self.objects = set()
        self.hashmap = self.__create_hashmap()
        self.surface = None
    
    def __create_hashmap(self) -> Dict[Tuple[int, int], Set[Object]]:
        """
        Create the spatial partitioning hashmap

        Returns:
        - The hashmap
        """
        hashmap = {}
        
        # Create the grid
        for i in range(const.RESOLUTION[0] // const.GRID_SIZE):
            for j in range(const.RESOLUTION[1] // const.GRID_SIZE):
                hashmap[(i, j)] = set()

        return hashmap

    def __pos_to_grid(self, pos: Tuple[float, float]) -> Tuple[int, int]:
        """
        Convert a position to a grid position within the hashmap

        Args:
        - pos: The position

        Returns:
        - The grid position
        """
        x = int(pos[0] // const.GRID_SIZE)
        y = int(pos[1] // const.GRID_SIZE)

        # clamp
        x = max(0, min(x, const.RESOLUTION[0] // const.GRID_SIZE - 1))
        y = max(0, min(y, const.RESOLUTION[1] // const.GRID_SIZE - 1))

        return (x, y)

    def __register_object(self, obj: Object) -> None:
        """
        Register an object in the hashmap

        Args:
        - obj: The object to register
        """
        grid_pos = self.__pos_to_grid(obj.pos)
        self.hashmap[grid_pos].add(obj)
    
    def set_surface(self, surface: pygame.Surface) -> None:
        """
        Set the surface to draw on

        Args:
        - surface: The surface to draw on
        """
        self.surface = surface
    
    def add(self, obj: Object) -> None:
        """
        Add an object to the simulation

        Args:
        - obj: The object to add
        """
        self.objects.add(obj)
        self.__register_object(obj)
    
    def remove(self, obj: Object) -> None:
        """
        Remove an object from the simulation

        Args:
        - obj: The object to remove
        """
        self.objects.remove(obj)
        grid_pos = self.__pos_to_grid(obj.pos)
        self.hashmap[grid_pos].remove(obj)
    
    def update(self, dt: float) -> None:
        """
        Update all the objects

        Args:
        - dt: Delta time
        """
        self.__update_hashmap(dt)
    
    def __update_hashmap(self, dt: float) -> None:
        """
        Update each cell in the hashmap independently
        """
        for obj_set in self.hashmap.values():
            self.__update_cell(obj_set, dt)
        
        # Clear the hashmap
        self.hashmap = self.__create_hashmap()

        # Re-register all the objects
        for obj in self.objects:
            self.__register_object(obj)
    
    def __update_cell(self, obj_set: Set[Object], dt: float) -> None:
        """
        Update the objects in a cell

        Args:
        - obj_set: The set of objects to update
        """
        for obj in obj_set:
            # Update & draw the object
            obj.update(dt)
            obj.draw(self.surface)