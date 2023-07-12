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
    def __init__(self, alpha: float = 0.001) -> None:
        """
        Create a new SGD controller

        Args:
        - alpha: The learning rate
        """
        self.alpha = alpha
    
    def update(self, arm: Any, target: np.ndarray) -> None:
        """
        Update the arm using SGD to a target

        Args:
        - arm: The arm to update
        - target: The target to update to
        """
        joint_angles = arm.joints

        a = np.sum(joint_angles)
        x = np.array([
            -np.sin(a),
            np.cos(a)
        ])

        # Compute the gradient
        gradient = 2 * np.array([-np.sin(a), np.cos(a)]) * (arm.get_end_effector_pos() - target)

        # Replicate the gradient to match the length of joint_angles
        # replicated_gradient = np.tile(gradient, len(joint_angles) // len(gradient))

        # Update the joint_angles using gradient descent
        joint_angles -= self.alpha * gradient

        arm.set_joint_angles(joint_angles)