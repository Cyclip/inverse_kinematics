from typing import *
import numpy as np

from objects.ball import Ball
from arm.controllers.base import Controller
from arm.arm import Arm
import constants as const


class Task:
    """
    Base task object
    """
    def __init__(self, controller: Controller, arm: Arm):
        self.done = False
        self.controller = controller
        self.arm = arm
    
    def update(self) -> None:
        """
        Check if the task is done
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__


class HoldBall(Task):
    """
    Task the arm to hold a certain ball
    """
    def __init__(self, controller: Controller, arm: Arm, ball: Ball):
        super().__init__(controller, arm)
        self.ball = ball

    def update(self) -> None:
        # Use controller to move the arm
        self.controller.update(self.arm, self.ball.pos)

        # Check if the ball is touching arm's end effector
        ballpos = self.ball.pos
        armpos = self.arm.get_end_effector_pos()

        if np.linalg.norm(ballpos - armpos) < self.ball.radius + const.ARM_END_RADIUS:
            self.done = True
            # make the ball static
            self.ball.set_held(True, self.arm)
            self.ball.vel = np.zeros(2, dtype=np.float64)
            self.ball.acc = np.zeros(2, dtype=np.float64)


class MoveArm(Task):
    """
    Task to move the arm to a certain position
    """
    def __init__(self, controller: Controller, arm: Arm, target: np.ndarray):
        super().__init__(controller, arm)
        self.target = target
    
    def update(self) -> None:
        # Use controller to move the arm
        self.controller.update(self.arm, self.target)

        # Check if the arm is at the target
        armpos = self.arm.get_end_effector_pos()
        if np.linalg.norm(armpos - self.target) < const.ARM_END_RADIUS:
            self.done = True
            self.arm.vel = np.zeros(2, dtype=np.float64)
            self.arm.acc = np.zeros(2, dtype=np.float64)
    
    def __str__(self) -> str:
        return f"Move arm to {round(self.target[0])}, {round(self.target[1])} (distance: {round(np.linalg.norm(self.arm.get_end_effector_pos() - self.target))})))"


class MoveToBall(Task):
    """
    Special task to move the arm to a ball
    """
    def __init__(self, controller: Controller, arm: Arm, ball: Ball):
        super().__init__(controller, arm)
        self.ball = ball
    
    def update(self) -> None:
        # Use controller to move the arm
        self.controller.update(self.arm, self.ball.pos)

        # Check if the arm is touching the ball
        armpos = self.arm.get_end_effector_pos()
        if np.linalg.norm(armpos - self.ball.pos) < const.ARM_END_RADIUS + self.ball.radius:
            self.done = True
            self.arm.vel = np.zeros(2, dtype=np.float64)
            self.arm.acc = np.zeros(2, dtype=np.float64)
    
    def __str__(self) -> str:
        ballpos = f"{round(self.ball.pos[0])}, {round(self.ball.pos[1])}"
        distance = round(np.linalg.norm(self.arm.get_end_effector_pos() - self.ball.pos))
        return f"Move arm to ball at {ballpos} (distance: {distance})"


class ReleaseBall(Task):
    """
    Task to release a ball
    """
    def __init__(self, controller: Controller, arm: Arm, ball: Ball):
        super().__init__(controller, arm)
        self.ball = ball
    
    def update(self) -> None:
        # Check if the ball is being held
        if self.ball.held:
            self.done = True
            self.ball.set_held(False)
            self.ball.vel = np.zeros(2, dtype=np.float64)
            self.ball.acc = np.zeros(2, dtype=np.float64)
        else:
            print("Ball is not being held!")


class Wait(Task):
    """
    Task to wait for a certain amount of time
    """
    def __init__(self, controller: Controller, arm: Arm, time: float):
        super().__init__(controller, arm)
        self.time = time
        self.timer = 0
    
    def update(self) -> None:
        self.timer += 1
        if self.timer >= self.time:
            self.done = True
    
    def __str__(self) -> str:
        # print time remaining
        return f"Wait for {round(self.time - self.timer)} ticks"


# Task generators
def move_ball(controller: Controller, arm: Arm, ball: Ball, target: np.ndarray) -> List[Task]:
    """
    Generate a list of tasks to move a ball to a target position

    Args:
    - arm: The arm
    - ball: The ball
    - target: The position of the jar
    """
    
    return [
        MoveToBall(controller, arm, ball),
        HoldBall(controller, arm, ball),
        MoveArm(controller, arm, target),
        ReleaseBall(controller, arm, ball)
    ]

def follow_linear_path(controller: Controller, arm: Arm, start: np.ndarray, end: np.ndarray, n=10) -> List[Task]:
    """
    Generate a list of tasks to follow a linear path

    Args:
    - arm: The arm
    - start: The start position
    - end: The end position
    - n: The number of points to interpolate
    """
    tasks = []
    points = np.linspace(start, end, n)
    for point in points:
        tasks.append(MoveArm(controller, arm, point))
    return tasks

def follow_circular_path(controller: Controller, arm: Arm, center: np.ndarray, radius: float, n=10) -> List[Task]:
    """
    Generate a list of tasks to follow a circular path

    Args:
    - arm: The arm
    - center: The center of the circle
    - radius: The radius of the circle
    - n: The number of points to interpolate
    """
    tasks = []
    angles = np.linspace(0, 2 * np.pi, n)
    for angle in angles:
        point = np.array([
            center[0] + radius * np.cos(angle),
            center[1] + radius * np.sin(angle)
        ])
        tasks.append(MoveArm(controller, arm, point))
    return tasks