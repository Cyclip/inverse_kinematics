import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Importing Axes3D from mpl_toolkits.mplot3d
from arm.arm import Arm

"""
Create a visual 3D curve representing the arm's possible positions
and distances from the target

The elevation of the curve will represent the distance from the target
squared, and the azimuth will represent the angle of the arm

Key methods:
arm.set_joint_angles(angles: np.ndarray) -> None
    This method sets the joint angles of the arm
    and updates the link positions accordingly

arm.get_end_effector_pos() -> np.ndarray
    This method returns the position of the end effector
    of the arm
"""

arm = Arm(
    np.array([0, 0]),
    70,
    2,
    (255, 255, 255)
)

# Target position
target = np.array([100, 100])

# Joint rotation limits
ROT_START = -np.pi / 2
ROT_END = np.pi / 2

# Number of points to plot
POINTS = 50

joint1_angles = np.linspace(ROT_START, ROT_END, POINTS)
joint2_angles = np.linspace(ROT_START, ROT_END, POINTS)

# Create a grid of joint angles
joint1_angles, joint2_angles = np.meshgrid(joint1_angles, joint2_angles)

# Create a grid of distances from the target
distances = np.zeros((POINTS, POINTS))

for i in range(POINTS):
    for j in range(POINTS):
        # Set the joint angles
        arm.set_joint_angles(np.array([joint1_angles[i, j], joint2_angles[i, j]]))
        
        # Get the end effector position
        end_effector_pos = arm.get_end_effector_pos()
        
        # Calculate the distance from the target
        # Raw distance may be positive or negative
        distances[i, j] = np.linalg.norm(target - end_effector_pos)

# Plot the curve
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(
    joint1_angles,
    joint2_angles,
    distances,
    cmap="viridis",
    edgecolor="none"
)

ax.set_xlabel("p₁")
ax.set_ylabel("p₂")
ax.set_zlabel("Raw distance")
ax.set_title("Arm Configuration Space")

plt.show()