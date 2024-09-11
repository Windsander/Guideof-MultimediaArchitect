import subprocess
import sys

def is_package_installed(package_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package_name):
    print(f"Installing {package_name}...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        print(f"{package_name} has been installed.")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}. Please try installing it manually.")

def main():
    packages = ["colour-science", "opencv-python", "opencv-contrib-python"]

    for package in packages:
        if is_package_installed(package):
            print(f"{package} is already installed.")
        else:
            install_package(package)

if __name__ == "__main__":
    main()