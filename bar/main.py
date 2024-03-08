import matplotlib
import platform

from foo import print_version

if __name__ == "__main__":
    print_version()
    print("python version: ", platform.python_version())
    print("matplotlib version: ", matplotlib.__version__)
