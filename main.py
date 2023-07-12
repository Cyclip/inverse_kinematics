from typing import *

import sim
import scenes
from arm import controllers


if __name__ == "__main__":
    s = sim.Simulation()
    s.set_scene(scenes.FillJarScene)
    s.set_controller(controllers.SGDController(
        alpha=0.00012,
        weight_decay=0,
        epochs=4
    ))
    s.run()