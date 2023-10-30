import subprocess
import sys

try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Required libraries installed successfully.")
except subprocess.CalledProcessError:
        print("An error occurred while installing required libraries.")
