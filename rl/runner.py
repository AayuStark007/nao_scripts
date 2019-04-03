import subprocess
import sys

if len(sys.argv) < 2:
    print("Please specify script to run")
    exit()

if sys.argv[1] == "runner.py":
    print("Cannot run itself")
    exit()

command = ["C:\\Python27\\python.exe"]
command.append(sys.argv[1:])

subprocess.call(command)