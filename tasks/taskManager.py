from typing import *
from queue import Queue
import pygame

from tasks.task import Task
from arm.arm import Arm
import constants as const

class TaskManager:
    def __init__(self, arm: Arm):
        self.tasks = Queue()
        self.arm = arm
        self.current_task = None
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the queue
        """
        self.tasks.put(task)
        print("Added task:", task)
    
    def add_tasks(self, tasks: List[Task]) -> None:
        """
        Add a list of tasks to the queue
        """
        for task in tasks:
            self.add_task(task)

    def update(self) -> None:
        """
        Update the task manager's queue
        The current task will be handled and
        when it's done, the next task will be
        handled
        """
        if self.current_task is None:
            if not self.tasks.empty():
                self.current_task = self.tasks.get()
        else:
            self.current_task.update()
            if self.current_task.done:
                self.current_task = None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw text in the top-left displaying the
        current task:

        "Current task: <task name>"
        """
        if self.current_task is not None:
            text = const.FONT.render("Current task: " + str(self.current_task), True, (255, 255, 255))
            surface.blit(text, (10, 10))