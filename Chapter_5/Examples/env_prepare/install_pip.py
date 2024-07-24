import os
import subprocess
import sys
import tempfile
import urllib.request


def is_pip_installed():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def download_get_pip(temp_dir):
    url = "https://bootstrap.pypa.io/get-pip.py"
    file_path = os.path.join(temp_dir, "get-pip.py")
    print(f"Downloading {url} to {file_path}...")
    urllib.request.urlretrieve(url, file_path)
    return file_path


def run_get_pip(file_path):
    print(f"Running {file_path}...")
    subprocess.run([sys.executable, file_path], check=True)


def main():
    if is_pip_installed():
        print("pip is already installed.")
    else:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download get-pip.py
            file_path = download_get_pip(temp_dir)

            # Run get-pip.py
            run_get_pip(file_path)


if __name__ == "__main__":
    main()
