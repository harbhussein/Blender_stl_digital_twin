import bpy
import math
import csv 

number_of_poses_to_generate = 10

armature_name = 'metarig'
left_upper_bone_name = 'upper_arm.L'
left_forearm_bone_name = 'forearm.L'
right_upper_bone_name = 'upper_arm.R'
right_forearm_bone_name = 'forearm.R'

# Counter for STL numbering
stl_counter = 1

# Function to save the armature as STL and log the bone coordinates to a pose-specific CSV
def save_as_stl_and_log_coords(pose_name):
    global stl_counter  # Access the counter from the global scope
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select the active object and store its current location and scale
    active_object = bpy.context.view_layer.objects.active
    original_location = active_object.location.copy()
    original_scale = active_object.scale.copy()
    
    # Center the object at the origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    active_object.location = (0, 0, 0)
    
    # Scale the object by 10 in all axes
    active_object.scale = (original_scale.x * 10, original_scale.y * 10, original_scale.z * 10)
    bpy.context.view_layer.update()

    # Save the object as STL with sequential naming
    filename = f"/home/harb/Data/lost+found/Phantom/P145/Electronic files/Phantom_data/MRCP_AM/poses/{stl_counter}.stl"
    active_object.select_set(True)
    bpy.ops.export_mesh.stl(filepath=filename)
    
    # Log the old pose name with the new STL number
    log_stl_mapping(pose_name, stl_counter)
    
    # Log bone coordinates with the same sequential number as the STL file
    log_bone_coordinates(stl_counter)
    
    # Revert the location and scale back to original after saving
    active_object.location = original_location
    active_object.scale = original_scale
    bpy.context.view_layer.update()

    # Increment the STL counter for the next STL file
    stl_counter += 1


# Function to log the STL mapping (pose name to STL number) in a CSV
def log_stl_mapping(pose_name, stl_number):
    csv_file_path = "/home/harb/Data/lost+found/Phantom/P145/Electronic files/Phantom_data/MRCP_AM/poses/stl_mapping.csv"

    # Append the mapping of the old pose name to the new STL number
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([stl_number, pose_name])  # Write STL number and pose name
        print(f"Logged STL number {stl_number} for pose {pose_name} in {csv_file_path}")

# Function to log the bone coordinates (x, y, z) to CSV with a pose-specific filename
def log_bone_coordinates(stl_counter):
    armature = bpy.data.objects.get(armature_name)
    if armature:
        # Collect center coordinates for all bones
        bones_data = []
        for bone in armature.pose.bones:
            head_coords = bone.head  # Get the bone head (base position)
            tail_coords = bone.tail  # Get the bone tail (end position)
            
            # Calculate the center of the bone (average of head and tail)
            center_coords = (head_coords + tail_coords) / 2

            # Append the center coordinate for the bone
            bones_data.append({
                'bone_name': bone.name,
                'center_x': center_coords.x,
                'center_y': center_coords.y,
                'center_z': center_coords.z
            })

        # Construct the CSV filename based on STL counter
        csv_file_path = f"/home/harb/Data/lost+found/Phantom/P145/Electronic files/Phantom_data/MRCP_AM/poses/{stl_counter}.csv"

        # Write the center coordinates to the CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['bone_name', 'center_x', 'center_y', 'center_z'])
            # Write header only if file is empty
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(bones_data)
            print(f"Logged all bone center coordinates to {csv_file_path}")
    else:
        print(f"Armature '{armature_name}' not found!")


# Function to rotate a pose bone
def rotate_bone(armature_name, upper_bone_name, forearm_bone_name, up_angle_deg, inward_angle_deg):
    armature = bpy.data.objects.get(armature_name)
    if armature:
        upper_bone = armature.pose.bones.get(upper_bone_name)
        forearm_bone = armature.pose.bones.get(forearm_bone_name)
        if upper_bone and forearm_bone:
            # Apply the rotation to the upper arm
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')

            bpy.ops.pose.select_all(action='DESELECT')
            upper_bone.bone.select = True
            bpy.context.view_layer.objects.active = armature

            # Convert angles to radians
            radians_up = math.radians(up_angle_deg)
            radians_inward = math.radians(inward_angle_deg)

            # Rotate upper arm bone around X axis to move up and around Y axis to move inward
            upper_bone.rotation_mode = 'XYZ'
            upper_bone.rotation_euler[0] = radians_up  # Rotate around X axis to move up
            upper_bone.rotation_euler[1] = radians_inward  # Rotate around Y axis to move inward
            upper_bone.rotation_euler[2] = 0  # Reset Z axis rotation

            # Apply the rotation to the forearm relative to the upper arm's rotation
            forearm_bone.rotation_mode = 'XYZ'
            forearm_bone.rotation_euler[0] = radians_up  # Same X axis rotation as upper arm
            forearm_bone.rotation_euler[1] = 0  # Reset Y axis rotation (forearm.L and forearm.R rotate towards each other)
            forearm_bone.rotation_euler[2] = 0  # Reset Z axis rotation

            # Update the scene
            bpy.context.view_layer.update()


# Function to generate arm poses
def generate_arm_poses(num_poses, armature_name, left_upper_bone_name, left_forearm_bone_name,
                        right_upper_bone_name, right_forearm_bone_name, start_up_angle,
                          end_up_angle, start_inward_angle, end_inward_angle):
    for i in range(num_poses):
        # Calculate interpolated angles
        up_angle_deg = start_up_angle - (start_up_angle - end_up_angle) * i / (num_poses - 1)
        inward_angle_deg = start_inward_angle - (start_inward_angle - end_inward_angle) * i / (num_poses - 1)

        # Rotate left and right arms for each angle
        rotate_bone(armature_name, left_upper_bone_name, left_forearm_bone_name, up_angle_deg, inward_angle_deg)
        rotate_bone(armature_name, right_upper_bone_name, right_forearm_bone_name, up_angle_deg, -inward_angle_deg)  # Right arm inward angle is opposite

        # Define pose name based on angles
        pose_name = f"pose_arm_{up_angle_deg:.1f}deg_{inward_angle_deg:.1f}inward"
        
        # Save the current pose as STL and log bone coordinates to a pose-specific CSV
        save_as_stl_and_log_coords(pose_name)
        print(f"Saved pose {pose_name}")




# Function to generate additional poses for a fixed upper arm angle with a given range of forearm inward angles
def generate_forearm_poses(fixed_upper_angle, max_forearm_angle):
    fixed_left_inward_angle = 0  # Fixed left inward angle
    fixed_right_inward_angle = 0  # Fixed right inward angle
    num_forearm_poses = number_of_poses_to_generate  # Number of forearm poses to generate

    # Generate additional poses for forearm rotations
    for j in range(num_forearm_poses):
        forearm_inward_angle = (max_forearm_angle / (num_forearm_poses - 1)) * j  # Calculate the forearm inward angle

        # Rotate left and right upper arms to fixed angles
        rotate_bone(armature_name, left_upper_bone_name, left_forearm_bone_name, fixed_upper_angle, fixed_left_inward_angle)
        rotate_bone(armature_name, right_upper_bone_name, right_forearm_bone_name, fixed_upper_angle, fixed_right_inward_angle)

        # Apply the forearm inward rotation
        left_forearm_bone = bpy.data.objects[armature_name].pose.bones[left_forearm_bone_name]
        right_forearm_bone = bpy.data.objects[armature_name].pose.bones[right_forearm_bone_name]

        
        left_forearm_bone.rotation_euler[1] = math.radians(forearm_inward_angle)
        right_forearm_bone.rotation_euler[1] = math.radians(-forearm_inward_angle)

        # Define pose name based on angles
        pose_name = f"pose_arm_{forearm_inward_angle:.1f}deg"
        
        # Update the scene
        bpy.context.view_layer.update()

        
        # Save the current pose as STL and log bone coordinates to a pose-specific CSV
        save_as_stl_and_log_coords(pose_name)
        print(f"Saved pose {pose_name}")


### To generate fixed poses, one side only, upper arm moves, while forearm extended ###

# Function to rotate a pose bone
def rotate_bone_only(armature_name, upper_bone_name, forearm_bone_name, up_angle_deg, inward_angle_deg):
    armature = bpy.data.objects.get(armature_name)
    if armature:
        upper_bone = armature.pose.bones.get(upper_bone_name)
        forearm_bone = armature.pose.bones.get(forearm_bone_name)
        if upper_bone and forearm_bone:
            # Apply the rotation to the upper arm
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')

            bpy.ops.pose.select_all(action='DESELECT')
            upper_bone.bone.select = True
            bpy.context.view_layer.objects.active = armature

            # Convert angles to radians
            radians_up = math.radians(up_angle_deg)
            radians_inward = math.radians(inward_angle_deg)

            # Rotate upper arm bone around X axis to move up and around Y axis to move inward
            upper_bone.rotation_mode = 'XYZ'
            upper_bone.rotation_euler[0] = radians_up  # Rotate around X axis to move up
            upper_bone.rotation_euler[1] = radians_inward  # Rotate around Y axis to move inward
            upper_bone.rotation_euler[2] = 0  # Reset Z axis rotation

            # Keep the forearm extended and aligned with the upper arm
            forearm_bone.rotation_mode = 'XYZ'
            forearm_bone.rotation_euler[0] = 0  # No rotation around X axis
            forearm_bone.rotation_euler[1] = 0  # Reset Y axis rotation
            forearm_bone.rotation_euler[2] = 0  # Reset Z axis rotation

            # Update the scene
            bpy.context.view_layer.update()



def generate_fixed_arm_poses_in_range(start_angle, end_angle, num_poses, armature_name, left_upper_bone_name, 
                                      left_forearm_bone_name, right_upper_bone_name, right_forearm_bone_name):
    fixed_forearm_angle = 0  # Fixed forearm angle

    for i in range(num_poses):
        # Calculate interpolated angle
        angle = start_angle + (end_angle - start_angle) * i / (num_poses - 1)

        # Left arm fixed, right arm rotated up
        rotate_bone_only(armature_name, left_upper_bone_name, left_forearm_bone_name, 0, 0)
        rotate_bone_only(armature_name, right_upper_bone_name, right_forearm_bone_name, angle, 0)

        # Define pose name based on angles
        pose_name = f"pose_right_arm_{angle:.1f}deg"
        
        # Save the current pose as STL and log bone coordinates to a pose-specific CSV
        save_as_stl_and_log_coords(pose_name)
        print(f"Saved pose {pose_name}")

        # Left arm rotated up, right arm fixed
        rotate_bone_only(armature_name, left_upper_bone_name, left_forearm_bone_name, angle, 0)
        rotate_bone_only(armature_name, right_upper_bone_name, right_forearm_bone_name, 0, 0)

        # Define pose name based on angles
        pose_name = f"pose_left_arm_{angle:.1f}deg"
        
        # Save the current pose as STL and log bone coordinates to a pose-specific CSV
        save_as_stl_and_log_coords(pose_name)
        print(f"Saved pose {pose_name}")

        # Both arms up
        rotate_bone_only(armature_name, left_upper_bone_name, left_forearm_bone_name, angle, 5)
        rotate_bone_only(armature_name, right_upper_bone_name, right_forearm_bone_name, angle, -5)

        # Define pose name based on angles
        pose_name = f"pose_two_arms_{angle:.1f}deg"
        
        # Save the current pose as STL and log bone coordinates to a pose-specific CSV
        save_as_stl_and_log_coords(pose_name)
        print(f"Saved pose {pose_name}")


                            # # =========== Main ============ # #
 
### 1 ###
# Hardcoded rotation angles
lower_angle = 70            # Angle to rotate the right arm up (in degrees)
right_inward_angle = -5     # Angle to rotate the right arm inward (in degrees)
upper_angle = 90            # Angle to rotate the left arm up (in degrees)
left_inward_angle = 5       # Angle to rotate the left arm inward (in degrees)

# Generate arm poses
generate_arm_poses(number_of_poses_to_generate, armature_name, left_upper_bone_name,
                    left_forearm_bone_name, right_upper_bone_name, right_forearm_bone_name, 
                    upper_angle, lower_angle, left_inward_angle, right_inward_angle)



### 2 ###
# Generate poses for upper arm angles at 45, 50, 55, and 60 degrees with different ranges for forearm angles not to overlap
angle_ranges = {
    45: 30,
    50: 30,
    55: 25,
    60: 25}

for angle, max_forearm_angle in angle_ranges.items():
    generate_forearm_poses(angle, max_forearm_angle)


### 3 ###
start_angle = 65
end_angle = 85
num_poses = number_of_poses_to_generate


generate_fixed_arm_poses_in_range(start_angle, end_angle, num_poses, armature_name, left_upper_bone_name,
                                   left_forearm_bone_name, right_upper_bone_name, right_forearm_bone_name)


# Additional angles to explore
additional_angles = {
    30: 30,  # Upper arm elevation starting from 30 degrees
    75: 20,  # Upper arm elevation from 75 to 55 degrees
    40: 20,  # Upper arm elevation from 40 to 20 degrees
    50: 15   # Upper arm elevation from 50 to 35 degrees
}

# Generate forearm poses for the specified additional angles
for angle, max_forearm_angle in additional_angles.items():
    generate_forearm_poses(angle, max_forearm_angle)

# # Additional fixed poses for the range of upper arm angles
# generate_fixed_arm_poses_in_range(50, 70, number_of_poses_to_generate, armature_name,
#                                   left_upper_bone_name, left_forearm_bone_name, right_upper_bone_name,
#                                   right_forearm_bone_name)

print("All poses saved.")


