from typing import *
import numpy as np
from arm.arm import Arm
from scenes.setter import SceneSetter
import constants as const

from objects.ball import Ball
from objects.block import Block
from tasks import taskManager
from tasks.task import follow_linear_path, Wait, MoveToBall, HoldBall, MoveArm, ReleaseBall, MoveRelative

class FillJarScene(SceneSetter):
    """
    First evaluation scene for the arm

    The scene contains 2 jars on left and right of
    the arm. The arm's tasks are to fill the right
    jar with all the balls on the left jar.
    """
    # Number of balls in each row and column
    NUM_BALLS = 3

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
            100,
            3,
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
            Wait(controller, arm, 30)
        )

        # Create a move_ball task for each ball
        for ball in self.balls:
            self.taskManager.add_tasks([
                MoveToBall(controller, arm, ball),                                  # Move the arm to the ball
                HoldBall(controller, arm, ball),                                    # Hold the ball
                MoveRelative(controller, arm, np.array([0, -50])),                   # Move the arm up
                MoveArm(controller, arm, self.rightJar[1].pos - np.array([0, 250])),# Move the arm to the right jar
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
        y = const.RESOLUTION[1] // 2
        mid = const.RESOLUTION[0] // 2
        distanceFromMiddle = 80

        self.leftJar = self.__make_jar(
            sim,
            np.array([
                mid - distanceFromMiddle,
                y
            ])
        )

        self.rightJar = self.__make_jar(
            sim,
            np.array([
                mid + distanceFromMiddle + 125,
                y
            ])
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
        # Left, bottom, right
        jar = [
            Block(
                pos=np.array([
                    offset[0] - 150,
                    offset[1] + 50,
                ]),
                size=np.array([50, 250]),
                color=(255, 255, 255)
            ),

            Block(
                pos=np.array([
                    offset[0] - 76,
                    offset[1] + 150
                ]),
                size=np.array([100, 50]),
                color=(255, 255, 255)
            ),
            
            Block(
                pos=np.array([
                    offset[0] - 1,
                    offset[1] + 50,
                ]),
                size=np.array([50, 250]),
                color=(255, 255, 255)
            )
        ]

        # Add the jar to the simulation
        for block in jar:
            sim.objects.add(block)

        return jar

    def __make_balls(self, sim: Any) -> None:
        # form a grid of balls above the left jar
        self.balls = []
        for i in range(self.NUM_BALLS):
            for j in range(self.NUM_BALLS):
                self.balls.append(
                    Ball(
                        np.array([
                            self.leftJar[0].pos[0] + i * 20 + 50,
                            self.leftJar[0].pos[1] - j * 20 - 100
                        ]),
                        10,
                        0.5,
                        (255, 255, 255)
                    )
                )

                # Add the ball to the simulation
                sim.objects.add(self.balls[-1])

                # random vel ball
                self.balls[-1].vel = np.random.normal(0, 10, 2)
    
    def update(self, sim: Any, dt: float) -> None:
        """
        Update the scene
        """
        self.taskManager.update()
        self.taskManager.draw(sim.surface)