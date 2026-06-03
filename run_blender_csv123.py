import subprocess
import os
import bpy

# Path to the Blender executable
blender_path = '/home/harb/blender/blender-launcher.sh'  

# Path to the Blender file you want to run
#blend_file = '/home/harb/Data/lost+found/Phantom/P145/Electronic files/Phantom_data/MRCP_AM/male_mesh_2025.blend'

blend_file = '/home/harb/blender/male_mesh_2025_dose.blend'

# Additional command line arguments
script_file = '/home/harb/Documents/Python codes/blender_codes/to_do_script_csv123.py'

# Construct the command
command = [blender_path, blend_file, '--python', script_file]

# Run the command
subprocess.run(command)
