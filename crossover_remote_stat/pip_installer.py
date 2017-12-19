# This code install line by line a list of pip package
import sys
import pip

# usage:
# python pip_installer requirements.txt
def install(package):
    pip.main(['install', package])

# argv[1] expected to be requirements.txt
if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for line in f:
            install(line)