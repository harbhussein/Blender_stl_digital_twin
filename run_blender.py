import subprocess
import os
import bpy

# Path to the Blender executable
blender_path = './blender/blender-launcher.sh'  

# Path to the Blender file you want to run
blend_file = './blender/male_mesh_2025_dose.blend'

# Additional command line arguments
script_file = './blender_codes/to_do_script.py'

# Construct the command
command = [blender_path, blend_file, '--python', script_file]

# Run the command
subprocess.run(command)
