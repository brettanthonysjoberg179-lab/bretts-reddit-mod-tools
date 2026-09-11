"""Install script — pip install -r requirements.txt."""
import subprocess
import sys

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

if __name__ == "__main__":
    install()
