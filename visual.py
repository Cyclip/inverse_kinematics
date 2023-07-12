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

# Target position
target = np.array([0, 0])

# Arm config
ROT_START = -np.pi / 2
ROT_END = np.pi / 2
LINK_LENGTH = 70

# Curve
POINTS = 50

# Gradient descent
EPOCHS = 5000
ALPHA = 0.0001


arm = Arm(
    np.array([0, 0]),
    LINK_LENGTH,
    2,
    (255, 255, 255)
)

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
        # (target - end point)^2
        distances[i, j] = np.linalg.norm(end_effector_pos - target)


# Now we're going to attempt to do gradient descent
# Initialise random set of angles
joint_angles = np.random.uniform(ROT_START, ROT_END, 2)
arm.set_joint_angles(joint_angles)

# history
hx = [joint_angles[0],]
hy = [joint_angles[1],]
hz = [np.linalg.norm(target - arm.get_end_effector_pos())]
his = []
hisx = np.linspace(1, EPOCHS, EPOCHS)

def wrap(value: float, start: float, end: float) -> float:
    range_size = end - start
    wrapped_value = (value - start) % range_size + start
    return wrapped_value

for i in range(EPOCHS):
    # get all the new angles
    # ∂e/∂p_n = l[
    #   -sin a
    #   cos a
    # ]
    #
    # derivative is 2(e - t)[ -sin a cos a ] matrix
    a = np.sum(joint_angles)
    x = np.array([
        -np.sin(a),
        np.cos(a)
    ])

    # Compute the gradient
    gradient = 2 * np.array([-np.sin(a), np.cos(a)]) * (arm.get_end_effector_pos() - target)

    # Replicate the gradient to match the length of joint_angles
    replicated_gradient = np.tile(gradient, len(joint_angles) // len(gradient))

    # Update the joint_angles using gradient descent
    joint_angles -= ALPHA * replicated_gradient

    arm.set_joint_angles(joint_angles)
    dis = np.linalg.norm(target - arm.get_end_effector_pos())
    his.append(dis)

    if i % (EPOCHS // 5) == 0:
        hx.append(wrap(joint_angles[0], ROT_START, ROT_END))
        hy.append(wrap(joint_angles[1], ROT_START, ROT_END))
        hz.append(dis)

print(f"Final: {joint_angles}")

# Plot the curve
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.plot_surface(
    joint1_angles,
    joint2_angles,
    distances,
    edgecolor="none",
    alpha=0.8,
)

# Plot gradient descent
ax.plot3D(
    hx,
    hy,
    hz,
    color="red"
    # alpha=0.2
)

last = len(hx) - 1
ax.scatter(
    hx[last], hy[last], hz[last],
    alpha=1,
    c="green",
    s=25
)

ax.set_xlabel("p₁")
ax.set_ylabel("p₂")
ax.set_zlabel("Raw distance")
ax.set_title("Arm Configuration Space")

# ax2
ax2 = fig.add_subplot(122)
ax2.plot(hisx, his, color="red")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Elevation")

plt.show()