from __future__ import annotations
from typing import *
import pygame
import constants as const
import numpy as np
from arm.controllers.base import Controller

"""
The Stochastic Gradient Descent class
"""

class SGDController(Controller):
    def __init__(self, alpha: float = 0.001, weight_decay: float = 0.01, epochs: int = 10, epsilon: float = 0.1) -> None:
        """
        Create a new SGD controller

        Args:
        - alpha: The learning rate
        - weight_decay: The weight decay
        - epochs: The number of epochs
        - epsilon: The epsilon for calculating the gradient
        """
        self.alpha = alpha
        self.weight_decay = weight_decay
        self.epochs = epochs
        self.epsilon = epsilon
    
    def update(self, arm: Any, target: np.ndarray) -> None:
        """
        Update the arm using SGD to a target

        Args:
        - arm: The arm to update
        - target: The target to update to
        """
        for _ in range(self.epochs):
            self.__update(arm, target)
    
    def __update(self, arm: Any, target: np.ndarray) -> None:
        joint_angles = arm.joints

        # Calculate the loss
        end = arm.get_end_effector_pos()
        error = end - target
        loss = np.linalg.norm(error)

        # Calculate the gradient
        gradient = np.zeros_like(joint_angles)
        for i in range(len(joint_angles)):
            # Calculate the gradient for each joint
            joint_angles[i] += self.epsilon
            arm.set_joint_angles(joint_angles)
            end = arm.get_end_effector_pos()
            error = target - end
            loss2 = np.linalg.norm(error)
            gradient[i] = (loss2 - loss) / self.epsilon
            joint_angles[i] -= self.epsilon

        # Update the joint angles
        joint_angles -= self.alpha * gradient
        # joint_angles -= self.weight_decay * joint_angles

        arm.set_joint_angles(joint_angles)
