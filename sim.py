import pygame
import constants as const
import numpy as np

from objects.ball import Ball
from objects.manager import ObjectManager

class Simulation:
    """
    The main simulation class
    """
    def __init__(self) -> None:
        self.running = False
        self.objects = ObjectManager()
        
        pygame.init()
        pygame.display.set_caption("Inverse Kinematics")
    
    def run(self) -> None:
        """
        Run the simulation
        """
        self.surface = pygame.display.set_mode(const.RESOLUTION)
        self.objects.set_surface(self.surface)

        # Create a clock to limit the framerate
        clock = pygame.time.Clock()

        # Create balls bouncing around
        for i in range(150):
            ball = Ball(
                pos=(np.random.randint(0, const.RESOLUTION[0]), np.random.randint(0, const.RESOLUTION[1])),
                radius=np.random.randint(10, 30),
                mass=np.random.randint(1, 10),
                color=(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
            )
            ball.apply_force(np.random.randint(-650, 650, 2))
            self.objects.add(ball)

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Get delta time
            # dt = clock.tick() / 1000
            dt = 0.2

            # Clear the screen
            self.surface.fill((0, 0, 0))

            # draw grid
            for i in range(const.RESOLUTION[0] // const.GRID_SIZE):
                pygame.draw.line(self.surface, (255, 255, 255), (i * const.GRID_SIZE, 0), (i * const.GRID_SIZE, const.RESOLUTION[1]))
            for j in range(const.RESOLUTION[1] // const.GRID_SIZE):
                pygame.draw.line(self.surface, (255, 255, 255), (0, j * const.GRID_SIZE), (const.RESOLUTION[0], j * const.GRID_SIZE))

            # Update the objects
            self.__update_objects(dt)
            
            pygame.display.update()

            # Limit the framerate
            clock.tick(60)
    
    def __update_objects(self, dt: float) -> None:
        """
        Update all the objects

        Args:
        - dt: Delta time
        """
        self.objects.update(dt)
        self.objects.draw()