import os
from subprocess import call

from docopt import docopt

from hurry.utils import (
    CommandList,
    ConfigReader,
    ExecChooser
)


def main():
    try:
        config = ConfigReader(os.getcwd()).get_dict()
    except FileNotFoundError:
        print("Can't find hurry.json in the current folder")
        return

    commands = CommandList(prefix="hurry")
    commands.add_config(config)
    arguments = docopt(commands.to_string(), options_first=True)
    executable_str = ExecChooser(config).get_exec(arguments)
    print("Execute: " + executable_str)
    call(executable_str, shell=True)
