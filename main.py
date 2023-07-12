from typing import *

import sim
import scenes
from arm import controllers


if __name__ == "__main__":
    s = sim.Simulation()
    s.set_scene(scenes.FollowMouseScene)
    s.set_controller(controllers.SGDController(
        alpha=0.0001,
        weight_decay=-1,
        epochs=10
    ))
    s.run()