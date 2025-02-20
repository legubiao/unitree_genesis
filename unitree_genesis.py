import genesis as gs

import config
from unitree_bridge import UnitreeSdk2GenesisBridge

# Configure the genesis backend
if config.GENESIS_BACKEND == "cuda":
    gs.init(backend=gs.cuda)
elif config.GENESIS_BACKEND == "vulkan":
    gs.init(backend=gs.vulkan)
else:
    gs.init(backend=gs.cpu)

scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=config.SIMULATE_DT,
        gravity=(0, 0, -9.81),
    ),
    viewer_options=gs.options.ViewerOptions(
        max_FPS=config.VIEWER_FPS,
    ),
)

# Configure the scene
plane = scene.add_entity(
    gs.morphs.Plane(),
)
robot = scene.add_entity(
    gs.morphs.URDF(
        file=config.ROBOT_FILE,
        pos=(0, 0, config.INIT_HEIGHT),
    ),
)

scene.build()
unitree = UnitreeSdk2GenesisBridge(robot, scene, gs)

while True:
    scene.step()
