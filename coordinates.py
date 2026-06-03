import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def calculate_bone_position(upper_arm_length, forearm_length, up_angle_deg, inward_angle_deg):
    radians_up = math.radians(up_angle_deg)
    radians_inward = math.radians(inward_angle_deg)

    start_offset = 0.3  # 30 cm offset in y-axis
    left_start_x = 0
    left_start_y = start_offset
    left_start_z = 0

    right_start_x = 0
    right_start_y = -start_offset
    right_start_z = 0

    # Left side
    left_upper_arm_end_x = upper_arm_length * math.sin(radians_up) * math.cos(radians_inward)
    left_upper_arm_end_y = start_offset + upper_arm_length * math.cos(radians_up)
    left_upper_arm_end_z = upper_arm_length * math.sin(radians_up) * math.sin(radians_inward)

    left_forearm_start_x = left_upper_arm_end_x
    left_forearm_start_y = left_upper_arm_end_y
    left_forearm_start_z = left_upper_arm_end_z

    left_forearm_end_x = left_forearm_start_x + forearm_length * math.sin(radians_up) * math.cos(radians_inward)
    left_forearm_end_y = left_forearm_start_y - forearm_length * math.cos(radians_up)
    left_forearm_end_z = left_forearm_start_z + forearm_length * math.sin(radians_up) * math.sin(radians_inward)

    # Right side (mirrored along y-axis)
    right_upper_arm_end_x = upper_arm_length * math.sin(radians_up) * math.cos(radians_inward)
    right_upper_arm_end_y = -start_offset - upper_arm_length * math.cos(radians_up)
    right_upper_arm_end_z = upper_arm_length * math.sin(radians_up) * math.sin(radians_inward)

    right_forearm_start_x = right_upper_arm_end_x
    right_forearm_start_y = right_upper_arm_end_y
    right_forearm_start_z = right_upper_arm_end_z

    right_forearm_end_x = right_forearm_start_x + forearm_length * math.sin(radians_up) * math.cos(radians_inward)
    right_forearm_end_y = right_forearm_start_y + forearm_length * math.cos(radians_up)
    right_forearm_end_z = right_forearm_start_z + forearm_length * math.sin(radians_up) * math.sin(radians_inward)

    return (left_start_x, left_start_y, left_start_z), \
           (left_upper_arm_end_x, left_upper_arm_end_y, left_upper_arm_end_z), \
           (left_forearm_start_x, left_forearm_start_y, left_forearm_start_z), \
           (left_forearm_end_x, left_forearm_end_y, left_forearm_end_z), \
           (right_start_x, right_start_y, right_start_z), \
           (right_upper_arm_end_x, right_upper_arm_end_y, right_upper_arm_end_z), \
           (right_forearm_start_x, right_forearm_start_y, right_forearm_start_z), \
           (right_forearm_end_x, right_forearm_end_y, right_forearm_end_z)

# Function to generate arm poses and collect coordinates for both left and right sides
def generate_arm_poses(num_poses, start_up_angle, end_up_angle, start_inward_angle, end_inward_angle):
    coordinates = []
    for i in range(num_poses):
        up_angle_deg = start_up_angle - (start_up_angle - end_up_angle) * i / (num_poses - 1)
        inward_angle_deg = start_inward_angle - (start_inward_angle - end_inward_angle) * i / (num_poses - 1)
        
        left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
        right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = \
        calculate_bone_position(upper_arm_length, forearm_length, up_angle_deg, inward_angle_deg)
        
        coordinates.append((left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos,
                            right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos))
    return coordinates

# Function to generate forearm poses and collect coordinates for both left and right sides
def generate_forearm_poses(fixed_upper_angle, max_forearm_angle, num_forearm_poses):
    coordinates = []
    for j in range(num_forearm_poses):
        forearm_inward_angle = (max_forearm_angle / (num_forearm_poses - 1)) * j
        
        left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
        right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = \
        calculate_bone_position(upper_arm_length, forearm_length, fixed_upper_angle, forearm_inward_angle)
        
        coordinates.append((left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos,
                            right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos))
    return coordinates

# Function to generate fixed arm poses in range and collect coordinates for both left and right sides
def generate_fixed_arm_poses_in_range(start_angle, end_angle, num_poses):
    coordinates = []
    for i in range(num_poses):
        angle = start_angle + (end_angle - start_angle) * i / (num_poses - 1)
        
        left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
        right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = \
        calculate_bone_position(upper_arm_length, forearm_length, angle, 0)
        
        coordinates.append((left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos,
                            right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos))
    return coordinates

# Parameters
upper_arm_length = 1.0
forearm_length = 1.0
number_of_poses_to_generate = 10

# Generate coordinates for each set of poses
arm_pose_coords = generate_arm_poses(number_of_poses_to_generate, 90, 70, 5, -5)
forearm_pose_coords = []

angle_ranges = {45: 30, 50: 30, 55: 25, 60: 25}
for angle, max_forearm_angle in angle_ranges.items():
    forearm_pose_coords.extend(generate_forearm_poses(angle, max_forearm_angle, number_of_poses_to_generate))

fixed_pose_coords = generate_fixed_arm_poses_in_range(65, 85, number_of_poses_to_generate)

##===================================================================================
##===================================================================================
# Additional angles to explore
additional_angles = {
    30: 30,   # Upper arm elevation starting from 30 degrees
    75: 20,   # Upper arm elevation from 75 to 55 degrees
    40: 20,   # Upper arm elevation from 40 to 20 degrees
    50: 15    # Upper arm elevation from 50 to 35 degrees
}

for angle, max_forearm_angle in additional_angles.items():
    forearm_pose_coords.extend(generate_forearm_poses(angle, max_forearm_angle, number_of_poses_to_generate))
    
# Additional fixed poses
additional_fixed_pose_coords = generate_fixed_arm_poses_in_range(50, 70, number_of_poses_to_generate)
fixed_pose_coords.extend(additional_fixed_pose_coords)

##===================================================================================
##===================================================================================

# Plot the coordinates
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot arm poses
for i, pose in enumerate(arm_pose_coords):
    left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
    right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
    ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
            [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
            [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
            c='r', linestyle='-', label='Arm Pose - Left Upper Arm' if i == 0 else "")
    
    ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
            [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
            [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
            c='b', linestyle='-', label='Arm Pose - Left Forearm' if i == 0 else "")
    
    ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
            [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
            [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
            c='r', linestyle='-', label='Arm Pose - Right Upper Arm' if i == 0 else "")
    
    ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
            [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
            [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
            c='b', linestyle='-', label='Arm Pose - Right Forearm' if i == 0 else "")

# Plot forearm poses
for j, pose in enumerate(forearm_pose_coords):
    left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
    right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
    ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
            [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
            [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
            c='g', linestyle='--', label='Forearm Pose - Left Upper Arm' if j == 0 else "")
    
    ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
            [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
            [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
            c='olive', linestyle='--', label='Forearm Pose - Left Forearm' if j == 0 else "")
    
    ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
            [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
            [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
            c='g', linestyle='--', label='Forearm Pose - Right Upper Arm' if j == 0 else "")
    
    ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
            [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
            [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
            c='olive', linestyle='--', label='Forearm Pose - Right Forearm' if j == 0 else "")

# Plot fixed poses
for k, pose in enumerate(fixed_pose_coords):
    left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
    right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
    ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
            [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
            [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
            c='gold', linestyle=':', label='Fixed Pose - Left Upper Arm' if k == 0 else "")
    
    ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
            [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
            [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
            c='coral', linestyle=':', label='Fixed Pose - Left Forearm' if k == 0 else "")
    
    ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
            [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
            [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
            c='gold', linestyle=':', label='Fixed Pose - Right Upper Arm' if k == 0 else "")
    
    ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
            [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
            [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
            c='coral', linestyle=':', label='Fixed Pose - Right Forearm' if k == 0 else "")

# Plot additional forearm poses
for l, pose in enumerate(additional_fixed_pose_coords):
    left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
    right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
    ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
            [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
            [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
            c='m', linestyle='-.', label='Additional Pose - Left Upper Arm' if l == 0 else "")
    
    ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
            [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
            [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
            c='c', linestyle='-.', label='Additional Pose - Left Forearm' if l == 0 else "")
    
    ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
            [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
            [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
            c='m', linestyle='-.', label='Additional Pose - Right Upper Arm' if l == 0 else "")
    
    ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
            [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
            [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
            c='c', linestyle='-.', label='Additional Pose - Right Forearm' if l == 0 else "")

# Set labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()



# # Plot the coordinates
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot arm poses
# for i, pose in enumerate(arm_pose_coords):
#     left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
#     right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
#     ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
#             [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
#             [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
#             c='r', linestyle='-', label='Left Upper Arm' if i == 0 else "")
    
#     ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
#             [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
#             [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
#             c='b', linestyle='-', label='Left Forearm' if i == 0 else "")
    
#     ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
#             [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
#             [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
#             c='r', linestyle='-', label='Right Upper Arm' if i == 0 else "")
    
#     ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
#             [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
#             [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
#             c='b', linestyle='-', label='Right Forearm' if i == 0 else "")

# # Plot forearm poses
# for pose in forearm_pose_coords:
#     left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
#     right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
#     ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
#             [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
#             [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
#             c='g', linestyle='--')
    
#     ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
#             [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
#             [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
#             c='olive', linestyle='--')
    
#     ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
#             [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
#             [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
#             c='g', linestyle='--')
    
#     ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
#             [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
#             [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
#             c='olive', linestyle='--')

# # Plot fixed poses
# for pose in fixed_pose_coords:
#     left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
#     right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
#     ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
#             [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
#             [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
#             c='gold', linestyle=':')
    
#     ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
#             [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
#             [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
#             c='coral', linestyle=':')
    
#     ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
#             [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
#             [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
#             c='gold', linestyle=':')
    
#     ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
#             [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
#             [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
#             c='coral', linestyle=':')

# ##============================================================================
# ##============================================================================
# # Plot additional forearm poses
# for pose in additional_fixed_pose_coords:
#     left_upper_arm_start_pos, left_upper_arm_end_pos, left_forearm_start_pos, left_forearm_end_pos, \
#     right_upper_arm_start_pos, right_upper_arm_end_pos, right_forearm_start_pos, right_forearm_end_pos = pose
    
#     ax.plot([left_upper_arm_start_pos[0], left_upper_arm_end_pos[0]], 
#             [left_upper_arm_start_pos[1], left_upper_arm_end_pos[1]], 
#             [left_upper_arm_start_pos[2], left_upper_arm_end_pos[2]], 
#             c='m', linestyle='-.')
    
#     ax.plot([left_forearm_start_pos[0], left_forearm_end_pos[0]], 
#             [left_forearm_start_pos[1], left_forearm_end_pos[1]], 
#             [left_forearm_start_pos[2], left_forearm_end_pos[2]], 
#             c='c', linestyle='-.')
    
#     ax.plot([right_upper_arm_start_pos[0], right_upper_arm_end_pos[0]], 
#             [right_upper_arm_start_pos[1], right_upper_arm_end_pos[1]], 
#             [right_upper_arm_start_pos[2], right_upper_arm_end_pos[2]], 
#             c='m', linestyle='-.')
    
#     ax.plot([right_forearm_start_pos[0], right_forearm_end_pos[0]], 
#             [right_forearm_start_pos[1], right_forearm_end_pos[1]], 
#             [right_forearm_start_pos[2], right_forearm_end_pos[2]], 
#             c='c', linestyle='-.')



# # Set labels and legend
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.legend()

# plt.show()


