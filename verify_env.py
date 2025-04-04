import sys
import os
import subprocess

# Check if we are in a virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("You are already in a virtual environment.")
else:
    print("You are not in a virtual environment.")
    
    # Define the path to your virtual environment's activation script
    env_path = os.path.join(os.getcwd(), 'env')  # Assuming virtual environment folder is named 'env'

    # Check if the virtual environment folder exists
    if os.path.exists(env_path):
        print("Activating virtual environment...")
        # Run the shell and source the activate script using bash
        subprocess.run(['bash', '-i', '-c', 'source env/bin/activate && python Documents/sensor.py'], shell=False)
    else:
        print("Virtual environment not found. Please create one.")
