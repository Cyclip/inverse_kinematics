from typing import *
from objects.obj import Object
from objects.block import Block
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
        # Moving objects
        self.dynamic_objects = set()
        # Static objects
        self.static_objects = set()
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
        if isinstance(obj, Block):
            self.static_objects.add(obj)
        else:
            self.dynamic_objects.add(obj)
            self.__register_object(obj)
    
    def remove(self, obj: Object) -> None:
        """
        Remove an object from the simulation

        Args:
        - obj: The object to remove
        """
        self.dynamic_objects.remove(obj)
        grid_pos = self.__pos_to_grid(obj.pos)
        self.hashmap[grid_pos].remove(obj)
    
    def update(self, dt: float) -> None:
        """
        Update all the objects

        Args:
        - dt: Delta time
        """
        self.__update_hashmap(dt)
    
    def draw(self) -> None:
        """
        Draw all the objects
        """
        for obj in self.dynamic_objects | self.static_objects:
            obj.draw(self.surface)
    
    def __update_hashmap(self, dt: float) -> None:
        """
        Update each cell in the hashmap independently
        """
        # Update each cell
        # Iterate over keys
        for key in self.hashmap.keys():
            self.__update_cell(key, dt)
        
        # Clear the hashmap
        self.hashmap = self.__create_hashmap()

        # Re-register all the objects
        for obj in self.dynamic_objects:
            self.__register_object(obj)
    
    def __update_cell(self, key: Tuple[int, int], dt: float) -> None:
        """
        Update a cell in the hashmap

        Args:
        - key: The key of the cell
        - dt: Delta time
        """
        # Get the neighbouring cells
        # Include static objects
        neighbours = self.__get_neighbours(key) | self.static_objects

        # Update each object in the cell
        for obj in self.hashmap[key]:
            obj.update(dt, neighbours)
    
    def __get_neighbours(self, key: Tuple[int, int]) -> Set[Object]:
        """
        Get the neighbouring cells of a cell

        Args:
        - key: The key of the cell

        Returns:
        - The neighbouring cells
        """
        # Get neighbouring keys within the hashmap
        neighbours = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_key = (key[0] + i, key[1] + j)
                if new_key in self.hashmap:
                    neighbours |= self.hashmap[new_key]
        
        return neighbours