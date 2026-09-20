# Autonomous Vehicle Reflexive Braking System

A safety-critical reflexive braking supervisor designed for autonomous electric vehicles. Built using **ROS 2 Humble** and simulated in **Gazebo**, this system provides a deterministic, failsafe emergency intervention layer bridging physical actuator limits with software perception.

---

## 📌 Overview
While autonomous planners excel at high-level navigation, dynamic edge-case obstacles require low-latency, deterministic reflexes. This project addresses the gap between software decision-making and physical brake latencies:
- **Time-to-Collision (TTC) Dynamic Supervisor:** Continuously evaluates forward laser scans against vehicle odometry.
- **Hierarchical Safety Control:** Multi-tier state logic (`NOMINAL`, `WARNING`, `EMERGENCY_BRAKE`).
- **Physical Dynamics Consideration:** Models mechanical brake delay and deceleration limits ($a_{\text{brake}} = -\mu \cdot g$).

---

## 🛠 Tech Stack
- **Middleware:** ROS 2 Humble Hawksbill
- **Simulation:** Gazebo 11 / Ignition
- **Languages:** Python 3.10
- **Interfaces:** `rclpy`, `sensor_msgs`, `nav_msgs`, `geometry_msgs`

---

## 🏗 Architecture

```text
[ /scan (LaserScan) ] ──┐
                         ├──> [ Sensor Fusion / TTC Node ]
[ /odom (Odometry)  ] ──┘                 │
                                          v
[ /cmd_vel (Planner) ] ───────> [ Safety Supervisor ] ───> [ /cmd_vel (Gazebo Robot) ]
```

---

## 🚀 Getting Started (Laptop Setup)

```bash
# Clone the repository
git clone https://github.com/Adiseshareddy1221/autonomous-reflexive-braking.git
cd autonomous-reflexive-braking/reflexive_braking_ws