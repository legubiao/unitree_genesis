import config
import torch
import numpy as np

from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelPublisher
from unitree_sdk2py.utils.thread import RecurrentThread
from unitree_sdk2py.core.channel import ChannelFactoryInitialize

from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowCmd_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.idl.default import unitree_go_msg_dds__LowState_ as LowState_default
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_

TOPIC_LOWCMD = "rt/lowcmd"
TOPIC_LOWSTATE = "rt/lowstate"
TOPIC_HIGHSTATE = "rt/sportmodestate"
TOPIC_WIRELESS_CONTROLLER = "rt/wirelesscontroller"


class UnitreeSdk2GenesisBridge:
    def __init__(self, robot, scene):

        ChannelFactoryInitialize(config.DOMAIN_ID, config.INTERFACE)

        self.robot = robot
        self.scene = scene
        self.motor_dofs = [robot.get_joint(name).dof_idx_local for name in config.DOF_NAMES[0]]
        self.num_motor = len(self.motor_dofs)

        self.dof_pos = torch.zeros(self.num_motor)
        self.dof_vel = torch.zeros(self.num_motor)
        self.dof_torque = torch.zeros(self.num_motor)

        self.output_force = np.zeros(self.num_motor)

        # Unitree sdk2 message
        # LowState
        self.low_state = LowState_default()
        self.low_state_puber = ChannelPublisher(TOPIC_LOWSTATE, LowState_)
        self.low_state_puber.Init()
        self.lowStateThread = RecurrentThread(
            interval=self.scene.dt, target=self.publish_low_state, name="sim_lowstate"
        )
        self.lowStateThread.Start()

        # LowCmd
        self.low_cmd_suber = ChannelSubscriber(TOPIC_LOWCMD, LowCmd_)
        self.low_cmd_suber.Init(self.low_cmd_handler, 10)

        # High state
        self.high_state = unitree_go_msg_dds__SportModeState_()
        self.high_state_puber = ChannelPublisher(TOPIC_HIGHSTATE, SportModeState_)
        self.high_state_puber.Init()
        self.HighStateThread = RecurrentThread(
            interval=self.scene.dt, target=self.publish_high_state, name="sim_highstate"
        )
        self.HighStateThread.Start()

    def publish_low_state(self):
        self.dof_pos[:] = self.robot.get_dofs_position(self.motor_dofs)
        self.dof_vel[:] = self.robot.get_dofs_velocity(self.motor_dofs)
        self.dof_torque[:] = self.robot.get_dofs_force(self.motor_dofs)

        # Joint readings
        for i in range(self.num_motor):
            self.low_state.motor_state[i].q = self.dof_pos[i]
            self.low_state.motor_state[i].dq = self.dof_vel[i]
            self.low_state.motor_state[i].tau_est = self.dof_torque[i]

        # IMU readings
        self.low_state.imu_state.quaternion[:] = self.robot.get_quat()[:4]
        self.low_state.imu_state.gyroscope[:] = self.robot.get_ang()[:3]
        self.low_state.imu_state.accelerometer[:] = [0, 0, -9.81]
        # Todo: Waiting Genesis to add accelerometer readings

        self.low_state_puber.Write(self.low_state)

    def low_cmd_handler(self, msg: LowCmd_):
        for i in range(self.num_motor):
            self.output_force[i] = (
                    msg.motor_cmd[i].tau
                    + msg.motor_cmd[i].kp * (msg.motor_cmd[i].q - self.dof_pos[i])
                    + msg.motor_cmd[i].kd * (msg.motor_cmd[i].dq - self.dof_vel[i])
            )
        self.robot.control_dofs_force(self.output_force, self.motor_dofs)

    def publish_high_state(self):
        self.high_state.position[:] = self.robot.get_pos()[:3]
        self.high_state.velocity[:] = self.robot.get_vel()[:3]
        self.high_state_puber.Write(self.high_state)
