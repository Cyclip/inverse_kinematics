from __future__ import annotations
from typing import *
import pygame
import constants as const
import numpy as np

"""
The main arm class
Includes an array of joints and an array of links, which are used to
calculate the forward kinematics of the arm.
"""

class Arm:
    # Rotation limits
    ROT_START = -np.pi / 2
    ROT_END = np.pi / 2

    def __init__(
            self,
            pos: np.ndarray,
            link_length: float,
            num_links: int,
            color: Tuple[int, int, int],
            joint_color: Tuple[int, int, int] = (255, 0, 0),
    ) -> None:
        """
        Create a new arm with zero rotation
        """
        self.pos = np.array(pos, dtype=np.float64)
        self.__link_length = link_length
        self.__num_links = num_links
        self.__color = color
        self.__joint_color = joint_color

        if link_length < 0:
            raise ValueError("link_length must be positive")

        # Create vector joint positions (size: num_links)
        # i.e. [0, 0, 0, 0]
        # self.joints = np.random.normal(Arm.ROT_START, Arm.ROT_END, num_links)
        self.joints = np.ones(num_links, dtype=np.float64)

        # Create matrix of link starting positions
        self.links = np.zeros((num_links, 2), dtype=np.float64)
        # Iteratively update link positions
        self.__update_links()
    
    def set_joint_angles(self, angles: np.ndarray) -> None:
        """
        Set the joint angles
        """
        if angles.shape != self.joints.shape:
            raise ValueError("angles must have the same shape as self.joints")

        self.joints = angles
        self.__update_links()
    
    def __update_links(self, start=1) -> None:
        """
        Update the starting positions of each link
        depending on the angle and length of the link

        Optionally, only update links starting from a certain index
        """
        # We get the sum of the joints up to the current index
        # because as we iterate through the joints, we want to
        # get the sum of the previous joints
        #
        # We do this since the north-line of the arm, whilst initially
        # 0, adjusts depending on the angle of the previous joint.
        # As such, we need to get the sum of the previous joints to
        # get the correct angle of the current joint

        if start < 1:
            raise ValueError("start must be greater than 1")

        # first set the starting position of the first link
        self.links[0] = self.pos

        for i in range(start, self.__num_links):
            # Get end position of previous link
            prev_end = self.__get_end_pos(i - 1)

            # Set to current
            self.links[i] = prev_end
    
    def __get_end_pos(self, idx: int) -> np.ndarray:
        """
        Get the end position of a link at a given index
        """
        start = self.links[idx]

        # Get sum of joints up to the current index
        # See __update_links() for explanation
        angle = np.sum(self.joints[:idx + 1])

        # Get the end position
        end = start + np.array([
            np.cos(angle),
            np.sin(angle),
        ]) * self.__link_length

        return end
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the arm
        """
        # Draw links
        for i in range(self.__num_links):
            if i == self.__num_links - 1:
                end = self.get_end_effector_pos()
            else:
                end = self.links[i + 1]

            pygame.draw.line(
                surface,
                self.__color,
                self.links[i],
                end,
                const.ARM_WIDTH,
            )
        
        # Draw joints
        for i in range(self.__num_links):
            pygame.draw.circle(
                surface,
                self.__joint_color,
                self.links[i],
                const.ARM_WIDTH,
            )
        
        # Draw end point of arm
        pygame.draw.circle(
            surface,
            (0, 255, 0),
            self.get_end_effector_pos(),
            const.ARM_WIDTH,
        )
    
    def get_end_effector_pos(self) -> np.ndarray:
        """
        Get the end effector position
        """
        return self.__get_end_pos(self.__num_links - 1)
    
    def update(self, dt: float) -> None:
        """
        Update the arm
        """
        pass