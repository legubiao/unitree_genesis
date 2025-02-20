# Unitree Genesis
A genesis simulation based on [unitree_sdk_python](https://github.com/unitreerobotics/unitree_sdk2_python), but not only unitree robots.

![](.images/ros2control.png)

> **Todo List**:
> * [x] **[2025-01-15]** Go2 Robot with ROS2-Control
> * [ ] IMU sensor (waiting for genesis update) 
> * [ ] More robots
> * [ ] High-level state broadcast

## Install Dependencies
* Create a conda env (I used pycharm and miniconda)
* Install cuda and config environment variables
  ```bash
  export PATH="$PATH:/usr/local/cuda/bin"
  export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
  ```
* Clone and install latest Genesis
  ```bash
  git clone https://github.com/Genesis-Embodied-AI/Genesis.git
  cd Genesis
  pip install -e .
  ```
* Install [Unitree SDK2 Python](https://github.com/unitreerobotics/unitree_sdk2_python), **Don't used the version installed by pip**
  ```bash
  git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
  cd unitree_sdk2_python
  pip3 install -e .
  ```

## Controller

* ROS2 Distrobox command
    ```bash
    distrobox create --name ubuntu22 --additional-flags "--runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all" --image ubuntu:22.04 --home ~/distrobox/ubuntu22
    ```