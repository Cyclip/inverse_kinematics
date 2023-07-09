from typing import *

import sim
import scenes


if __name__ == "__main__":
    s = sim.Simulation()
    s.set_scene(scenes.ArmTestScene)
    s.run()