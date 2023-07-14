from typing import *
import numpy as np
from arm.arm import Arm
from scenes.setter import SceneSetter
import constants as const

from objects.ball import Ball
from objects.block import Block
from tasks import taskManager
from tasks.task import follow_linear_path, Wait, MoveToBall, HoldBall, MoveArm, ReleaseBall, MoveRelative
from colors import gen_colours

class FillJarScene(SceneSetter):
    """
    First evaluation scene for the arm

    The scene contains 2 jars on left and right of
    the arm. The arm's tasks are to fill the right
    jar with all the balls on the left jar.
    """
    # Number of balls in each row and column
    NUM_BALLS = 4

    def __init__(self) -> None:
        """
        Create a new scene setter

        Args:
        - sim: The simulation
        """
        super().__init__()
        self.taskManager = None
    
    def set_scene(self, sim: Any) -> None:
        """
        Create the scene
        """
        # Create an arm
        self.arm = Arm(
            np.array([
                const.RESOLUTION[0] // 2,
                const.RESOLUTION[1] // 2 - 100
            ]),
            70,
            5,
            (255, 255, 255),
            (255, 0, 0)
        )
    
        # Create the jars
        self.__make_jars(sim)

        # Create the balls
        self.__make_balls(sim)

        # Add the arm to the simulation
        sim.objects.add(self.arm)
    
    # override set controller
    def set_controller(self, controller: Any) -> None:
        """
        Set the controller
        """
        self.controller = controller

        # Setup the tasks
        self.__setup_tasks()
    
    def __setup_tasks(self) -> None:
        """
        Setup the tasks
        """
        # Create the task manager
        self.taskManager = taskManager.TaskManager(self.arm)

        controller = self.controller
        arm = self.arm

        self.taskManager.add_task(
            Wait(controller, arm, 100)
        )

        # Create a move_ball task for each ball
        for ball in self.balls:
            self.taskManager.add_tasks([
                MoveToBall(controller, arm, ball),                                  # Move the arm to the ball
                HoldBall(controller, arm, ball),                                    # Hold the ball
                MoveRelative(controller, arm, np.array([0, -50])),                   # Move the arm up
                MoveArm(controller, arm, self.rightJar[1].pos - np.array([-110, 250])),# Move the arm to the right jar
                ReleaseBall(controller, arm, ball)                                  # Release the ball into the jar
            ])

            # Wait for 1 second
            self.taskManager.add_task(
                Wait(self.controller, self.arm, 10)
            )
        
        # Move the arm to the left jar
        self.taskManager.add_tasks(
            follow_linear_path(
                self.controller,
                self.arm,
                self.leftJar[1].pos - np.array([0, 150]),
                self.leftJar[1].pos - np.array([0, 250])
            )
        )

    def __make_jars(self, sim: Any) -> None:
        y = const.RESOLUTION[1] // 2 - 50
        # distance from edges
        d = 300

        self.leftJar = self.__make_jar(
            sim,
            np.array([d, y])
        )

        self.rightJar = self.__make_jar(
            sim,
            np.array([const.RESOLUTION[0] - d - 200, y])
        )
    
    def __make_jar(self, sim: Any, offset: np.ndarray) -> List[Block]:
        """
        Create a jar

        Args:
        - sim: The simulation
        - offset: The offset of the jar

        Returns:
        - The jar
        """
        jar = [
            # left
            Block(
                offset + np.array([0, 0]),
                np.array([50, 200]),
                (255, 255, 255)
            ),
            # bottom
            Block(
                offset + np.array([0, 200]),
                np.array([200, 50]),
                (255, 255, 255)
            ),
            # right
            Block(
                offset + np.array([150, 0]),
                np.array([50, 200]),
                (255, 255, 255)
            )
        ]

        # Add the jar to the simulation
        for block in jar:
            sim.objects.add(block)

        return jar

    def __make_balls(self, sim: Any) -> None:
        # colours
        colours = gen_colours((214, 56, 45), self.NUM_BALLS ** 2)
        print(colours)

        # form a grid of balls above the left jar        
        self.balls = []
        for i in range(self.NUM_BALLS):
            for j in range(self.NUM_BALLS):
                self.balls.append(
                    Ball(
                        self.leftJar[1].pos + np.array([20 * i + 70, -20 * j - 150]),
                        15,
                        0.5,
                        # purple
                        colours[i * self.NUM_BALLS + j]
                    )
                )

                # Add the ball to the simulation
                sim.objects.add(self.balls[-1])

                # random velocity
                self.balls[-1].apply_impulse(
                    np.random.uniform(-50, 50, 2)
                )
    
    def update(self, sim: Any, dt: float) -> None:
        """
        Update the scene
        """
        self.taskManager.update()
        self.taskManager.draw(sim.surface)