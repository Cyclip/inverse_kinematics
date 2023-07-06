import pygame
import constants as const
import numpy as np

from objects.ball import Ball

class Simulation:
    """
    The main simulation class
    """
    def __init__(self) -> None:
        self.running = False
        self.objects = set()
        
        pygame.init()
        pygame.display.set_caption("Inverse Kinematics")
    
    def run(self) -> None:
        """
        Run the simulation
        """
        self.surface = pygame.display.set_mode(const.RESOLUTION)

        # Create a clock to limit the framerate
        clock = pygame.time.Clock()

        # Create a ball
        ball = Ball((100, 100), 10, 1, (255, 255, 255))
        self.objects.add(ball)

        # set ball velocity
        ball.vel = np.array([60, 0], dtype=np.float64)

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

            # Update the objects
            for obj in self.objects:
                obj.update(dt)
                print(obj.pos)
                obj.draw(self.surface)
            
            pygame.display.update()

            # Limit the framerate
            clock.tick(60)