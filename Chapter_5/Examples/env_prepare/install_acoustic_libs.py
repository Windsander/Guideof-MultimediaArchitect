import subprocess
import sys
import platform


def is_package_installed(package_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name):
    print(f"Installing {package_name}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
    subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True)

def is_portaudio_installed():
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["brew", "list", "portaudio"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Linux":
            result = subprocess.run(["dpkg", "-s", "portaudio19-dev"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            return True  # Assume portaudio is handled manually on other platforms
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def install_portaudio():
    if platform.system() == "Darwin":  # macOS
        print("Installing portaudio using Homebrew...")
        subprocess.run(["brew", "install", "portaudio"], check=True)
    elif platform.system() == "Linux":
        print("Installing portaudio using APT...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "portaudio19-dev"], check=True)
    else:
        print("Please install portaudio manually for your platform.")
        sys.exit(1)

def main():
    packages = ["soundfile", "pyaudio", "librosa"]

    for package in packages:
        if package == "pyaudio":
            if not is_portaudio_installed():
                install_portaudio()
            if is_package_installed(package):
                print(f"{package} is already installed.")
            else:
                install_package(package)
                print(f"{package} has been installed.")
        else:
            if is_package_installed(package):
                print(f"{package} is already installed.")
            else:
                install_package(package)
                print(f"{package} has been installed.")


if __name__ == "__main__":
    main()