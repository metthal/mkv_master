import subprocess
import sys


class Process:
    def __init__(self, name):
        self.name = name

    def run(self, args, return_output=False):
        all_args = [self.name] + args
        result = subprocess.run(all_args, stdout=subprocess.PIPE if return_output else sys.stdout, stderr=subprocess.STDOUT if return_output else sys.stderr)
        return result.returncode, result.stdout
