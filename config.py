ROBOT = "unitree/go2"  # Robot name, "go2", "b2", "b2w", "h1", "go2w", "g1"
GENESIS_BACKEND = "cuda"  # Genesis backend, "cpu", "cuda", "vulkan"
ROBOT_FILE = "robots/" + ROBOT + "/robot.urdf"  # Robot file
DOMAIN_ID = 1  # Domain id
INTERFACE = "lo"  # Interface

DOF_NAMES = [
    "FR_hip_joint",
    "FR_thigh_joint",
    "FR_calf_joint",
    "FL_hip_joint",
    "FL_thigh_joint",
    "FL_calf_joint",
    "RR_hip_joint",
    "RR_thigh_joint",
    "RR_calf_joint",
    "RL_hip_joint",
    "RL_thigh_joint",
    "RL_calf_joint",
],
INIT_HEIGHT = 0.5  # Initial height

SIMULATE_DT = 0.005  # Need to be larger than the runtime of viewer.sync()
VIEWER_DT = 0.02  # 50 fps for viewer
